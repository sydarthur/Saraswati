import logging
from typing import Iterable, List, Optional

def normalize(s: Optional[str]) -> str:
    """Normalize string to lowercase and strip whitespace."""
    return s.lower().strip() if isinstance(s, str) else ""

def filter_by_journal(papers: List[dict], journals: Iterable[str]) -> List[dict]:
    """Return papers whose journal name matches the provided list (case-insensitive)."""
    journals_set = {normalize(j) for j in journals}
    seen_venues = set()
    filtered = []

    for paper in papers:
        # Try Semantic Scholar Graph API format first
        journal_name = normalize(paper.get("journal", {}).get("name"))
        if not journal_name:
            journal_name = normalize(paper.get("venue"))

        seen_venues.add(journal_name)

        if journal_name in journals_set:
            filtered.append(paper)

    print("\n🧾 Unique venues returned in this query:")
    for venue in sorted(seen_venues):
        print("-", venue)

    return filtered


def filter_by_year_range(
    papers: List[dict],
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
) -> List[dict]:
    logging.info(f"Filtering {len(papers)} papers by year range: {start_year} - {end_year}")
    filtered = []
    for paper in papers:
        year = paper.get("year")
        if not isinstance(year, int):
            continue
        if start_year is not None and year < start_year:
            continue
        if end_year is not None and year > end_year:
            continue
        filtered.append(paper)
    logging.info(f"Year range filter result: {len(filtered)} papers matched")
    return filtered