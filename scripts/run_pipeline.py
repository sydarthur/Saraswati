"""Run the search pipeline and save results to CSV."""

import csv
import os
import sys
from typing import List, Dict

from scripts.query_articles import main as run_query


def save_csv(rows: List[Dict], path: str) -> None:
    if not rows:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = sorted(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k) for k in fieldnames})


def main(config_path: str, output_csv: str) -> None:
    papers = run_query(config_path)
    save_csv(papers, output_csv)


if __name__ == "__main__":
    cfg = sys.argv[1] if len(sys.argv) > 1 else "config/search_config.yaml"
    out = sys.argv[2] if len(sys.argv) > 2 else "data/results.csv"
    main(cfg, out)
