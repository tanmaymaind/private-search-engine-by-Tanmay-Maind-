"""Small checks for ranking: title matches and rare terms should win."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from search_engine import build_engine  # noqa: E402


def test_redis_query_ranks_redis_doc_first():
    engine = build_engine()
    results = engine.search("redis in-memory cache")
    assert results, "expected results for a redis query"
    assert "redis" in results[0]["title"].lower()


def test_search_query_ranks_search_doc_first():
    engine = build_engine()
    results = engine.search("inverted index TF-IDF ranking")
    assert results, "expected results for a search query"
    assert "search" in results[0]["title"].lower()


def test_no_results_for_unknown_term():
    engine = build_engine()
    assert engine.search("zzzzqqq") == []
