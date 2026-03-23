"""
Shared utility functions for the replication of
"No Interest: The Marginalization of Women in Academic Finance"
(Fine, Yadav & Murawski, 2025)
"""

import re
import pandas as pd


def reconstruct_abstract(inverted_index: dict) -> str | None:
    """Reconstruct abstract text from OpenAlex inverted index format."""
    if not inverted_index:
        return None
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(w for _, w in word_positions)


def extract_first_name(display_name: str) -> str | None:
    """Extract the first usable name from an author's display name."""
    if not display_name:
        return None
    parts = display_name.strip().split()
    if not parts:
        return None
    first = parts[0]
    # Skip single-letter initials (e.g., "J." or "J")
    if len(first) <= 2 or (len(first) == 2 and first.endswith(".")):
        if len(parts) > 2:
            return parts[1]
        return first
    return first


# Sex/gender keyword patterns (word-boundary aware)
GENDER_KEYWORDS = [
    r"\bgender\b",
    r"\bsex\b",
    r"\bfemale\b",
    r"\bmale\b",
    r"\bwoman\b",
    r"\bwomen\b",
    r"\bgirl\b",
    r"\bboy\b",
    r"\bmasculin",
    r"\bfeminin",
    r"\bsexism\b",
    r"\bmisogyn",
    r"\bpatriarch",
    r"\bglass ceiling\b",
    r"\bgender gap\b",
    r"\bgender bias\b",
    r"\bgender diversity\b",
    r"\bgender inequalit",
    r"\bgender discriminat",
    r"\bgender differenc",
    r"\bsex differenc",
    r"\bgender pay gap\b",
    r"\bwage gap\b",
    r"\bfemale ceo\b",
    r"\bfemale director\b",
    r"\bboard diversity\b",
    r"\bwomen in finance\b",
    r"\bfemale representation\b",
]

GENDER_PATTERN = re.compile("|".join(GENDER_KEYWORDS), re.IGNORECASE)


def has_gender_content(text: str) -> bool:
    """Check if text contains sex/gender-related keywords."""
    if not text:
        return False
    return bool(GENDER_PATTERN.search(text))


def classify_gender_article(abstract: str) -> str:
    """
    Heuristic classification of sex/gender articles into:
    - 'gender_mechanisms': structural/systemic gender dynamics
    - 'sex_differences_catalogue': documenting behavioral differences
    - 'instrumental': gender as predictor of financial outcomes (default)
    """
    if not abstract:
        return "instrumental"
    text = abstract.lower()

    gm_keywords = [
        "mechanism", "structural", "systemic", "patriach", "glass ceiling",
        "discrimination", "bias", "inequality", "marginali", "barrier",
        "stereotype", "prejudice", "exclusion", "segregat", "harassment",
    ]
    csd_keywords = [
        "difference between", "gender difference", "sex difference",
        "comparison", "compare", "versus", "gap between",
        "men and women differ", "women and men differ",
    ]

    if any(k in text for k in gm_keywords):
        return "gender_mechanisms"
    elif any(k in text for k in csd_keywords):
        return "sex_differences_catalogue"
    else:
        return "instrumental"


# Data paths
DATA_DIR = "data"
RAW_DIR = f"{DATA_DIR}/raw"
PROCESSED_DIR = f"{DATA_DIR}/processed"
EXTERNAL_DIR = f"{DATA_DIR}/external"
FIGURES_DIR = "figures"
