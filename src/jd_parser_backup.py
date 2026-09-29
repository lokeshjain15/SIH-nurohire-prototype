import re

from src.skill_extractor import normalize_skill


# Common technical/professional skills used only as a fallback
# when a JD is written as an unstructured paragraph.
COMMON_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "php",
    "ruby",
    "go",
    "kotlin",
    "swift",

    "html",
    "css",
    "react",
    "react.js",
    "reactjs",
    "angular",
    "vue",
    "vue.js",

    "node.js",
    "nodejs",
    "express",
    "django",
    "flask",
    "fastapi",
    "spring",
    "spring boot",

    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "mongodb",
    "sqlite",
    "oracle",

    "aws",
    "azure",
    "gcp",
    "google cloud platform",

    "docker",
    "kubernetes",
    "jenkins",
    "git",
    "github",
    "gitlab",
    "ci/cd",

    "rest api",
    "restful api",
    "graphql",
    "microservices",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "tensorflow",
    "keras",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",

    "data structures",
    "algorithms",
    "object-oriented programming",
    "object oriented programming",
    "oop",

    "power bi",
    "tableau",
    "excel",

    "communication",
    "problem solving",
    "leadership",
    "teamwork",

    "accounting",
    "financial reporting",
    "financial analysis",
    "taxation",
    "auditing",
    "tally",
    "gst"
]


def clean_skill_line(line):
    """
    Clean one skill line from a JD.
    """

    line = str(line).strip()

    line = re.sub(
        r"^[\-\*\•\✓\✔\▪\●]+\s*",
        "",
        line
    )

    line = line.strip(" ,;:-")

    return line


def split_skills(text):
    """
    Convert a structured skill section
    into individual normalized skills.
    """

    skills = []

    for line in str(text).splitlines():

        line = clean_skill_line(line)

        if not line:
            continue

        parts = re.split(
            r"[,;|]",
            line
        )

        for part in parts:

            skill = clean_skill_line(part)

            if not skill:
                continue

            # Prevent complete sentences
            # from becoming skill names.
            if len(skill.split()) > 6:
                continue

            normalized = normalize_skill(skill)

            if normalized:
                skills.append(normalized)

    return sorted(set(skills))


def extract_section(
    job_description,
    start_headings,
    stop_headings
):
    """
    Extract text below a JD heading.

    Works with headings such as:
    Required Skills:
    Requirements:
    Preferred Skills:
    Nice to Have:
    """

    lines = str(job_description).splitlines()

    collecting = False
    collected = []

    for line in lines:

        clean_line = (
            line.strip()
            .lower()
            .rstrip(":")
        )

        is_start = any(
            clean_line == heading
            or clean_line.startswith(heading + ":")
            for heading in start_headings
        )

        if is_start:
            collecting = True

            # Supports:
            # Required Skills: Python, Java, SQL
            if ":" in line:
                inline_text = line.split(":", 1)[1].strip()

                if inline_text:
                    collected.append(inline_text)

            continue

        if collecting:

            is_stop = any(
                clean_line == heading
                or clean_line.startswith(heading + ":")
                for heading in stop_headings
            )

            if is_stop:
                break

            collected.append(line)

    return "\n".join(collected)


def skill_exists_in_text(skill, text):
    """
    Safely detect a known skill inside JD text.
    """

    normalized_skill = normalize_skill(skill)

    text = str(text).lower()

    # Check aliases as well as normalized value.
    variants = {
        normalized_skill,
        str(skill).lower().strip()
    }

    alias_variants = {
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

    if normalized_skill in alias_variants:
        variants.update(
            alias_variants[normalized_skill]
        )

    for variant in variants:

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(variant)
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        ):
            return True

    return False


def extract_unstructured_skills(job_description):
    """
    Fallback extraction for paragraph-style JDs.

    Example:
    We are looking for a Python developer with
    experience in Django, SQL, AWS and Docker.
    """

    detected = []

    for skill in COMMON_SKILLS:

        if skill_exists_in_text(
            skill,
            job_description
        ):
            detected.append(
                normalize_skill(skill)
            )

    return sorted(set(detected))


def extract_preferred_from_text(job_description):
    """
    Detect skills appearing in sentences containing
    preferred / nice-to-have wording.
    """

    preferred = []

    text = str(job_description)

    sentences = re.split(
        r"[\n.!?]+",
        text
    )

    preferred_markers = [
        "preferred",
        "nice to have",
        "nice-to-have",
        "bonus",
        "plus",
        "desirable",
        "advantage"
    ]

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if not any(
            marker in sentence_lower
            for marker in preferred_markers
        ):
            continue

        for skill in COMMON_SKILLS:

            if skill_exists_in_text(
                skill,
                sentence
            ):
                preferred.append(
                    normalize_skill(skill)
                )

    return sorted(set(preferred))


def extract_job_skills(job_description):
    """
    Extract Required + Preferred skills.

    Strategy:
    1. Read structured JD sections.
    2. Detect skills from the complete JD.
    3. Detect preferred skills from preference wording.
    4. Treat remaining detected skills as required.
    """

    job_description = str(job_description)

    required_text = extract_section(
        job_description,

        [
            "required skills",
            "requirements",
            "must have",
            "must-have",
            "required qualifications",
            "technical skills"
        ],

        [
            "preferred skills",
            "preferred qualifications",
            "nice to have",
            "nice-to-have",
            "experience",
            "education",
            "responsibilities",
            "job responsibilities",
            "about the role",
            "benefits"
        ]
    )

    preferred_text = extract_section(
        job_description,

        [
            "preferred skills",
            "preferred qualifications",
            "nice to have",
            "nice-to-have",
            "desirable skills"
        ],

        [
            "experience",
            "education",
            "responsibilities",
            "job responsibilities",
            "benefits",
            "about the company"
        ]
    )

    structured_required = split_skills(
        required_text
    )

    structured_preferred = split_skills(
        preferred_text
    )

    detected_all = extract_unstructured_skills(
        job_description
    )

    detected_preferred = extract_preferred_from_text(
        job_description
    )

    preferred_skills = sorted(
        set(
            structured_preferred
            + detected_preferred
        )
    )

    required_skills = sorted(
        set(
            structured_required
            + [
                skill
                for skill in detected_all
                if skill not in preferred_skills
            ]
        )
    )

    # A skill should not appear in both lists.
    required_skills = [
        skill
        for skill in required_skills
        if skill not in preferred_skills
    ]

    all_skills = sorted(
        set(
            required_skills
            + preferred_skills
        )
    )

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "all_skills": all_skills
    }


def extract_required_experience(job_description):
    """
    Detect minimum required experience.

    Examples:
    minimum 3 years
    at least 2 years
    3+ years
    3-5 years
    2 to 4 years
    3 years of experience
    experience of 4 years
    """

    text = str(job_description).lower()

    patterns = [
        r"minimum\s+(?:of\s+)?(\d+(?:\.\d+)?)\+?\s+years?",
        r"at\s+least\s+(\d+(?:\.\d+)?)\s+years?",
        r"(\d+(?:\.\d+)?)\+\s+years?",
        r"(\d+(?:\.\d+)?)\s*[-–]\s*\d+(?:\.\d+)?\s+years?",
        r"(\d+(?:\.\d+)?)\s+to\s+\d+(?:\.\d+)?\s+years?",
        r"(\d+(?:\.\d+)?)\s+years?\s+of\s+(?:relevant\s+)?experience",
        r"experience\s+of\s+(\d+(?:\.\d+)?)\+?\s+years?"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:
            return float(
                match.group(1)
            )

    return 0.0