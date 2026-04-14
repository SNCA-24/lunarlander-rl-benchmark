#!/usr/bin/env python3
"""Regenerate benchmark plots from preserved CSV artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lunarlander_benchmark.plotting import generate_all_plots


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results-dir",
        default=str(ROOT / "results" / "final_benchmark"),
        help="Directory containing preserved benchmark CSV artifacts.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "results" / "reproduced_plots"),
        help="Directory to write regenerated plots. Defaults to a separate folder to avoid overwriting preserved artifacts.",
    )
    parser.add_argument(
        "--allow-overwrite",
        action="store_true",
        help="Allow writing into a non-empty output directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generated = generate_all_plots(args.results_dir, args.output_dir, allow_overwrite=args.allow_overwrite)
    print(f"Generated {len(generated)} plots in {Path(args.output_dir).resolve()}")
    for path in generated:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
