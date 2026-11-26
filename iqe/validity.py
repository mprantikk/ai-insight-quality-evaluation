"""Statistical validity: guard against the multiple-comparisons problem.

Automated insight engines test thousands of slices, so some "patterns" are
noise. Benjamini-Hochberg controls the false discovery rate across the whole
candidate pool rather than judging each p-value alone.
"""

from __future__ import annotations

from typing import Sequence


def benjamini_hochberg(p_values: Sequence[float], alpha: float = 0.05) -> list[float]:
    """Return BH-adjusted p-values (q-values), in the original order."""
    n = len(p_values)
    if n == 0:
        return []
    if any(not 0.0 <= p <= 1.0 for p in p_values):
        raise ValueError("p-values must be between 0 and 1")
    order = sorted(range(n), key=lambda i: p_values[i])
    adjusted = [0.0] * n
    running_min = 1.0
    for rank in range(n, 0, -1):  # walk from largest p to smallest
        i = order[rank - 1]
        running_min = min(running_min, p_values[i] * n / rank)
        adjusted[i] = running_min
    return adjusted


def statistical_validity(
    p_values: Sequence[float],
    effect_sizes: Sequence[float],
    alpha: float = 0.05,
    min_effect: float = 0.2,
) -> list[dict]:
    """Score each insight 0-1 on statistical validity.

    An insight must survive FDR control *and* show a non-trivial effect size
    (|d| >= min_effect, Cohen's small-effect threshold by default). The score
    rewards a lower q-value and a larger effect; insights that fail either gate
    score 0.
    """
    if len(p_values) != len(effect_sizes):
        raise ValueError("p_values and effect_sizes must be the same length")
    q_values = benjamini_hochberg(p_values, alpha)
    results = []
    for q, d in zip(q_values, effect_sizes):
        significant = q <= alpha
        meaningful = abs(d) >= min_effect
        if significant and meaningful:
            # 0.5 for passing both gates, up to +0.25 each for strength
            q_strength = 1 - q / alpha
            d_strength = min(abs(d), 0.8) / 0.8
            score = 0.5 + 0.25 * q_strength + 0.25 * d_strength
        else:
            score = 0.0
        results.append(
            {
                "q_value": round(q, 4),
                "significant": significant,
                "meaningful_effect": meaningful,
                "validity": round(score, 3),
            }
        )
    return results
