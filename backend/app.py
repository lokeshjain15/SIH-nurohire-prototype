import os
import tempfile
import uuid
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from src.resume_parser import extract_resume_text
from src.predictor import predict_candidate
from backend.certificate_recommender import recommend_certificates
from backend.assessment_engine import (
    generate_assessment,
    evaluate_assessment,
    combined_readiness,
)
from backend.interview_engine import (
    generate_interview,
    evaluate_interview,
    final_readiness,
    transcribe_audio_file,
)

from database.database import (
    initialize_database,
    save_evaluation,
    get_evaluation_history,
    delete_evaluation
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="NeuroHire API",
    description=(
        "Real-time candidate evaluation "
        "and ranking API"
    ),
    version="1.1.0"
)


# =========================================================
# DATABASE
# =========================================================

initialize_database()


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# UPLOAD CONFIGURATION
# =========================================================

UPLOAD_DIR = "uploads"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx"
}

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "NeuroHire API is running",
        "version": "1.1.0"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================================
# SINGLE CANDIDATE EVALUATION
# =========================================================

@app.post("/evaluate")
async def evaluate_candidate(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # -----------------------------------------------------
    # Validate Job Description
    # -----------------------------------------------------

    if not job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description is required."
        )


    # -----------------------------------------------------
    # Validate Resume Extension
    # -----------------------------------------------------

    original_filename = (
        resume.filename
        or "resume"
    )

    extension = os.path.splitext(
        original_filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF and DOCX resumes "
                "are supported."
            )
        )


    # -----------------------------------------------------
    # Create Temporary Filename
    # -----------------------------------------------------

    unique_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )


    try:

        # -------------------------------------------------
        # Save Uploaded Resume Temporarily
        # -------------------------------------------------

        file_content = await resume.read()

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(
                file_content
            )


        # -------------------------------------------------
        # Extract Resume Text
        # -------------------------------------------------

        resume_text = extract_resume_text(
            file_path
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text found "
                    "in resume."
                )
            )


        # -------------------------------------------------
        # NeuroHire Prediction
        # -------------------------------------------------

        evaluation = predict_candidate(
            resume_text,
            job_description
        )


        # -------------------------------------------------
        # Certification Recommendations
        # -------------------------------------------------

        missing_required = evaluation.get(
            "missing_required_skills", []
        )
        missing_preferred = evaluation.get(
            "missing_preferred_skills", []
        )
        all_missing_skills = list(
            dict.fromkeys(missing_required + missing_preferred)
        )
        evaluation["certificate_recommendations"] = (
           recommend_certificates(
    all_missing_skills,
    evaluation.get("required_skills", []),
    evaluation.get("preferred_skills", [])
)
        )


        # -------------------------------------------------
        # Save Evaluation to Database
        # -------------------------------------------------

        evaluation_id = save_evaluation(
            candidate_name=original_filename,
            job_description=job_description,
            evaluation=evaluation
        )


        # -------------------------------------------------
        # API Response
        # -------------------------------------------------

        return {

            "success": True,

            "evaluation_id": evaluation_id,

            "candidate": {
                "file_name": original_filename
            },

            "evaluation": evaluation
        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


    finally:

        # -------------------------------------------------
        # Delete Temporary Resume
        # -------------------------------------------------

        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )


# =========================================================
# MULTIPLE CANDIDATE EVALUATION
# =========================================================

