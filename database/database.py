import sqlite3
import json
from datetime import datetime


DB_PATH = "database/neurohire.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def add_column_if_missing(
    cursor,
    table_name,
    column_name,
    column_definition
):
    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    existing_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    if column_name not in existing_columns:
        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name}
            {column_definition}
            """
        )


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT NOT NULL,
            job_description TEXT NOT NULL,
            neural_network_score REAL NOT NULL,
            recommendation TEXT NOT NULL,

            skill_match REAL,
            required_skill_match REAL,
            preferred_skill_match REAL,
            weighted_skill_match REAL,

            jd_similarity REAL,

            experience_years REAL,
            required_experience REAL,
            experience_score REAL,

            education_score REAL,

            matched_skills TEXT,
            missing_skills TEXT,

            matched_required_skills TEXT,
            missing_required_skills TEXT,

            matched_preferred_skills TEXT,
            missing_preferred_skills TEXT,

            required_skills TEXT,
            preferred_skills TEXT,
            job_skills TEXT,
            candidate_skills TEXT,

            recommendation_reason TEXT,

            created_at TEXT NOT NULL
        )
        """
    )


    # =====================================================
    # DATABASE MIGRATION FOR EXISTING DATABASE
    # =====================================================

    new_columns = {

        "required_skill_match":
            "REAL",

        "preferred_skill_match":
            "REAL",

        "weighted_skill_match":
            "REAL",

        "required_experience":
            "REAL",

        "matched_required_skills":
            "TEXT",

        "missing_required_skills":
            "TEXT",

        "matched_preferred_skills":
            "TEXT",

        "missing_preferred_skills":
            "TEXT",

        "required_skills":
            "TEXT",

        "preferred_skills":
            "TEXT",

        "job_skills":
            "TEXT",

        "candidate_skills":
            "TEXT"
    }


    for column_name, definition in new_columns.items():

        add_column_if_missing(
            cursor,
            "evaluations",
            column_name,
            definition
        )


    connection.commit()
    connection.close()


def save_evaluation(
    candidate_name,
    job_description,
    evaluation
):

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO evaluations (

            candidate_name,
            job_description,

            neural_network_score,
            recommendation,

            skill_match,
            required_skill_match,
            preferred_skill_match,
            weighted_skill_match,

            jd_similarity,

            experience_years,
            required_experience,
            experience_score,

            education_score,

            matched_skills,
            missing_skills,

            matched_required_skills,
            missing_required_skills,

            matched_preferred_skills,
            missing_preferred_skills,

            required_skills,
            preferred_skills,

            job_skills,
            candidate_skills,

            recommendation_reason,

            created_at
        )

        VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?
        )
        """,

        (
            candidate_name,

            job_description,

            evaluation[
                "neural_network_score"
            ],

            evaluation[
                "recommendation"
            ],

            evaluation.get(
                "skill_match",
                0.0
            ),

            evaluation.get(
                "required_skill_match",
                0.0
            ),

            evaluation.get(
                "preferred_skill_match",
                0.0
            ),

            evaluation.get(
                "weighted_skill_match",
                0.0
            ),

            evaluation.get(
                "jd_similarity",
                0.0
            ),

            evaluation.get(
                "experience_years",
                0.0
            ),

            evaluation.get(
                "required_experience",
                0.0
            ),

            evaluation.get(
                "experience_score",
                0.0
            ),

            evaluation.get(
                "education_score",
                0.0
            ),

            json.dumps(
                evaluation.get(
                    "matched_skills",
                    []
                )
            ),

            json.dumps(
                evaluation.get(
                    "missing_skills",
                    []
                )
            ),

            json.dumps(
                evaluation.get(
                    "matched_required_skills",
                    []
                )
            ),

            json.dumps(
                evaluation.get(
                    "missing_required_skills",
                    []
                )
            ),

            json.dumps(
                evaluation.get(
                    "matched_preferred_skills",
                    []
                )
            ),

            json.dumps(
                evaluation.get(
                    "missing_preferred_skills",
                    []
                )
            ),

            json.dumps(
                evaluation.get(
                    "required_skills",
                    []
                )
            ),

            json.dumps(
                evaluation.get(
                    "preferred_skills",
                    []
                )
            ),

            json.dumps(
                evaluation.get(
                    "job_skills",
                    []
                )
            ),

            json.dumps(
                evaluation.get(
                    "candidate_skills",
                    []
                )
            ),

            evaluation.get(
                "recommendation_reason",
                ""
            ),

            datetime.now().isoformat()
        )
    )


    connection.commit()

    evaluation_id = cursor.lastrowid

    connection.close()

    return evaluation_id


def get_evaluation_history():

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM evaluations
        ORDER BY id DESC
        """
    )


    rows = cursor.fetchall()

    connection.close()


    history = []


    json_fields = [

        "matched_skills",
        "missing_skills",

        "matched_required_skills",
        "missing_required_skills",

        "matched_preferred_skills",
        "missing_preferred_skills",

        "required_skills",
        "preferred_skills",

        "job_skills",
        "candidate_skills"
    ]


    for row in rows:

        item = dict(row)


        for field in json_fields:

            if field in item:

                try:

                    item[field] = json.loads(
                        item[field]
                        or "[]"
                    )

                except (
                    json.JSONDecodeError,
                    TypeError
                ):

                    item[field] = []


        history.append(
            item
        )


    return history


def delete_evaluation(
    evaluation_id
):

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM evaluations
        WHERE id = ?
        """,
        (
            evaluation_id,
        )
    )


    connection.commit()

    deleted = (
        cursor.rowcount > 0
    )

    connection.close()

    return deleted