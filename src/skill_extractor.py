import re


def normalize_skill(skill):
    """
    Clean and normalize a skill name.
    """

    skill = str(skill).lower().strip()

    # Remove bullets
    skill = re.sub(
        r"^[\-\*\•\✓\✔\▪\●]+\s*",
        "",
        skill
    )

    # Remove extra spaces
    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    # Common aliases
    aliases = {
        "react.js": "react",
        "reactjs": "react",

        "nodejs": "node.js",
        "node js": "node.js",

        "restful api": "rest api",
        "restful apis": "rest api",
        "rest api": "rest api",

        "oop": "object-oriented programming",
        "object oriented programming": "object-oriented programming",

        "postgres": "postgresql",

        "google cloud platform": "gcp"
    }

    return aliases.get(
        skill,
        skill
    )


def get_skill_variants(skill):
    """
    Return possible textual variants
    of a normalized skill.

    Example:
    react -> react, react.js, reactjs
    """

    skill = normalize_skill(skill)

    variants = {
        "react": [
            "react",
            "react.js",
            "reactjs"
        ],

        "node.js": [
            "node.js",
            "nodejs",
            "node js"
        ],

        "rest api": [
            "rest api",
            "restful api",
            "restful apis"
        ],

        "object-oriented programming": [
            "object-oriented programming",
            "object oriented programming",
            "oop"
        ],

        "postgresql": [
            "postgresql",
            "postgres"
        ],

        "gcp": [
            "gcp",
            "google cloud platform"
        ]
    }

    return variants.get(
        skill,
        [skill]
    )


def skill_in_resume(skill, resume_text):
    """
    Check whether a JD skill exists
    in the candidate resume.

    Also supports common aliases.
    """

    resume_text = str(
        resume_text
    ).lower()

    normalized_skill = normalize_skill(
        skill
    )

    skill_variants = get_skill_variants(
        normalized_skill
    )

    for variant in skill_variants:

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(variant)
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(
            pattern,
            resume_text,
            flags=re.IGNORECASE
        ):
            return True

    return False


def extract_candidate_skills(
    resume_text,
    job_skills
):
    """
    Extract candidate skills relative
    to the current Job Description.

    No global hardcoded skill list
    is required here.
    """

    found_skills = []

    for skill in job_skills:

        normalized_skill = normalize_skill(
            skill
        )

        if skill_in_resume(
            normalized_skill,
            resume_text
        ):
            found_skills.append(
                normalized_skill
            )

    return sorted(
        set(found_skills)
    )


def calculate_skill_match(
    candidate_skills,
    job_skills
):
    """
    Original skill-match calculation.

    IMPORTANT:
    This function is retained for
    compatibility with the existing
    trained neural-network model.
    """

    if not job_skills:
        return 0.0

    candidate_set = set(
        normalize_skill(skill)
        for skill in candidate_skills
    )

    job_set = set(
        normalize_skill(skill)
        for skill in job_skills
    )

    matched_skills = (
        candidate_set
        & job_set
    )

    percentage = (
        len(matched_skills)
        / len(job_set)
    ) * 100

    return round(
        percentage,
        2
    )


def calculate_skill_breakdown(
    candidate_skills,
    required_skills,
    preferred_skills
):
    """
    Calculate separate Required and
    Preferred skill matches.

    Required skills receive greater
    importance than preferred skills.

    Weighted score:
    Required  = 70%
    Preferred = 30%

    This weighted score is currently
    intended for explanation/reporting.
    Existing NN compatibility is preserved
    through calculate_skill_match().
    """

    candidate_set = set(
        normalize_skill(skill)
        for skill in candidate_skills
    )

    required_set = set(
        normalize_skill(skill)
        for skill in required_skills
    )

    preferred_set = set(
        normalize_skill(skill)
        for skill in preferred_skills
    )

    matched_required = sorted(
        candidate_set
        & required_set
    )

    missing_required = sorted(
        required_set
        - candidate_set
    )

    matched_preferred = sorted(
        candidate_set
        & preferred_set
    )

    missing_preferred = sorted(
        preferred_set
        - candidate_set
    )

    # Required skill percentage
    if required_set:
        required_match = (
            len(matched_required)
            / len(required_set)
        ) * 100
    else:
        required_match = 100.0

    # Preferred skill percentage
    if preferred_set:
        preferred_match = (
            len(matched_preferred)
            / len(preferred_set)
        ) * 100
    else:
        preferred_match = 100.0

    # Weighted skill score
    if required_set and preferred_set:

        weighted_match = (
            required_match * 0.70
            + preferred_match * 0.30
        )

    elif required_set:

        weighted_match = required_match

    elif preferred_set:

        weighted_match = preferred_match

    else:

        weighted_match = 0.0

    return {
        "required_match": round(
            required_match,
            2
        ),

        "preferred_match": round(
            preferred_match,
            2
        ),

        "weighted_match": round(
            weighted_match,
            2
        ),

        "matched_required":
            matched_required,

        "missing_required":
            missing_required,

        "matched_preferred":
            matched_preferred,

        "missing_preferred":
            missing_preferred
    }