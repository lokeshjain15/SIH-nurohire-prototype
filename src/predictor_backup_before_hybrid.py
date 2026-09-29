import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

from src.skill_extractor import (
    extract_candidate_skills,
    calculate_skill_match,
    calculate_skill_breakdown
)

from src.jd_parser import (
    extract_job_skills,
    extract_required_experience
)

from src.similarity import calculate_jd_similarity

from src.experience_extractor import (
    extract_experience,
    calculate_experience_score
)

from src.education_extractor import (
    calculate_education_score
)

MODEL_PATH = "models/neurohire_model_fixed.keras"
SCALER_PATH = "models/scaler.pkl"



model = load_model(
    MODEL_PATH,
    compile=False
)
scaler = joblib.load(SCALER_PATH)


def predict_candidate(
    resume_text,
    job_description
):

    # --------------------------------
    # 1. Extract Skills From JD
    # --------------------------------

    job_skill_data = extract_job_skills(
        job_description
    )

    required_skills = job_skill_data[
        "required_skills"
    ]

    preferred_skills = job_skill_data[
        "preferred_skills"
    ]

    job_skills = job_skill_data[
        "all_skills"
    ]


    # --------------------------------
    # 2. Extract Candidate Skills
    # --------------------------------

    candidate_skills = extract_candidate_skills(
        resume_text,
        job_skills
    )


    # --------------------------------
    # 3. Matched / Missing Skills
    # --------------------------------

    matched_skills = sorted(
        list(
            set(candidate_skills)
            & set(job_skills)
        )
    )

    missing_skills = sorted(
        list(
            set(job_skills)
            - set(candidate_skills)
        )
    )


    matched_required_skills = sorted(
        list(
            set(candidate_skills)
            & set(required_skills)
        )
    )

    missing_required_skills = sorted(
        list(
            set(required_skills)
            - set(candidate_skills)
        )
    )


    matched_preferred_skills = sorted(
        list(
            set(candidate_skills)
            & set(preferred_skills)
        )
    )

    missing_preferred_skills = sorted(
        list(
            set(preferred_skills)
            - set(candidate_skills)
        )
    )


    # --------------------------------
    # 4. Original Skill Match Score
    # --------------------------------
    # IMPORTANT:
    # This score is kept unchanged
    # for compatibility with the
    # existing trained NN model.
    # --------------------------------

    skill_score = calculate_skill_match(
        candidate_skills,
        job_skills
    )


    # --------------------------------
    # 5. Required / Preferred Breakdown
    # --------------------------------

    skill_breakdown = calculate_skill_breakdown(
        candidate_skills,
        required_skills,
        preferred_skills
    )

    required_skill_match = skill_breakdown[
        "required_match"
    ]

    preferred_skill_match = skill_breakdown[
        "preferred_match"
    ]

    weighted_skill_match = skill_breakdown[
        "weighted_match"
    ]


    # --------------------------------
    # 6. JD Similarity
    # --------------------------------

    similarity_score = calculate_jd_similarity(
        resume_text,
        job_description
    )


    # --------------------------------
    # 7. Experience
    # --------------------------------

    experience_years = extract_experience(
        resume_text
    )

    required_experience = (
        extract_required_experience(
            job_description
        )
    )

    if required_experience > 0:

        experience_score = (
            calculate_experience_score(
                experience_years,
                required_years=required_experience
            )
        )

    else:

        experience_score = 100.0


    # --------------------------------
    # 8. Education
    # --------------------------------

    education_score = (
    calculate_education_score(
        resume_text,
        job_description
    )
)


    # --------------------------------
    # 9. Prepare Neural Network Input
    # --------------------------------
    # DO NOT replace skill_score with
    # weighted_skill_match here.
    #
    # Existing model was trained using:
    # Skill_Match
    # JD_Similarity
    # Experience_Score
    # Education_Score
    # --------------------------------

    feature_names = [
        "Skill_Match",
        "JD_Similarity",
        "Experience_Score",
        "Education_Score"
    ]

    feature_values = [[
        skill_score,
        similarity_score,
        experience_score,
        education_score
    ]]

    features = pd.DataFrame(
        feature_values,
        columns=feature_names
    )


    # --------------------------------
    # 10. Apply Scaler
    # --------------------------------

    scaled_features = scaler.transform(
        features
    )


    # --------------------------------
    # 11. Neural Network Prediction
    # --------------------------------

    prediction = model.predict(
        scaled_features,
        verbose=0
    )[0][0]

    prediction = float(
        np.clip(
            prediction,
            0,
            100
        )
    )


    # --------------------------------
    # 12. Recommendation
    # --------------------------------

    if prediction >= 70:

        recommendation = (
            "Strong Match"
        )

    elif prediction >= 50:

        recommendation = (
            "Moderate Match"
        )

    elif prediction >= 30:

        recommendation = (
            "Weak Match"
        )

    else:

        recommendation = (
            "Low Match"
        )


    # --------------------------------
    # 13. Explanation
    # --------------------------------

    explanations = []


    total_job_skills = len(
        job_skills
    )

    matched_count = len(
        matched_skills
    )


    if total_job_skills > 0:

        explanations.append(
            f"{matched_count} of "
            f"{total_job_skills} "
            f"job skills matched."
        )

    else:

        explanations.append(
            "No job skills were detected "
            "in the job description."
        )


    # Required Skills Explanation

    if len(required_skills) > 0:

        explanations.append(
            f"{len(matched_required_skills)} of "
            f"{len(required_skills)} "
            f"required skills matched "
            f"({required_skill_match}%)."
        )

        if len(
            missing_required_skills
        ) > 0:

            explanations.append(
                f"{len(missing_required_skills)} "
                f"required skills are missing."
            )

    else:

        explanations.append(
            "No separate required skills "
            "were detected."
        )


    # Preferred Skills Explanation

    if len(preferred_skills) > 0:

        explanations.append(
            f"{len(matched_preferred_skills)} of "
            f"{len(preferred_skills)} "
            f"preferred skills matched "
            f"({preferred_skill_match}%)."
        )

        if len(
            missing_preferred_skills
        ) > 0:

            explanations.append(
                f"{len(missing_preferred_skills)} "
                f"preferred skills are missing."
            )


    # Experience Explanation

    if required_experience > 0:

        if (
            experience_years
            < required_experience
        ):

            explanations.append(
                f"Detected experience is "
                f"{experience_years} years, "
                f"below the "
                f"{required_experience}-year "
                f"requirement."
            )

        else:

            explanations.append(
                f"Experience requirement of "
                f"{required_experience} years "
                f"is satisfied with "
                f"{experience_years} years "
                f"detected."
            )

    else:

        explanations.append(
            "No minimum experience "
            "requirement was detected "
            "in the job description."
        )


    # Education Explanation

    if education_score >= 100:

        explanations.append(
            "Education requirement appears "
            "to be satisfied."
        )

    else:

        explanations.append(
            "Education requirement may not "
            "be fully satisfied."
        )


    recommendation_reason = " ".join(
        explanations
    )


    # --------------------------------
    # 14. Return Result
    # --------------------------------

    return {

        "candidate_skills":
            candidate_skills,

        "job_skills":
            job_skills,

        "required_skills":
            required_skills,

        "preferred_skills":
            preferred_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "matched_required_skills":
            matched_required_skills,

        "missing_required_skills":
            missing_required_skills,

        "matched_preferred_skills":
            matched_preferred_skills,

        "missing_preferred_skills":
            missing_preferred_skills,

        # Original skill score used by NN
        "skill_match":
            skill_score,

        # New detailed skill scores
        "required_skill_match":
            required_skill_match,

        "preferred_skill_match":
            preferred_skill_match,

        "weighted_skill_match":
            weighted_skill_match,

        "jd_similarity":
            similarity_score,

        "experience_years":
            experience_years,

        "required_experience":
            required_experience,

        "experience_score":
            experience_score,

        "education_score":
            education_score,

        "neural_network_score":
            round(
                prediction,
                2
            ),

        "recommendation":
            recommendation,

        "recommendation_reason":
            recommendation_reason
    }