"""Contextual relevance and actionability: expert panel ratings.

These two dimensions need human judgment. The framework requires the panel's
ratings to be reliable before they are used: ICC(2,1) >= 0.70 by default.
"""

from __future__ import annotations

from typing import Sequence

ICC_THRESHOLD = 0.70


def icc_2_1(ratings: Sequence[Sequence[float]]) -> float:
    """Intraclass correlation ICC(2,1): two-way random effects, absolute agreement.

    ratings[i][j] is rater j's score for item i. Shrout & Fleiss (1979).
    """
    n = len(ratings)
    if n < 2:
        raise ValueError("need at least 2 rated items")
    k = len(ratings[0])
    if k < 2 or any(len(r) != k for r in ratings):
        raise ValueError("every item needs the same number of raters (at least 2)")
    grand = sum(map(sum, ratings)) / (n * k)
    row_means = [sum(r) / k for r in ratings]
    col_means = [sum(ratings[i][j] for i in range(n)) / n for j in range(k)]
    ss_rows = k * sum((m - grand) ** 2 for m in row_means)
    ss_cols = n * sum((m - grand) ** 2 for m in col_means)
    ss_total = sum((x - grand) ** 2 for r in ratings for x in r)
    ss_err = ss_total - ss_rows - ss_cols
    msr = ss_rows / (n - 1)
    msc = ss_cols / (k - 1)
    mse = ss_err / ((n - 1) * (k - 1))
    denom = msr + (k - 1) * mse + k * (msc - mse) / n
    return (msr - mse) / denom if denom else 0.0


def panel_scores(ratings: Sequence[Sequence[float]], scale_max: int = 5) -> dict:
    """Average Likert ratings to 0-1 and report whether the panel is reliable."""
    icc = icc_2_1(ratings)
    scores = [round((sum(r) / len(r) - 1) / (scale_max - 1), 3) for r in ratings]
    return {"scores": scores, "icc": round(icc, 3), "reliable": icc >= ICC_THRESHOLD}
