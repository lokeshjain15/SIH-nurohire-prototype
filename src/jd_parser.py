import re

from src.skill_extractor import normalize_skill


# =========================================================
# COMMON SKILLS
# Used as fallback for unstructured Job Descriptions
# =========================================================

COMMON_SKILLS = [

    # Programming Languages
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

    # Frontend
    "html",
    "css",
    "react",
    "react.js",
    "reactjs",
    "angular",
    "vue",
    "vue.js",

    # Backend
    "node.js",
    "nodejs",
    "express",
    "django",
    "flask",
    "fastapi",
    "spring",
    "spring boot",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "mongodb",
    "sqlite",
    "oracle",

    # Cloud
    "aws",
    "azure",
    "gcp",
    "google cloud platform",

    # DevOps
    "docker",
    "kubernetes",
    "jenkins",
    "git",
    "github",
    "gitlab",
    "ci/cd",

    # APIs / Architecture
    "rest api",
    "restful api",
    "graphql",
    "microservices",

    # AI / ML / Data
    "machine learning",
    "deep learning",
    "mlops",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "tensorflow",
    "keras",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    

    # CS Fundamentals
    "data structures",
    "algorithms",
    "object-oriented programming",
    "object oriented programming",
    "oop",

    # Analytics
    "power bi",
    "tableau",
    "excel",

    # Professional Skills
    "communication",
    "problem solving",
    "leadership",
    "teamwork",

    # Finance / Accounting
    "accounting",
    "financial reporting",
    "financial analysis",
    "taxation",
    "auditing",
    "tally",
    "gst"
]


# =========================================================
# HEADINGS
# =========================================================

REQUIRED_HEADINGS = [
    "required skills",
    "requirements",
    "must have",
    "must-have",
    "required qualifications",
    "technical skills",
    "mandatory skills",
    "essential skills"
]


PREFERRED_HEADINGS = [
    "preferred skills",
    "preferred qualifications",
    "nice to have",
    "nice-to-have",
    "desirable skills",
    "good to have",
    "bonus skills"
]


OTHER_HEADINGS = [
    "experience",
    "education",
    "responsibilities",
    "job responsibilities",
    "about the role",
    "about the company",
    "benefits",
    "job description",
    "role",
    "qualifications"
]


# =========================================================
# BASIC CLEANING
# =========================================================

def clean_skill_line(line):
    """
    Clean one skill line.
    """

    line = str(line).strip()

    line = re.sub(
        r"^[\-\*\•\✓\✔\▪\●]+\s*",
        "",
        line
    )

    line = line.strip(
        " ,;:-"
    )

    return line


# =========================================================
# SPLIT STRUCTURED SKILLS
# =========================================================

def split_skills(text):
    """
    Convert structured skill text into
    normalized individual skills.
    """

    skills = []

    text = str(text)

    # Split by lines, comma, semicolon or pipe
    raw_parts = re.split(
        r"[\n,;|]+",
        text
    )

    for part in raw_parts:

        skill = clean_skill_line(
            part
        )

        if not skill:
            continue

        # Avoid complete sentences becoming skills
        if len(skill.split()) > 6:
            continue

        normalized = normalize_skill(
            skill
        )

        if normalized:
            skills.append(
                normalized
            )

    return sorted(
        set(skills)
    )


# =========================================================
# HEADING REGEX
# =========================================================

def build_heading_pattern(headings):
    """
    Build regex pattern for section headings.
    """

    escaped = sorted(
        [
            re.escape(heading)
            for heading in headings
        ],
        key=len,
        reverse=True
    )

    return (
        r"(?i)(?<![a-zA-Z0-9])"
        r"(?:"
        + "|".join(escaped)
        + r")"
        r"\s*:?"
    )


# =========================================================
# EXTRACT SECTION
# =========================================================

def extract_section(
    job_description,
    start_headings,
    stop_headings
):
    """
    Extract text belonging to one JD section.

    Supports:

    Required Skills:
    Python
    Java

    Preferred Skills:
    AWS

    and also:

    Required Skills: Python, Java, SQL
    Preferred Skills: AWS, Docker
    """

    text = str(
        job_description
    )

    start_pattern = re.compile(
        build_heading_pattern(
            start_headings
        )
    )

    stop_pattern = re.compile(
        build_heading_pattern(
            stop_headings
        )
    )

    start_match = start_pattern.search(
        text
    )

    if not start_match:
        return ""

    section_start = (
        start_match.end()
    )

    stop_match = stop_pattern.search(
        text,
        section_start
    )

    if stop_match:

        section_end = (
            stop_match.start()
        )

    else:

        section_end = len(
            text
        )

    return text[
        section_start:
        section_end
    ].strip()


# =========================================================
# SKILL SEARCH
# =========================================================

