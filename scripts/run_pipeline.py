import csv
import os
import sys
import logging
from typing import List, Dict

from scripts.query_articles import main as run_query

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def save_csv(rows: List[Dict], path: str) -> None:
    if not rows:
        logging.warning("No rows to save. Skipping CSV write.")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = sorted(rows[0].keys())
    logging.info(f"Saving {len(rows)} rows to CSV at {path}")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k) for k in fieldnames})
    logging.info("CSV save complete.")

def main(config_path: str, output_csv: str) -> None:
    import yaml
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    query = cfg.get("query", "")
    logging.info(f"Running search pipeline with config: {config_path}")
    logging.info(f"Query: {query}")
    papers = run_query(config_path)
    logging.info(f"Retrieved {len(papers)} papers from query.")
    save_csv(papers, output_csv)
    logging.info("Pipeline finished successfully.")

if __name__ == "__main__":
    cfg = sys.argv[1] if len(sys.argv) > 1 else "../config/search_config.yaml"
    out = sys.argv[2] if len(sys.argv) > 2 else "../data/results.csv"
    logging.info("Starting pipeline script.")
    main(cfg, out)
    logging.info("Script execution complete.")