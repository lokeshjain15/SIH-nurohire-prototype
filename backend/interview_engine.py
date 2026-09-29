from __future__ import annotations

import re
import uuid
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------
# NeuroHire AI Interview Engine
# Text-first, audio-ready prototype.
# Camera/video metadata is NEVER used for candidate competency scoring.
# ---------------------------------------------------------------------

INTERVIEW_BANK: Dict[str, List[Dict[str, Any]]] = {
    "python": [
        {
            "question": "Explain how exception handling works in Python and when you would use finally.",
            "concepts": ["try", "except", "finally", "exception", "error"],
        },
        {
            "question": "Describe the difference between a list and a tuple in Python and give a practical use case for each.",
            "concepts": ["list", "tuple", "mutable", "immutable"],
        },
    ],
    "machine learning": [
        {
            "question": "Explain overfitting in machine learning and describe two ways to reduce it.",
            "concepts": ["overfitting", "regularization", "validation", "dropout", "data"],
        },
        {
            "question": "How would you evaluate a classification model when the classes are imbalanced?",
            "concepts": ["precision", "recall", "f1", "confusion", "roc", "pr"],
        },
    ],
    "sql": [
        {
            "question": "Explain the difference between WHERE and HAVING in SQL.",
            "concepts": ["where", "having", "group", "aggregate"],
        },
        {
            "question": "What is a database index and what trade-offs does it introduce?",
            "concepts": ["index", "query", "performance", "write", "storage"],
        },
    ],
    "fastapi": [
        {
            "question": "Why would you choose FastAPI for a Python backend and how does request validation work?",
            "concepts": ["fastapi", "pydantic", "validation", "async", "api"],
        }
    ],
    "rest api": [
        {
            "question": "What makes an API RESTful? Explain common HTTP methods and status-code usage.",
            "concepts": ["http", "get", "post", "put", "delete", "status", "resource"],
        }
    ],
    "docker": [
        {
            "question": "Explain the difference between a Docker image and a running container.",
            "concepts": ["image", "container", "runtime", "dockerfile", "layer"],
        }
    ],
    "aws": [
        {
            "question": "Explain the roles of EC2, S3 and IAM in a basic AWS application.",
            "concepts": ["ec2", "s3", "iam", "compute", "storage", "access"],
        }
    ],
    "kubernetes": [
        {
            "question": "What are Pods and Deployments in Kubernetes, and why are replicas useful?",
            "concepts": ["pod", "deployment", "replica", "container"],
        }
    ],
    "git": [
        {
            "question": "Explain a safe Git workflow for feature development in a team.",
            "concepts": ["branch", "commit", "merge", "pull request", "repository"],
        }
    ],
    "mlops": [
        {
            "question": "What is MLOps and how would you monitor a machine-learning model after deployment?",
            "concepts": ["mlops", "deployment", "monitoring", "drift", "pipeline"],
        }
    ],
}

GENERIC_QUESTIONS = [
    {
        "question": "Describe a difficult technical problem you solved, the approach you used, and how you validated the result.",
        "concepts": ["problem", "approach", "test", "validate", "result"],
    },
    {
        "question": "Tell me about a time you had to learn a new technical skill quickly. How did you verify that you understood it?",
        "concepts": ["learn", "practice", "project", "test", "feedback"],
    },
]


