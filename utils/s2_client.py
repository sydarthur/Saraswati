# Utilities for interacting with the Semantic Scholar API
import json
import time
from typing import Iterable, List, Optional
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://api.semanticscholar.org/graph/v1"


def _request(path: str, params: dict, retries: int = 3, backoff: float = 1.0):
    """Internal helper to send GET requests with basic retries."""
    url = f"{BASE_URL}{path}?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"HTTP {resp.status}")
                data = resp.read()
                return json.loads(data.decode("utf-8"))
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(backoff * (2 ** attempt))


def search_papers(
    query: str,
    fields: Optional[Iterable[str]] = None,
    *,
    max_results: int = 100,
    retries: int = 3,
) -> List[dict]:
    """Search papers via Semantic Scholar."""

    results: List[dict] = []
    offset = 0
    page_limit = 100  # API allows up to 100 per page

    while len(results) < max_results:
        params = {
            "query": query,
            "offset": offset,
            "limit": min(page_limit, max_results - len(results)),
        }
        if fields:
            params["fields"] = ",".join(fields)

        resp = _request("/paper/search", params, retries)
        papers = resp.get("data", [])
        results.extend(papers)
        offset += len(papers)

        total = resp.get("total", 0)
        if offset >= total or not papers:
            break

    return results
