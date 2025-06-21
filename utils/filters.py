"""Utility functions for filtering Semantic Scholar papers."""
from typing import Iterable, List, Optional


def filter_by_journal(papers: List[dict], journals: Iterable[str]) -> List[dict]:
    """Return papers whose journal name is in the provided list."""
    journals_set = {j.lower() for j in journals}
    filtered = []
    for paper in papers:
        journal = paper.get("journal", {}) or {}
        name = journal.get("name", "").lower()
        if name in journals_set:
            filtered.append(paper)
    return filtered


def filter_by_year_range(
    papers: List[dict], start_year: Optional[int] = None, end_year: Optional[int] = None
) -> List[dict]:
    """Filter papers published between start_year and end_year (inclusive)."""
    filtered = []
    for paper in papers:
        year = paper.get("year")
        if year is None:
            continue
        if start_year is not None and year < start_year:
            continue
        if end_year is not None and year > end_year:
            continue
        filtered.append(paper)
    return filtered