@app.post("/evaluate-multiple")
async def evaluate_multiple_candidates(
    resumes: List[UploadFile] = File(...),
    job_description: str = Form(...)
):

    # -----------------------------------------------------
    # Validate Job Description
    # -----------------------------------------------------

    if not job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description is required."
        )


    # -----------------------------------------------------
    # Validate Resume List
    # -----------------------------------------------------

    if len(resumes) == 0:

        raise HTTPException(
            status_code=400,
            detail=(
                "At least one resume "
                "is required."
            )
        )


    results = []


    # =====================================================
    # PROCESS EACH RESUME
    # =====================================================

    for resume in resumes:

        original_filename = (
            resume.filename
            or "resume"
        )

        extension = os.path.splitext(
            original_filename
        )[1].lower()


        # -------------------------------------------------
        # Unsupported File
        # -------------------------------------------------

        if extension not in ALLOWED_EXTENSIONS:

            results.append({

                "candidate_name":
                    original_filename,

                "error":
                    "Only PDF and DOCX resumes are supported."
            })

            continue


        # -------------------------------------------------
        # Temporary File
        # -------------------------------------------------

        unique_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_filename
        )


        try:

            # ---------------------------------------------
            # Save Resume
            # ---------------------------------------------

            content = await resume.read()

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    content
                )


            # ---------------------------------------------
            # Extract Resume Text
            # ---------------------------------------------

            resume_text = extract_resume_text(
                file_path
            )


            if not resume_text.strip():

                results.append({

                    "candidate_name":
                        original_filename,

                    "error":
                        "No readable text found in resume."
                })

                continue


            # ---------------------------------------------
            # NeuroHire Prediction
            # ---------------------------------------------

            evaluation = predict_candidate(
                resume_text,
                job_description
            )


            # ---------------------------------------------
            # Certification Recommendations
            # ---------------------------------------------

            missing_required = evaluation.get(
                "missing_required_skills", []
            )
            missing_preferred = evaluation.get(
                "missing_preferred_skills", []
            )
            all_missing_skills = list(
                dict.fromkeys(missing_required + missing_preferred)
            )
            evaluation["certificate_recommendations"] = (
                recommend_certificates(all_missing_skills)
            )


            # ---------------------------------------------
            # Save Result to Database
            # ---------------------------------------------

            evaluation_id = save_evaluation(
                candidate_name=original_filename,
                job_description=job_description,
                evaluation=evaluation
            )


            # ---------------------------------------------
            # Add Successful Evaluation
            # ---------------------------------------------

            results.append({

                "evaluation_id":
                    evaluation_id,

                "candidate_name":
                    original_filename,

                "evaluation":
                    evaluation
            })


        except Exception as error:

            results.append({

                "candidate_name":
                    original_filename,

                "error":
                    str(error)
            })


        finally:

            # ---------------------------------------------
            # Delete Temporary Resume
            # ---------------------------------------------

            if os.path.exists(
                file_path
            ):

                os.remove(
                    file_path
                )


    # =====================================================
    # SUCCESSFUL RESULTS
    # =====================================================

    successful_results = [

        candidate

        for candidate in results

        if "evaluation" in candidate
    ]


    # =====================================================
    # RANK BY NEURAL NETWORK SCORE
    # =====================================================

    successful_results.sort(

        key=lambda candidate:
            candidate[
                "evaluation"
            ][
                "neural_network_score"
            ],

        reverse=True
    )


    # =====================================================
    # ADD RANK
    # =====================================================

    for index, candidate in enumerate(
        successful_results,
        start=1
    ):

        candidate["rank"] = index


    # =====================================================
    # FAILED RESULTS
    # =====================================================

    failed_results = [

        candidate

        for candidate in results

        if "error" in candidate
    ]


    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "success": True,

        "total_uploaded":
            len(resumes),

        "total_evaluated":
            len(successful_results),

        "total_failed":
            len(failed_results),

        "ranking":
            successful_results,

        "failed":
            failed_results
    }


# =========================================================
# EVALUATION HISTORY
# =========================================================

@app.get("/history")
def evaluation_history():

    history = get_evaluation_history()

    return {

        "success": True,

        "total":
            len(history),

        "history":
            history
    }


# =========================================================
# DELETE HISTORY ITEM
# =========================================================

@app.delete(
    "/history/{evaluation_id}"
)
def remove_evaluation(
    evaluation_id: int
):

    deleted = delete_evaluation(
        evaluation_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail=(
                "Evaluation not found."
            )
        )


    return {

        "success": True,

        "message":
            "Evaluation deleted successfully."
    }

