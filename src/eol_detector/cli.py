from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .engine import assess_inventory, posture_score
from .io import load_csv, render_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess synthetic or exported asset inventory for end-of-life exposure.")
    parser.add_argument("inventory", help="CSV inventory path")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date (YYYY-MM-DD)")
    parser.add_argument("--output", help="Optional Markdown report path")
    args = parser.parse_args()

    as_of = date.fromisoformat(args.as_of)
    assets = load_csv(args.inventory)
    findings = assess_inventory(assets, as_of)
    score = posture_score(assets, findings)
    report = render_markdown(assets, findings, as_of, score)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
