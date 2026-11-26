"""Novelty: does the insight say something the organization doesn't know?

Each insight is compared with a "known pattern baseline" (prior reports,
documented seasonality, domain common knowledge). Novelty is one minus the
highest similarity to any known pattern, using TF-IDF cosine similarity so the
method needs no external model and is fully reproducible.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Sequence

_STOP = set(
    "a an and are as at be by for from has in is it its of on or that the to was were "
    "will with this than more less vs per our we".split()
)


def _tokens(text: str) -> list[str]:
    # Truncation stemming (first 5 characters) so "submit"/"submission" and
    # "faster"/"fast" match without pulling in an NLP dependency.
    return [t[:5] for t in re.findall(r"[a-z0-9%]+", text.lower()) if t not in _STOP]


def _tfidf(docs: list[list[str]]) -> list[dict[str, float]]:
    df = Counter(t for d in docs for t in set(d))
    n = len(docs)
    vecs = []
    for d in docs:
        tf = Counter(d)
        vecs.append({t: (c / len(d)) * (math.log((1 + n) / (1 + df[t])) + 1) for t, c in tf.items()} if d else {})
    return vecs


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    dot = sum(v * b.get(t, 0.0) for t, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def novelty_scores(insights: Sequence[str], known_patterns: Sequence[str]) -> list[dict]:
    """Return novelty (0-1) and the closest known pattern for each insight."""
    if not known_patterns:
        return [{"novelty": 1.0, "closest_known": None, "similarity": 0.0} for _ in insights]
    docs = [_tokens(t) for t in list(insights) + list(known_patterns)]
    vecs = _tfidf(docs)
    ins_vecs, known_vecs = vecs[: len(insights)], vecs[len(insights) :]
    results = []
    for v in ins_vecs:
        sims = [_cosine(v, k) for k in known_vecs]
        best = max(range(len(sims)), key=sims.__getitem__)
        results.append(
            {
                "novelty": round(1 - sims[best], 3),
                "closest_known": known_patterns[best],
                "similarity": round(sims[best], 3),
            }
        )
    return results
