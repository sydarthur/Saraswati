import json
import sys
import logging
from typing import List

try:
    import yaml  # type: ignore
except ImportError:
    import json as yaml  # type: ignore

from utils.s2_client import search_papers
from utils.filters import filter_by_journal, filter_by_year_range

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def load_config(path: str) -> dict:
    logging.info(f"Loading config from {path}")
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    logging.info("Config loaded successfully")
    return cfg

def query_from_config(cfg: dict) -> List[dict]:
    query = cfg.get("query", "")
    max_results = cfg.get("max_results", 100)
    fields = cfg.get("fields")
    logging.info(f"Querying Semantic Scholar with query: {query}, max_results: {max_results}, fields: {fields}")

    papers = search_papers(query, fields=fields, max_results=max_results)
    logging.info(f"Retrieved {len(papers)} papers from Semantic Scholar")

    journals = cfg.get("journals")
    start_year = cfg.get("start_year")
    end_year = cfg.get("end_year")

    if journals:
        before = len(papers)
        papers = filter_by_journal(papers, journals)
        logging.info(f"Filtered by journals {journals}: {before} -> {len(papers)} papers")

    if start_year is not None or end_year is not None:
        before = len(papers)
        papers = filter_by_year_range(papers, start_year, end_year)
        logging.info(f"Filtered by year range {start_year}-{end_year}: {before} -> {len(papers)} papers")
    else:
        logging.info("No year range filter applied.")

    return papers

def main(config_path: str) -> List[dict]:
    cfg = load_config(config_path)
    logging.info("Starting query from config")
    results = query_from_config(cfg)
    logging.info(f"Query complete. {len(results)} papers after filtering.")
    return results

if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else "../config/search_config.yaml"
    logging.info("Starting query_articles script")
    results = main(config_file)
    print(json.dumps(results, indent=2))
    logging.info("Script finished")