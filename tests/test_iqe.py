import pandas as pd
import pytest

from iqe import benjamini_hochberg, evaluate, icc_2_1, novelty_scores, statistical_validity


# ---- statistical validity -------------------------------------------------

def test_bh_matches_hand_calculation():
    # p sorted: 0.01, 0.02, 0.03, 0.04 with n=4 -> 0.04, 0.04, 0.04, 0.04
    assert benjamini_hochberg([0.01, 0.04, 0.03, 0.02]) == pytest.approx([0.04] * 4)


def test_bh_is_monotone_and_capped():
    q = benjamini_hochberg([0.001, 0.2, 0.9, 0.05])
    assert all(0 <= x <= 1 for x in q)
    order = sorted(range(4), key=[0.001, 0.2, 0.9, 0.05].__getitem__)
    assert [q[i] for i in order] == sorted(q)


def test_bh_rejects_invalid_p():
    with pytest.raises(ValueError):
        benjamini_hochberg([0.5, 1.5])


def test_validity_needs_significance_and_effect():
    res = statistical_validity([0.001, 0.001, 0.6], [0.5, 0.05, 0.9])
    assert res[0]["validity"] > 0.5
    assert res[1]["validity"] == 0  # significant but trivial effect
    assert res[2]["validity"] == 0  # large effect but noise


# ---- novelty --------------------------------------------------------------

def test_restating_known_pattern_is_not_novel():
    known = ["Revenue peaks in December because of holiday demand"]
    res = novelty_scores(
        ["Revenue is higher in December due to holiday demand",
         "Telehealth denials are double in-person denials"],
        known,
    )
    assert res[0]["novelty"] < 0.6
    assert res[1]["novelty"] > 0.9


def test_no_baseline_means_fully_novel():
    assert novelty_scores(["anything"], [])[0]["novelty"] == 1.0


# ---- panel reliability ----------------------------------------------------

def test_icc_matches_shrout_fleiss_1979():
    # Classic 6 targets x 4 judges example; published ICC(2,1) = 0.29
    data = [[9, 2, 5, 8], [6, 1, 3, 2], [8, 4, 6, 8], [7, 1, 2, 6], [10, 5, 6, 9], [6, 2, 4, 7]]
    assert icc_2_1(data) == pytest.approx(0.29, abs=0.005)


def test_perfect_agreement_gives_icc_one():
    assert icc_2_1([[1, 1], [3, 3], [5, 5]]) == pytest.approx(1.0)


# ---- end to end -----------------------------------------------------------

def test_evaluate_keeps_dimensions_separate_and_flags_weakness():
    insights = pd.DataFrame(
        {"id": ["A", "B"],
         "text": ["Denials rose 30% after a payer rule change", "Sales are higher in December"],
         "p_value": [0.001, 0.001], "effect_size": [0.7, 0.9]}
    )
    rel = [[5, 5, 4], [2, 1, 2]]
    act = [[5, 4, 5], [1, 1, 2]]
    profiles, reliability = evaluate(insights, ["Sales are higher in December"], rel, act)
    assert {"validity", "novelty", "relevance", "actionability"} <= set(profiles.columns)
    assert "score" not in profiles.columns  # no collapsed single score, by design
    assert profiles.loc[0, "verdict"] == "surface on dashboard"
    assert profiles.loc[1, "verdict"].startswith("hold")
    assert reliability["relevance_reliable"]
