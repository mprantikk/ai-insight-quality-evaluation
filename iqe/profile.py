"""Combine the four dimensions into a profile, deliberately without one total.

The paper argues that a single "trust score" hides exactly the trade-offs a
decision-maker needs to see (a valid but obvious insight, a novel but
unactionable one). So `evaluate` returns the four scores side by side plus a
plain-language verdict that names the weakest dimension.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd

from .novelty import novelty_scores
from .panel import panel_scores
from .validity import statistical_validity

PASS_LEVEL = 0.5


@dataclass
class IQEProfile:
    insight_id: str
    text: str
    validity: float
    novelty: float
    relevance: float
    actionability: float
    verdict: str


def _verdict(dims: dict[str, float]) -> str:
    if dims["validity"] == 0:
        return "reject: not statistically supported"
    weak = [name for name, v in dims.items() if v < PASS_LEVEL]
    if not weak:
        return "surface on dashboard"
    return "hold: weak on " + ", ".join(weak)


def evaluate(
    insights: pd.DataFrame,
    known_patterns: list[str],
    relevance_ratings: list[list[float]],
    actionability_ratings: list[list[float]],
) -> tuple[pd.DataFrame, dict]:
    """Score every insight. `insights` needs columns id, text, p_value, effect_size."""
    validity = statistical_validity(insights.p_value.tolist(), insights.effect_size.tolist())
    novelty = novelty_scores(insights.text.tolist(), known_patterns)
    relevance = panel_scores(relevance_ratings)
    action = panel_scores(actionability_ratings)

    profiles = []
    for i, row in enumerate(insights.itertuples()):
        dims = {
            "validity": validity[i]["validity"],
            "novelty": novelty[i]["novelty"],
            "relevance": relevance["scores"][i],
            "actionability": action["scores"][i],
        }
        profiles.append(IQEProfile(row.id, row.text, **dims, verdict=_verdict(dims)))

    reliability = {
        "relevance_icc": relevance["icc"],
        "relevance_reliable": relevance["reliable"],
        "actionability_icc": action["icc"],
        "actionability_reliable": action["reliable"],
    }
    return pd.DataFrame([asdict(p) for p in profiles]), reliability
