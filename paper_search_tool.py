# File: paper_search_tool.py

import time
import logging
import requests
from typing import List, Dict

logging.basicConfig(level=logging.INFO)

def search_papers(
    topic: str,
    year: int,
    comparator: str = "after",
    min_citations: int = 0
) -> List[Dict]:
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": f'"{topic}"',
        "limit": 20,
        "fields": "title,authors,year,citationCount,url"
    }

# Custom Rate Limiter
    for attempt in range(5):
        try:
            response = requests.get(url, params=params)
            if response.status_code == 429:
                wait = 5 * (attempt + 1)
                logging.warning(f"Rate limited. Retrying in {wait}s...")
                time.sleep(wait)
                continue
            response.raise_for_status()
            break
        except Exception as e:
            logging.error(f"Error: {e}")
            return [{"error": str(e)}]

    papers = []
    for paper in response.json().get("data", []):
        citations = paper.get("citationCount", 0)
        pub_year = paper.get("year", 0)
        if citations >= min_citations and (
            (comparator == "after" and pub_year > year) or
            (comparator == "before" and pub_year < year) or
            (comparator == "in" and pub_year == year)
        ):
            papers.append({
                "title": paper.get("title"),
                "authors": ", ".join(a["name"] for a in paper.get("authors", [])),
                "year": pub_year,
                "citations": citations,
                "url": paper.get("url")
            })

    return papers
