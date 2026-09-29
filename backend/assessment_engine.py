"""Lightweight technical assessment engine integrated from the SIH prototype concepts.
No external LLM/API is required, so the demo remains deterministic and offline-friendly.
"""
from __future__ import annotations

import re
import uuid
from typing import Dict, List

QUESTION_BANK: Dict[str, List[dict]] = {
    "python": [
        {"question": "Explain how try, except and finally work in Python.", "concepts": ["try", "except", "finally", "exception", "error"]},
        {"question": "What is the difference between a Python list and tuple?", "concepts": ["list", "tuple", "mutable", "immutable"]},
    ],
    "sql": [
        {"question": "Explain the difference between WHERE and HAVING in SQL.", "concepts": ["where", "having", "group", "aggregate"]},
        {"question": "What is an index and how can it improve query performance?", "concepts": ["index", "query", "performance", "lookup"]},
    ],
    "machine learning": [
        {"question": "Explain overfitting and two ways to reduce it.", "concepts": ["overfitting", "regularization", "validation", "dropout", "data"]},
        {"question": "Explain precision, recall and F1-score.", "concepts": ["precision", "recall", "f1", "false positive", "false negative"]},
    ],
    "docker": [
        {"question": "What is the difference between a Docker image and a container?", "concepts": ["image", "container", "runtime", "immutable"]},
        {"question": "Why is a Dockerfile used?", "concepts": ["dockerfile", "image", "build", "instructions"]},
    ],
    "git": [
        {"question": "Explain git commit, branch and merge in a team workflow.", "concepts": ["commit", "branch", "merge", "repository"]},
    ],
    "rest api": [
        {"question": "What makes an API RESTful? Explain common HTTP methods.", "concepts": ["http", "get", "post", "put", "delete", "resource"]},
    ],
    "fastapi": [
        {"question": "Why would you use FastAPI for a Python backend?", "concepts": ["fastapi", "python", "api", "validation", "async"]},
    ],
    "aws": [
        {"question": "Explain the roles of EC2, S3 and IAM in a basic AWS application.", "concepts": ["ec2", "s3", "iam", "compute", "storage", "access"]},
    ],
    "kubernetes": [
        {"question": "What are Pods and Deployments in Kubernetes?", "concepts": ["pod", "deployment", "replica", "container"]},
    ],
    "power bi": [
        {"question": "How would you build a reliable Power BI dashboard from raw data?", "concepts": ["power bi", "data", "model", "visual", "measure"]},
    ],
}


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def generate_assessment(candidate_id: str, skills: List[str], num_questions: int = 4) -> dict:
    clean_skills = list(dict.fromkeys(_normalize(s) for s in skills if _normalize(s)))
    questions = []
    for skill in clean_skills:
        bank = QUESTION_BANK.get(skill)
        if not bank:
            bank = [{
                "question": f"Explain your understanding of {skill} and describe a practical use case.",
                "concepts": [part for part in skill.split() if len(part) > 2] + ["example", "use"]
            }]
        for item in bank:
            questions.append({
                "question_id": f"Q-{uuid.uuid4().hex[:8]}",
                "skill": skill,
                "question": item["question"],
                "expected_concepts": item["concepts"],
            })
            if len(questions) >= max(1, min(num_questions, 8)):
                break
        if len(questions) >= max(1, min(num_questions, 8)):
            break

    if not questions:
        questions.append({
            "question_id": f"Q-{uuid.uuid4().hex[:8]}",
            "skill": "problem solving",
            "question": "Describe a difficult technical problem you solved and how you validated the solution.",
            "expected_concepts": ["problem", "solution", "test", "result"],
        })

    return {
        "assessment_id": f"AS-{uuid.uuid4().hex[:10]}",
        "candidate_id": candidate_id,
        "skills": clean_skills,
        "questions": questions,
    }


def evaluate_assessment(questions: List[dict], answers: Dict[str, str]) -> dict:
    results = []
    all_strengths, all_weaknesses = [], []

    for question in questions:
        qid = question.get("question_id", "")
        answer = str(answers.get(qid, "") or "").strip()
        answer_lower = answer.lower()
        concepts = [str(c).lower() for c in question.get("expected_concepts", [])]
        matched = [c for c in concepts if c in answer_lower]
        missing = [c for c in concepts if c not in answer_lower]
        coverage = len(matched) / len(concepts) if concepts else 0.5
        word_count = len(re.findall(r"\b\w+\b", answer))
        completeness = min(1.0, word_count / 30.0)
        score = round(min(100.0, (0.72 * coverage + 0.28 * completeness) * 100), 1)
        confidence = round(min(0.95, 0.55 + 0.25 * completeness + 0.15 * coverage), 2)

        if score >= 60:
            all_strengths.append(question.get("skill", "technical knowledge"))
        else:
            all_weaknesses.append(question.get("skill", "technical knowledge"))

        results.append({
            "question_id": qid,
            "skill": question.get("skill"),
            "question": question.get("question"),
            "answer": answer,
            "score": score,
            "confidence": confidence,
            "matched_concepts": matched,
            "missing_concepts": missing,
            "evidence_id": f"EV-{uuid.uuid4().hex[:8]}",
        })

    overall = round(sum(r["score"] for r in results) / len(results), 1) if results else 0.0
    confidence = round(sum(r["confidence"] for r in results) / len(results), 2) if results else 0.0
    return {
        "overall_score": overall,
        "confidence": confidence,
        "strengths": list(dict.fromkeys(all_strengths)),
        "weaknesses": list(dict.fromkeys(all_weaknesses)),
        "question_results": results,
    }


def combined_readiness(resume_score: float, assessment_score: float) -> float:
    # Prototype blend: resume evidence remains primary; assessment adds direct evidence.
    return round(max(0.0, min(100.0, 0.60 * float(resume_score or 0) + 0.40 * float(assessment_score or 0))), 1)