def _normalize(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def generate_interview(
    candidate_id: str,
    skills: List[str],
    num_questions: int = 4,
    target_role: str = "Target Role",
) -> Dict[str, Any]:
    limit = max(1, min(int(num_questions or 4), 6))
    questions: List[Dict[str, Any]] = []

    normalized_skills = []
    for skill in skills or []:
        s = _normalize(skill)
        if s and s not in normalized_skills:
            normalized_skills.append(s)

    for skill in normalized_skills:
        bank = INTERVIEW_BANK.get(skill)
        if not bank:
            bank = [{
                "question": f"Explain your practical experience with {skill} and describe one real use case.",
                "concepts": [skill, "project", "implementation", "result"],
            }]

        for item in bank:
            questions.append({
                "question_id": f"IQ-{uuid.uuid4().hex[:8]}",
                "skill": skill,
                "question": item["question"],
                "expected_concepts": item.get("concepts", []),
                "assessment_mode": "interview",
            })
            if len(questions) >= limit:
                break
        if len(questions) >= limit:
            break

    generic_index = 0
    while len(questions) < limit:
        item = GENERIC_QUESTIONS[generic_index % len(GENERIC_QUESTIONS)]
        questions.append({
            "question_id": f"IQ-{uuid.uuid4().hex[:8]}",
            "skill": "general technical reasoning",
            "question": item["question"],
            "expected_concepts": item["concepts"],
            "assessment_mode": "interview",
        })
        generic_index += 1

    return {
        "interview_id": f"INT-{uuid.uuid4().hex[:10]}",
        "candidate_id": candidate_id,
        "target_role": target_role,
        "questions": questions,
        "mode": "text-first-audio-ready",
    }


def _score_answer(question: Dict[str, Any], transcript: str) -> Dict[str, Any]:
    text = _normalize(transcript)
    words = re.findall(r"[a-zA-Z0-9+#./-]+", text)
    word_count = len(words)

    concepts = [_normalize(c) for c in question.get("expected_concepts", []) if _normalize(c)]
    matched = [c for c in concepts if c in text]
    missing = [c for c in concepts if c not in text]

    concept_coverage = (len(matched) / len(concepts)) if concepts else 0.5

    if word_count == 0:
        completeness = 0.0
    elif word_count < 12:
        completeness = 0.35
    elif word_count < 30:
        completeness = 0.65
    elif word_count < 80:
        completeness = 0.9
    else:
        completeness = 1.0

    # Prototype clarity proxy: rewards structured, sufficiently developed answers.
    sentence_count = max(1, len(re.findall(r"[.!?]+", transcript)))
    avg_sentence_len = word_count / sentence_count if sentence_count else word_count
    if word_count == 0:
        clarity = 0.0
    elif 8 <= avg_sentence_len <= 35:
        clarity = 0.9
    elif 4 <= avg_sentence_len <= 50:
        clarity = 0.72
    else:
        clarity = 0.55

    relevance = min(1.0, 0.35 + 0.65 * concept_coverage) if text else 0.0

    score = round(
        100 * (
            0.50 * concept_coverage
            + 0.25 * completeness
            + 0.15 * clarity
            + 0.10 * relevance
        ),
        1,
    )

    confidence = round(
        min(0.97, 0.50 + 0.25 * completeness + 0.20 * concept_coverage),
        2,
    ) if text else 0.0

    communication_score = round(100 * (0.60 * clarity + 0.40 * completeness), 1)

    return {
        "question_id": question.get("question_id"),
        "skill": question.get("skill"),
        "question": question.get("question"),
        "score": score,
        "communication_score": communication_score,
        "confidence": confidence,
        "word_count": word_count,
        "matched_concepts": matched,
        "missing_concepts": missing,
        "transcript": transcript.strip(),
        "evidence_id": f"EVID-{uuid.uuid4().hex[:10]}",
    }


def evaluate_interview(
    questions: List[Dict[str, Any]],
    transcripts: Dict[str, str],
    camera_snapshot_captured: bool = False,
) -> Dict[str, Any]:
    results = []
    strengths = []
    weaknesses = []

    for question in questions or []:
        qid = str(question.get("question_id", ""))
        transcript = str((transcripts or {}).get(qid, "") or "")
        result = _score_answer(question, transcript)
        results.append(result)

        skill = result.get("skill") or "technical reasoning"
        if result["score"] >= 70:
            strengths.append(skill)
        elif result["score"] < 55:
            weaknesses.append(skill)

    if results:
        technical_score = round(sum(r["score"] for r in results) / len(results), 1)
        communication_score = round(
            sum(r["communication_score"] for r in results) / len(results), 1
        )
        confidence = round(sum(r["confidence"] for r in results) / len(results), 2)
    else:
        technical_score = 0.0
        communication_score = 0.0
        confidence = 0.0

    overall_score = round(0.75 * technical_score + 0.25 * communication_score, 1)

    return {
        "overall_score": overall_score,
        "technical_score": technical_score,
        "communication_score": communication_score,
        "confidence": confidence,
        "strengths": sorted(set(strengths)),
        "weaknesses": sorted(set(weaknesses)),
        "question_results": results,
        "media_metadata": {
            "has_camera_snapshot": bool(camera_snapshot_captured),
            "camera_used_for_scoring": False,
            "disclaimer": (
                "Camera/video capture is demonstration metadata only and is not "
                "used for competency scoring."
            ),
        },
    }


def final_readiness(
    resume_score: float,
    assessment_score: float,
    interview_score: float,
) -> float:
    """
    Prototype blend:
    45% Resume/JD NeuroHire score
    30% Technical assessment
    25% AI interview
    """
    try:
        r = float(resume_score or 0)
        a = float(assessment_score or 0)
        i = float(interview_score or 0)
    except (TypeError, ValueError):
        return 0.0

    score = 0.45 * r + 0.30 * a + 0.25 * i
    return round(max(0.0, min(100.0, score)), 1)


def transcribe_audio_file(audio_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Optional Faster-Whisper transcription.
    This function lazy-loads the model only when audio transcription is requested.
    If Faster-Whisper is unavailable, the API can gracefully fall back to manual text.
    """
    try:
        from faster_whisper import WhisperModel
    except Exception as exc:
        return "", {
            "available": False,
            "error": f"Faster-Whisper is not installed: {exc}",
        }

    try:
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path, beam_size=5)
        transcript = " ".join(seg.text.strip() for seg in segments if seg.text).strip()

        return transcript, {
            "available": True,
            "language": getattr(info, "language", "en"),
            "language_probability": float(
                getattr(info, "language_probability", 1.0) or 0.0
            ),
            "duration": float(getattr(info, "duration", 0.0) or 0.0),
        }
    except Exception as exc:
        return "", {
            "available": False,
            "error": str(exc),
        }
