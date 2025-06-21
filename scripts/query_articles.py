"""Query Semantic Scholar and filter results based on YAML configuration."""

import json
import sys
from typing import List

try:
    import yaml  # type: ignore
except ImportError:  # fall back to simple parser for minimal YAML (subset of JSON)
    import json as yaml  # type: ignore

from utils.s2_client import search_papers
from utils.filters import filter_by_journal, filter_by_year_range


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def query_from_config(cfg: dict) -> List[dict]:
    query = cfg.get("query", "")
    max_results = cfg.get("max_results", 100)
    fields = cfg.get("fields")

    papers = search_papers(query, fields=fields, max_results=max_results)

    filters = cfg.get("filters", {}) or {}
    journals = filters.get("journals")
    start_year = filters.get("start_year")
    end_year = filters.get("end_year")

    if journals:
        papers = filter_by_journal(papers, journals)
    papers = filter_by_year_range(papers, start_year, end_year)

    return papers


def main(config_path: str) -> List[dict]:
    cfg = load_config(config_path)
    return query_from_config(cfg)


if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config/search_config.yaml"
    results = main(config_file)
    print(json.dumps(results, indent=2))
