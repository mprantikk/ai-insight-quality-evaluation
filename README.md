# Beyond the Dashboard: A Conceptual Framework for Evaluating Insight Quality in AI-Augmented BI Systems

[![CI](https://github.com/mprantikk/ai-insight-quality-evaluation/actions/workflows/ci.yml/badge.svg)](https://github.com/mprantikk/ai-insight-quality-evaluation/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)

<p align="left">
  <a href="https://github.com/mprantikk/ai-insight-quality-evaluation/blob/main/Insight_Quality_Evaluation_Framework_Formatted.pdf">
    <img src="https://img.shields.io/badge/Read%20Full%20Paper-2E7D32?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Read PDF Online" />
  </a>
</p>

**Author:** Md. Masud Parvej (Independent Researcher)  
**Contact:** [mprantikk@gmail.com](mailto:mprantikk@gmail.com)

---

## 📌 Project Overview

The integration of artificial intelligence (AI) into business intelligence (BI) platforms has given rise to **augmented analytics**, enabling the automated detection, generation, and narration of data-driven insights with minimal human intervention. While this advancement promises scalable decision support, organizations still lack systematic criteria for evaluating whether these algorithmically generated insights are statistically sound, contextually relevant, genuinely novel, and actionable, rather than being spurious, redundant, or misleading.

This repository contains the formal manuscript for the **Insight Quality Evaluation (IQE) Framework**. The framework draws upon research in data mining interestingness, information systems success, and human-computer interaction to establish a structured approach for evaluating AI-generated insights before they are presented on strategic dashboards.

---

## 💡 Core Evaluation Dimensions

The IQE Framework evaluates AI-generated insights across four complementary dimensions:

1. **Statistical Validity:** Assesses whether a generated insight reflects a genuine and statistically robust pattern or results from false-positive inflation caused by exhaustive automated data mining (e.g., multiple comparisons or the "garden of forking paths" problem).

2. **Contextual Relevance:** Evaluates whether an insight aligns with current business objectives, operational priorities, and the decision-making needs of its intended users.

3. **Novelty:** Measures whether an insight provides information beyond existing domain knowledge, business intuition, or established organizational understanding.

4. **Actionability:** Determines whether an insight can be translated into a clear, practical, and feasible business action or operational decision.

---

## 🔬 Proposed Research Methodology

The accompanying manuscript proposes a rigorous mixed-methods validation strategy comprising three phases:

- **Phase 1 (Computational Evaluation):** Apply subspace search and association rule mining techniques to publicly available benchmark datasets (e.g., UCI, Kaggle, World Bank, WHO, and OECD) to compute measures of statistical validity and surprise.

- **Phase 2 (Expert Panel Validation):** Conduct structured evaluations with domain experts (*n* = 15–20 per domain) to assess contextual relevance, perceived actionability, and the faithfulness of Natural Language Generation (NLG) narratives against blinded statistical summaries.

- **Phase 3 (Moderator Analysis):** Perform multi-group analyses to investigate how **Task Complexity** and **Organizational Data Maturity** moderate the relationships among the proposed quality dimensions.

---

## 🧪 Reference Implementation

The `iqe/` package turns the framework into code you can run on a batch of AI-generated insights. It scores each insight on all four dimensions and, following the paper's non-collapsibility principle, **does not merge them into one "trust score"**. Instead it names the weakest dimension.

| Dimension | How it is measured |
|---|---|
| Statistical validity | Benjamini–Hochberg FDR control across the whole candidate pool, plus a minimum effect size |
| Novelty | TF-IDF cosine distance from a "known pattern baseline" (prior reports, documented seasonality) |
| Contextual relevance | Expert panel Likert ratings, accepted only if ICC(2,1) ≥ 0.70 |
| Actionability | Expert panel Likert ratings, accepted only if ICC(2,1) ≥ 0.70 |

```bash
pip install -r requirements.txt
python evaluate_insights.py
```

```
Panel reliability (ICC(2,1), threshold 0.70):
  relevance      0.85  reliable
  actionability  0.91  reliable

insight_id  validity  novelty  relevance  actionability  verdict
        I1     0.966    0.929      0.917          0.917  surface on dashboard
        I2     0.997    0.394      0.417          0.167  hold: weak on novelty, relevance, actionability
        I4     0.000    1.000      0.083          0.000  reject: not statistically supported
        ...
```

I2 ("revenue is higher in December") is statistically rock-solid but already known and not useful, which is exactly the kind of insight a single score would wrongly rank first. The example data in `examples/` is synthetic.

The ICC implementation is tested against the published Shrout & Fleiss (1979) example. The novelty measure is lexical by design (no external model, fully reproducible); swapping in sentence embeddings is a natural extension.

---

## 📄 Repository Structure

- `Insight_Quality_Evaluation_Framework_Formatted.pdf`: the manuscript
- `iqe/`: reference implementation (validity, novelty, panel reliability, profile)
- `evaluate_insights.py`: command-line runner
- `examples/`: synthetic insights, known-pattern baseline and panel ratings
- `tests/`: pytest suite, run in CI on Python 3.10 and 3.12

---

## 👥 Contribution & Collaboration

This research provides a conceptual foundation for evaluating AI-generated insights and is intended to encourage empirical validation and collaborative development.

If you are interested in developing automated scoring methods, implementing evaluation pipelines, or validating the framework using open-source tools in Python or R, feel free to open an issue or contact me via email.
