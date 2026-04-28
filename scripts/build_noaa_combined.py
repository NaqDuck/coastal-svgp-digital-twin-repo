#!/usr/bin/env python3
"""Rebuild generated NOAA_all_surveys_combined.csv files from per-tile CSVs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CONFIG = {
    "bass": {
        "input_dir": Path("Datasets") / "Extracted" / "Bass CSV",
        "output": Path("Datasets") / "Extracted" / "Bass CSV" / "NOAA_all_surveys_combined.csv",
    },
    "bicentennial": {
        "input_dir": Path("Datasets") / "Extracted" / "Bicent CSV",
        "output": Path("Datasets") / "Extracted" / "Bicent CSV" / "NOAA_all_surveys_combined.csv",
    },
}


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "Codes").is_dir() and (candidate / "Datasets").is_dir():
            return candidate
    raise FileNotFoundError("Could not find project root containing Codes and Datasets")


def point_csvs(input_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in input_dir.glob("*_points.csv")
        if path.name != "NOAA_all_surveys_combined.csv"
    )


def build_combined(beach: str, root: Path) -> None:
    cfg = CONFIG[beach]
    input_dir = root / cfg["input_dir"]
    output = root / cfg["output"]
    files = point_csvs(input_dir)

    if not files:
        raise FileNotFoundError(f"No per-survey *_points.csv files found in {input_dir}")

    output.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    expected_header: list[str] | None = None

    with output.open("w", newline="", encoding="utf-8") as out_f:
        writer: csv.DictWriter[str] | None = None

        for path in files:
            with path.open(newline="", encoding="utf-8") as in_f:
                reader = csv.DictReader(in_f)
                if reader.fieldnames is None:
                    raise ValueError(f"Missing CSV header: {path}")

                if expected_header is None:
                    expected_header = list(reader.fieldnames)
                    writer = csv.DictWriter(out_f, fieldnames=expected_header)
                    writer.writeheader()
                elif list(reader.fieldnames) != expected_header:
                    raise ValueError(f"Header mismatch in {path}")

                assert writer is not None
                for row in reader:
                    writer.writerow(row)
                    total_rows += 1

    print(f"{beach}: wrote {total_rows:,} rows -> {output.relative_to(root)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--beach",
        choices=["bass", "bicentennial", "all"],
        default="all",
        help="Which combined NOAA CSV to rebuild.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = find_project_root()
    beaches = CONFIG if args.beach == "all" else [args.beach]
    for beach in beaches:
        build_combined(beach, root)


if __name__ == "__main__":
    main()