def skill_exists_in_text(
    skill,
    text
):
    """
    Detect a skill safely inside text.
    """

    normalized_skill = normalize_skill(
        skill
    )

    text = str(
        text
    ).lower()

    variants = {
        normalized_skill,
        str(skill).lower().strip()
    }

    alias_variants = {

        # =================================================
        # FRONTEND
        # =================================================

        "react": [
            "react",
            "react.js",
            "reactjs",
            "react js"
        ],

        "vue": [
            "vue",
            "vue.js",
            "vuejs",
            "vue js"
        ],

        # =================================================
        # BACKEND
        # =================================================

        "node.js": [
            "node.js",
            "nodejs",
            "node js"
        ],

        "fastapi": [
            "fastapi",
            "fast api"
        ],

        "spring boot": [
            "spring boot",
            "springboot"
        ],

        # =================================================
        # API / ARCHITECTURE
        # =================================================

        "rest api": [
            "rest api",
            "rest APIs",
            "restful api",
            "restful APIs",
            "restful services",
            "rest services"
        ],

        "microservices": [
            "microservices",
            "microservice",
            "micro-services",
            "micro-service"
        ],

        # =================================================
        # DATABASE
        # =================================================

        "postgresql": [
            "postgresql",
            "postgres",
            "postgre sql"
        ],

        "mongodb": [
            "mongodb",
            "mongo db"
        ],

        # =================================================
        # CLOUD
        # =================================================

        "aws": [
            "aws",
            "amazon web services"
        ],

        "gcp": [
            "gcp",
            "google cloud",
            "google cloud platform"
        ],

        "azure": [
            "azure",
            "microsoft azure"
        ],

        # =================================================
        # DEVOPS
        # =================================================

        "git": [
            "git"
        ],

        "github": [
            "github",
            "git hub"
        ],

        "ci/cd": [
            "ci/cd",
            "ci cd",
            "ci-cd",
            "continuous integration",
            "continuous deployment",
            "continuous delivery"
        ],

        "docker": [
            "docker",
            "docker container",
            "docker containers"
        ],

        "kubernetes": [
            "kubernetes",
            "k8s"
        ],

        # =================================================
        # AI / ML
        # =================================================

        "machine learning": [
            "machine learning",
            "ml"
        ],

        "deep learning": [
            "deep learning",
            "dl"
        ],

        "artificial intelligence": [
            "artificial intelligence",
            "ai"
        ],

        "natural language processing": [
            "natural language processing",
            "nlp"
        ],

        "mlops": [
            "mlops",
            "ml ops",
            "ml-ops",
            "machine learning operations"
        ],

        "scikit-learn": [
            "scikit-learn",
            "scikit learn",
            "sklearn"
        ],

        "tensorflow": [
            "tensorflow",
            "tensor flow"
        ],

        "pytorch": [
            "pytorch",
            "py torch"
        ],

        # =================================================
        # PROGRAMMING
        # =================================================

        "c#": [
            "c#",
            "c sharp"
        ],

        "c++": [
            "c++",
            "cpp"
        ],

        # =================================================
        # ANALYTICS
        # =================================================

        "power bi": [
            "power bi",
            "powerbi"
        ],

        # =================================================
        # CS FUNDAMENTALS
        # =================================================

        "object-oriented programming": [
            "object-oriented programming",
            "object oriented programming",
            "oop"
        ]
    }


    if normalized_skill in alias_variants:

        variants.update(
            alias_variants[
                normalized_skill
            ]
        )


    for variant in variants:

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(
                variant
            )
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        ):

            return True


    return False


# =========================================================
# DETECT KNOWN SKILLS
# =========================================================

def extract_unstructured_skills(
    job_description
):
    """
    Detect known skills from normal paragraph text.
    """

    detected = []

    for skill in COMMON_SKILLS:

        if skill_exists_in_text(
            skill,
            job_description
        ):

            detected.append(
                normalize_skill(
                    skill
                )
            )

    return sorted(
        set(detected)
    )


# =========================================================
# EXPLICIT PREFERRED WORDING
# =========================================================

def extract_preferred_from_text(
    job_description
):
    """
    Detect skills occurring inside sentences
    containing preferred wording.

    Used mainly when there is no explicit
    Preferred Skills section.
    """

    preferred = []

    text = str(
        job_description
    )

    sentences = re.split(
        r"[\n.!?]+",
        text
    )

    preferred_markers = [
        "preferred",
        "nice to have",
        "nice-to-have",
        "bonus",
        "desirable",
        "advantage",
        "good to have"
    ]


    for sentence in sentences:

        sentence_lower = (
            sentence.lower()
        )

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
                    normalize_skill(
                        skill
                    )
                )


    return sorted(
        set(preferred)
    )


# =========================================================
# EXTRACT SECTION SKILLS
# =======================================================



def extract_skills_from_section(
    section_text
):
    """
    Extract only recognized skills
    from a structured JD section.

    Prevents complete lines such as:
    'JavaScript React AWS Docker'
    from becoming one fake skill.
    """

    if not str(section_text).strip():
        return []

    return extract_unstructured_skills(
        section_text
    )

