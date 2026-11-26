"""Score a batch of AI-generated insights with the IQE Framework.

    python evaluate_insights.py                  # runs the bundled example
    python evaluate_insights.py --out report.csv # also saves the profiles
"""

import argparse
import json
from pathlib import Path

import pandas as pd

from iqe import evaluate

HERE = Path(__file__).parent / "examples"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--insights", default=HERE / "insights.csv")
    ap.add_argument("--known", default=HERE / "known_patterns.txt")
    ap.add_argument("--ratings", default=HERE / "ratings.json")
    ap.add_argument("--out")
    args = ap.parse_args()

    insights = pd.read_csv(args.insights)
    known = [l.strip() for l in Path(args.known).read_text().splitlines() if l.strip()]
    ratings = json.loads(Path(args.ratings).read_text())

    profiles, reliability = evaluate(insights, known, ratings["relevance"], ratings["actionability"])

    print("Panel reliability (ICC(2,1), threshold 0.70):")
    for dim in ("relevance", "actionability"):
        ok = "reliable" if reliability[f"{dim}_reliable"] else "NOT reliable: collect more ratings"
        print(f"  {dim:<14} {reliability[f'{dim}_icc']:.2f}  {ok}")
    print()
    cols = ["insight_id", "validity", "novelty", "relevance", "actionability", "verdict"]
    print(profiles[cols].to_string(index=False))
    if args.out:
        profiles.to_csv(args.out, index=False)
        print(f"\nSaved {args.out}")


if __name__ == "__main__":
    main()
