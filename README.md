# Replication: "No Interest: The Marginalization of Women in Academic Finance"

An open-source replication of Fine, Yadav & Murawski (2025), *Feminist Economics*, using freely available data and tools in place of the original paid databases.

---

## Overview

This project replicates the key empirical findings of the paper, which analyzed 125,871 finance articles published between 1918 and 2020 to document the systematic marginalization of women in academic finance. The original study used the Dimensions database and a commercial Gender API; this replication uses **OpenAlex** and **gender-guesser** instead.

### Key Findings (Replication vs. Paper)

| Metric | Paper | This Replication |
|--------|-------|-----------------|
| Total articles collected | 125,871 | ~100K+ |
| Male authorship | 83.3% | ~83% |
| Female authorship | 16.7% | ~17% |
| Articles with sex/gender content | 0.78% (433/55,210) | ~1.04% |
| Spearman ρ (female authorship vs. gender content) | 0.45 | 0.418 (p = 0.0003) |
| LDA topics | 21 | 21 |
| Inequality topic present | No | No (confirmed) |

---

## Project Structure

```
Project/
├── README.md
├── requirements.txt
├── utils.py                              # Shared helper functions
├── methodology.txt                       # Full written methodology
│
├── 01_journal_list_and_rankings.ipynb    # ABDC journal list + OpenAlex matching
├── 02_data_collection_openalex.ipynb     # Fetch articles + authorships from OpenAlex
├── 03_gender_inference.ipynb             # Name-based gender inference
├── 04_topic_modeling.ipynb               # LDA topic modeling (K=21)
├── 05_sex_gender_content_analysis.ipynb  # Keyword search + category classification
├── 06_statistical_analysis_and_figures.ipynb  # Stats, regressions, all figures
│
├── data/
│   ├── raw/
│   │   ├── journals/                     # Per-journal checkpoint parquets
│   │   ├── articles.parquet              # All articles
│   │   └── authorships.parquet           # All authorships
│   └── processed/
│       ├── journal_list.csv              # 90 journals with ABDC ranks + OpenAlex IDs
│       ├── articles_gendered.parquet     # Articles with gender metrics
│       ├── authorships_gendered.parquet  # Authorships with inferred gender
│       ├── articles_with_topics.parquet  # Articles with LDA topic assignments
│       ├── articles_gender_content.parquet  # Articles flagged for gender content
│       └── gender_articles_for_review.csv   # Flagged articles for manual review
│
└── figures/
    ├── replication_comparison.png        # Paper vs. replication comparison (6 panels)
    ├── female_authorship_over_time.png
    ├── female_authorship_by_rank.png
    ├── gender_content_over_time.png
    ├── topic_gender_heatmap.png
    ├── coherence_scores.png
    ├── topic_wordclouds.png
    └── journal_scatter.png
```

---

## Setup

### 1. Create and activate a conda environment

```bash
conda create -n my_env python=3.10
conda activate my_env
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Run the notebooks in order

```bash
jupyter notebook
```

Open and run each notebook sequentially (01 → 06).

---

## Notebooks

### `01_journal_list_and_rankings.ipynb`
Defines 90 finance journals from the ABDC Quality List (Field of Research 3502: Banking, Finance and Investment), searches OpenAlex for their source IDs, and fuzzy-matches unresolved entries. Saves `data/processed/journal_list.csv`.

### `02_data_collection_openalex.ipynb`
Paginates the OpenAlex Works API for each journal (type = article, years 1918–2020). Reconstructs abstracts from OpenAlex's inverted index format. Checkpoints per journal so the 2–4 hour run can be interrupted and resumed. Saves `data/raw/articles.parquet` and `data/raw/authorships.parquet`.

### `03_gender_inference.ipynb`
Extracts first names from author display names and runs `gender-guesser` on all unique names. Maps raw categories to male / female / unclassified. Computes article-level metrics: `pct_female`, `n_male`, `n_female`, `first_author_gender`, `last_author_gender`. Saves gendered parquets.

### `04_topic_modeling.ipynb`
Filters to abstracts from 1988–2020 (~47K documents). Preprocesses with spaCy (lemmatization, stopword removal). Trains a Gensim LDA model with K=21 topics (`random_state=42`). Computes coherence sweep (K=5 to 40) to validate K=21. Generates word clouds and assigns dominant topics to each article.

### `05_sex_gender_content_analysis.ipynb`
Applies a word-boundary regex pattern over 20 gender-related keywords to flag articles containing sex/gender analysis. Classifies flagged articles into three categories using a heuristic keyword classifier:
- **Instrumental (INS):** Gender as a predictor of financial outcomes
- **Catalogues of Sex Differences (CSD):** Documenting behavioral differences
- **Gender Mechanisms (GM):** Structural/systemic gender dynamics

> **Note:** The paper's original classification was done by hand-coding. The heuristic classifier here is an approximation. For a full replication, manually review `data/processed/gender_articles_for_review.csv`.

### `06_statistical_analysis_and_figures.ipynb`
Produces all main results: overall gender proportions, trends over time, breakdown by journal rank and country, topic × gender heatmap, gender content prevalence, Spearman correlation, and logistic regression. Generates the 6-panel replication comparison figure.

---

## Tools and Differences from the Original

| Original | This Replication | Notes |
|----------|-----------------|-------|
| Dimensions (paid) | OpenAlex (free) | Article counts may differ slightly |
| Gender API (paid) | gender-guesser (open-source) | Lower accuracy for non-Western names |
| Bayesian logistic regression (Stan) | MLE via scipy | Same model specification; frequentist estimates |
| Hand-coded gender content categories | Heuristic keyword classifier | Manual review of flagged articles recommended |
| Exact abstract text | Reconstructed from inverted index | Minor whitespace differences possible |

---

## Manual Review Required

The file `data/processed/gender_articles_for_review.csv` contains all articles flagged as having sex/gender content (~496 articles). For a full replication of the paper's INS/CSD/GM category breakdown, these should be reviewed and hand-coded. The paper's split was approximately 51% Instrumental, 32% Catalogues of Sex Differences, and 17% Gender Mechanisms.

---

## Approximate Runtimes

| Notebook | Runtime |
|----------|---------|
| 01 | 5–10 minutes |
| 02 | 2–4 hours |
| 03 | 5–10 minutes |
| 04 | 30–60 minutes |
| 05 | < 5 minutes |
| 06 | 5–15 minutes |

---

## Reference

Fine, C., Yadav, K., & Murawski, C. (2025). No Interest: The Marginalization of Women in Academic Finance. *Feminist Economics*, 31(1), 1–36.
