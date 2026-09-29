import re
from datetime import datetime


MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}


def extract_experience(text):
    text = str(text).lower()

    # =====================================================
    # 1. EXPLICIT EXPERIENCE STATEMENTS
    # =====================================================

    patterns = [
        r'(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience',
        r'(\d+(?:\.\d+)?)\+?\s*years?\s+experience',
        r'experience\s+of\s+(\d+(?:\.\d+)?)\+?\s*years?',
        r'over\s+(\d+(?:\.\d+)?)\s+years?',
        r'more\s+than\s+(\d+(?:\.\d+)?)\s+years?'
    ]

    explicit_years = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text
        )

        for match in matches:
            try:
                explicit_years.append(
                    float(match)
                )
            except ValueError:
                pass

    if explicit_years:
        return round(
            max(explicit_years),
            1
        )


    # =====================================================
    # 2. DATE-RANGE BASED EXPERIENCE
    #
    # Examples:
    # April 2024 - November 2024
    # April 2024 – November 2024
    # April 2024 to November 2024
    # May 2022 - Present
    # =====================================================

    month_names = "|".join(
        MONTHS.keys()
    )

    date_pattern = rf'''
        ({month_names})
        \s+
        (19\d{{2}}|20\d{{2}})
        \s*
        (?:to|-|–|—)
        \s*
        (
            present
            |
            current
            |
            ({month_names})
            \s+
            (19\d{{2}}|20\d{{2}})
        )
    '''

    matches = re.findall(
        date_pattern,
        text,
        flags=re.VERBOSE
    )

    intervals = []

    for match in matches:

        start_month_name = (
            match[0]
        )

        start_year = int(
            match[1]
        )

        end_value = (
            match[2]
        )

        start_month = MONTHS[
            start_month_name
        ]


        # Present / Current
        if end_value in [
            "present",
            "current"
        ]:

            now = datetime.now()

            end_year = now.year
            end_month = now.month

        else:

            end_month_name = (
                match[3]
            )

            end_year = int(
                match[4]
            )

            end_month = MONTHS[
                end_month_name
            ]


        start_index = (
            start_year * 12
            + start_month
        )

        end_index = (
            end_year * 12
            + end_month
        )


        if end_index >= start_index:

            intervals.append(
                (
                    start_index,
                    end_index
                )
            )


    if not intervals:
        return 0.0


    # =====================================================
    # 3. MERGE OVERLAPPING WORK PERIODS
    # =====================================================

    intervals.sort()

    merged = [
        intervals[0]
    ]

    for start, end in intervals[1:]:

        previous_start, previous_end = (
            merged[-1]
        )

        if start <= previous_end:

            merged[-1] = (
                previous_start,
                max(
                    previous_end,
                    end
                )
            )

        else:

            merged.append(
                (
                    start,
                    end
                )
            )


    # =====================================================
    # 4. TOTAL EXPERIENCE
    # =====================================================

    total_months = 0

    for start, end in merged:

        total_months += (
            end - start
        )


    years = (
        total_months / 12
    )

    return round(
        years,
        1
    )


# =========================================================
# EXPERIENCE MATCH SCORE
# =========================================================

def calculate_experience_score(
    experience_years,
    required_years=2
):
    """
    Calculate candidate experience alignment
    against the actual job requirement.

    Examples:

    Candidate = 0.6 years
    Required  = 2 years
    Score     = 30%

    Candidate = 1 year
    Required  = 2 years
    Score     = 50%

    Candidate = 2 years
    Required  = 2 years
    Score     = 100%

    Candidate = 3 years
    Required  = 2 years
    Score     = 100%
    """

    try:

        experience_years = float(
            experience_years
        )

        required_years = float(
            required_years
        )

    except (
        TypeError,
        ValueError
    ):

        return 0.0


    # No minimum experience required
    if required_years <= 0:

        return 100.0


    # No candidate experience detected
    if experience_years <= 0:

        return 0.0


    # Experience alignment
    score = (
        experience_years
        / required_years
    ) * 100


    # Cap score between 0 and 100
    score = min(
        max(
            score,
            0.0
        ),
        100.0
    )


    return round(
        score,
        2
    )