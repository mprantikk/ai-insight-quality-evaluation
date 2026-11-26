"""Reference implementation of the Insight Quality Evaluation (IQE) Framework.

The framework scores an AI-generated insight on four dimensions that are kept
separate on purpose (the paper's "non-collapsibility" principle):

    statistical validity  - computed (Benjamini-Hochberg FDR control)
    novelty               - computed (distance from a known-pattern baseline)
    contextual relevance  - expert panel rating, reliability-checked (ICC)
    actionability         - expert panel rating, reliability-checked (ICC)
"""

from .validity import benjamini_hochberg, statistical_validity
from .novelty import novelty_scores
from .panel import icc_2_1, panel_scores
from .profile import IQEProfile, evaluate

__all__ = [
    "benjamini_hochberg",
    "statistical_validity",
    "novelty_scores",
    "icc_2_1",
    "panel_scores",
    "IQEProfile",
    "evaluate",
]
__version__ = "0.1.0"