# =========================================================
# JOB SKILLS
# =========================================================

def extract_job_skills(
    job_description
):
    """
    Extract Required and Preferred skills.

    Priority:
    1. Explicit Required / Preferred sections
    2. Preferred wording in normal text
    3. Remaining detected skills become required
    """

    job_description = str(
        job_description
    )


    # -----------------------------------------------------
    # REQUIRED SECTION
    # -----------------------------------------------------

    required_stop_headings = (
        PREFERRED_HEADINGS
        + OTHER_HEADINGS
    )

    required_text = extract_section(
        job_description,
        REQUIRED_HEADINGS,
        required_stop_headings
    )


    # -----------------------------------------------------
    # PREFERRED SECTION
    # -----------------------------------------------------

    preferred_stop_headings = (
        REQUIRED_HEADINGS
        + OTHER_HEADINGS
    )

    preferred_text = extract_section(
        job_description,
        PREFERRED_HEADINGS,
        preferred_stop_headings
    )


    # -----------------------------------------------------
    # EXTRACT EXPLICIT SECTION SKILLS
    # -----------------------------------------------------

    structured_required = (
        extract_skills_from_section(
            required_text
        )
    )

    structured_preferred = (
        extract_skills_from_section(
            preferred_text
        )
    )


    # -----------------------------------------------------
    # ALL SKILLS IN JD
    # -----------------------------------------------------

    detected_all = (
        extract_unstructured_skills(
            job_description
        )
    )


    # -----------------------------------------------------
    # PREFERRED LOGIC
    # -----------------------------------------------------

    if structured_preferred:

        # Explicit section takes priority.
        preferred_skills = sorted(
            set(
                structured_preferred
            )
        )

    else:

        preferred_skills = (
            extract_preferred_from_text(
                job_description
            )
        )


    # -----------------------------------------------------
    # REQUIRED LOGIC
    # -----------------------------------------------------

    if structured_required:

        # When the JD explicitly provides a Required Skills section,
        # treat that section as authoritative. Do NOT promote every
        # skill mentioned elsewhere (education, responsibilities,
        # certifications, company description, etc.) to "required".
        required_skills = sorted(
            set(
                structured_required
            )
        )

    else:

        # No explicit Required Skills section:
        # fall back to skills detected across the JD, excluding
        # anything identified as preferred.
        required_skills = sorted(
            [
                skill
                for skill in detected_all
                if skill
                not in preferred_skills
            ]
        )


    # -----------------------------------------------------
    # REMOVE DUPLICATES BETWEEN CATEGORIES
    # -----------------------------------------------------

    preferred_set = set(
        preferred_skills
    )

    required_skills = sorted(
        [
            skill
            for skill in required_skills
            if skill not in preferred_set
        ]
    )

    preferred_skills = sorted(
        preferred_set
    )


    # -----------------------------------------------------
    # ALL SKILLS
    # -----------------------------------------------------

    all_skills = sorted(
        set(
            required_skills
            + preferred_skills
        )
    )


    return {

        "required_skills":
            required_skills,

        "preferred_skills":
            preferred_skills,

        "all_skills":
            all_skills
    }


# =========================================================
# EXPERIENCE REQUIREMENT
# =========================================================

def extract_required_experience(job_description):
    """
    Detect minimum required experience from a job description.

    Supported examples:
    - Minimum 2 years
    - Minimum 2 years of experience
    - At least 2 years
    - 2+ years
    - 2-4 years
    - 2 – 4 years
    - 2 to 4 years
    - 2 years of experience
    - Experience of 2 years
    - Experience: 2 years
    - 2 yrs experience
    """

    text = str(job_description).lower()

    # Normalize spacing / dash variants
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    patterns = [

        # Minimum 2 years / Minimum 2 years of experience
        r"minimum\s+(?:of\s+)?(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",

        # At least 2 years
        r"at\s+least\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",

        # 2+ years
        r"(\d+(?:\.\d+)?)\+\s*(?:years?|yrs?)",

        # 2-4 years
        r"(\d+(?:\.\d+)?)\s*-\s*\d+(?:\.\d+)?\s*(?:years?|yrs?)",

        # 2 to 4 years
        r"(\d+(?:\.\d+)?)\s+to\s+\d+(?:\.\d+)?\s*(?:years?|yrs?)",

        # 2 years of experience
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s+of\s+(?:relevant\s+)?experience",

        # 2 years experience
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s+(?:relevant\s+)?experience",

        # Experience of 2 years
        r"experience\s+of\s+(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",

        # Experience: 2 years
        r"experience\s*:\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)"
    ]

    matches = []

    for pattern in patterns:
        for match in re.findall(pattern, text, flags=re.IGNORECASE):
            try:
                matches.append(float(match))
            except (TypeError, ValueError):
                pass

    if matches:
        # For ranges like 2-4, regex captures the minimum (2),
        # which is exactly what we want.
        return min(matches)

    return 0.0