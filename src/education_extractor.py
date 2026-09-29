import re


# =========================================================
# EDUCATION LEVEL CONFIGURATION
# =========================================================

EDUCATION_LEVELS = {
    "none": 0,
    "diploma": 1,
    "bachelor": 2,
    "master": 3,
    "doctorate": 4
}


# =========================================================
# DETECT EDUCATION LEVEL
# =========================================================

def extract_education_level(text):
    """
    Detect the highest education level mentioned
    in a resume or job description.
    """

    text = str(text).lower()

    # -----------------------------------------------------
    # Doctorate
    # -----------------------------------------------------

    doctorate_patterns = [
        r"\bph\.?d\.?\b",
        r"\bdoctorate\b",
        r"\bdoctoral\b"
    ]

    # -----------------------------------------------------
    # Master's
    # -----------------------------------------------------

    master_patterns = [
        r"\bmaster'?s?\b",
        r"\bm\.?\s*tech\b",
        r"\bmtech\b",
        r"\bm\.?\s*sc\b",
        r"\bmsc\b",
        r"\bm\.?\s*c\.?\s*a\.?\b",
        r"\bmca\b",
        r"\bm\.?\s*b\.?\s*a\.?\b",
        r"\bmba\b",
        r"\bm\.?\s*e\.?\b"
    ]

    # -----------------------------------------------------
    # Bachelor's
    # -----------------------------------------------------

    bachelor_patterns = [
        r"\bbachelor'?s?\b",
        r"\bb\.?\s*tech\b",
        r"\bbtech\b",
        r"\bb\.?\s*e\.?\b",
        r"\bb\.?\s*sc\b",
        r"\bbsc\b",
        r"\bb\.?\s*c\.?\s*a\.?\b",
        r"\bbca\b",
        r"\bb\.?\s*b\.?\s*a\.?\b",
        r"\bbba\b"
    ]

    # -----------------------------------------------------
    # Diploma
    # -----------------------------------------------------

    diploma_patterns = [
        r"\bdiploma\b",
        r"\bpolytechnic\b"
    ]

    groups = [
        ("doctorate", doctorate_patterns),
        ("master", master_patterns),
        ("bachelor", bachelor_patterns),
        ("diploma", diploma_patterns)
    ]

    for level, patterns in groups:

        for pattern in patterns:

            if re.search(pattern, text):
                return level

    return "none"


# =========================================================
# CALCULATE EDUCATION SCORE
# =========================================================

def calculate_education_score(
    resume_text,
    job_description=None
):
    """
    Compare candidate education with the education
    requirement from the job description.

    Score interpretation:

    Candidate meets/exceeds requirement = 100
    One level below requirement          = 70
    Two levels below requirement         = 40
    No qualification detected            = 0

    If no education requirement can be detected
    in the JD, education does not penalize the
    candidate and receives 100.
    """

    candidate_level = extract_education_level(
        resume_text
    )

    # -----------------------------------------------------
    # Backward compatibility
    # -----------------------------------------------------
    # If no JD is supplied, retain sensible behavior based
    # on candidate education alone.

    if job_description is None:

        if candidate_level in [
            "doctorate",
            "master",
            "bachelor"
        ]:
            return 100.0

        if candidate_level == "diploma":
            return 60.0

        return 0.0


    required_level = extract_education_level(
        job_description
    )


    # -----------------------------------------------------
    # No explicit education requirement detected
    # -----------------------------------------------------

    if required_level == "none":
        return 100.0


    candidate_rank = EDUCATION_LEVELS.get(
        candidate_level,
        0
    )

    required_rank = EDUCATION_LEVELS.get(
        required_level,
        0
    )


    # -----------------------------------------------------
    # Candidate meets or exceeds requirement
    # -----------------------------------------------------

    if candidate_rank >= required_rank:
        return 100.0


    # -----------------------------------------------------
    # No education detected
    # -----------------------------------------------------

    if candidate_rank == 0:
        return 0.0


    difference = (
        required_rank - candidate_rank
    )


    # One qualification level below
    if difference == 1:
        return 70.0


    # Two levels below
    if difference == 2:
        return 40.0


    return 20.0