# =========================================================
# TARGETED TECHNICAL ASSESSMENT (SIH INTEGRATION)
# =========================================================

class AssessmentGenerateRequest(BaseModel):
    candidate_id: str
    skills: List[str] = Field(default_factory=list)
    num_questions: int = Field(default=4, ge=1, le=8)


class AssessmentEvaluateRequest(BaseModel):
    candidate_id: str
    resume_score: float = 0.0
    questions: List[Dict[str, Any]] = Field(default_factory=list)
    answers: Dict[str, str] = Field(default_factory=dict)


@app.post("/assessment/generate")
def create_targeted_assessment(payload: AssessmentGenerateRequest):
    return {
        "success": True,
        **generate_assessment(
            candidate_id=payload.candidate_id,
            skills=payload.skills,
            num_questions=payload.num_questions,
        ),
    }


@app.post("/assessment/evaluate")
def score_targeted_assessment(payload: AssessmentEvaluateRequest):
    result = evaluate_assessment(payload.questions, payload.answers)
    result["combined_readiness_score"] = combined_readiness(
        payload.resume_score,
        result["overall_score"],
    )
    return {
        "success": True,
        "candidate_id": payload.candidate_id,
        "resume_score": round(float(payload.resume_score or 0), 1),
        **result,
    }


@app.get("/assessment/health")
def assessment_health():
    return {
        "status": "healthy",
        "module": "targeted-technical-assessment",
        "mode": "offline-rule-based-prototype",
    }

# =========================================================
# AI INTERVIEW (SIH PHASE 2 INTEGRATION)
# =========================================================

class InterviewGenerateRequest(BaseModel):
    candidate_id: str
    skills: List[str] = Field(default_factory=list)
    target_role: str = "Target Role"
    num_questions: int = Field(default=4, ge=1, le=6)


class InterviewEvaluateRequest(BaseModel):
    candidate_id: str
    resume_score: float = 0.0
    assessment_score: float = 0.0
    questions: List[Dict[str, Any]] = Field(default_factory=list)
    transcripts: Dict[str, str] = Field(default_factory=dict)
    camera_snapshot_captured: bool = False


@app.get("/interview/health")
def interview_health():
    return {
        "status": "healthy",
        "module": "ai-interview",
        "mode": "text-first-audio-ready",
        "camera_used_for_scoring": False,
    }


@app.post("/interview/generate")
def create_interview(payload: InterviewGenerateRequest):
    return {
        "success": True,
        **generate_interview(
            candidate_id=payload.candidate_id,
            skills=payload.skills,
            num_questions=payload.num_questions,
            target_role=payload.target_role,
        ),
    }


@app.post("/interview/evaluate")
def score_interview(payload: InterviewEvaluateRequest):
    result = evaluate_interview(
        questions=payload.questions,
        transcripts=payload.transcripts,
        camera_snapshot_captured=payload.camera_snapshot_captured,
    )

    result["final_readiness_score"] = final_readiness(
        resume_score=payload.resume_score,
        assessment_score=payload.assessment_score,
        interview_score=result["overall_score"],
    )

    return {
        "success": True,
        "candidate_id": payload.candidate_id,
        "resume_score": round(float(payload.resume_score or 0), 1),
        "assessment_score": round(float(payload.assessment_score or 0), 1),
        **result,
    }


@app.post("/interview/transcribe")
async def interview_transcribe(audio: UploadFile = File(...)):
    suffix = os.path.splitext(audio.filename or "")[1] or ".webm"
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_path = temp.name

    try:
        content = await audio.read()
        temp.write(content)
        temp.flush()
        temp.close()

        transcript, info = transcribe_audio_file(temp_path)

        return {
            "success": bool(transcript),
            "transcript": transcript,
            "transcription": info,
        }
    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass

