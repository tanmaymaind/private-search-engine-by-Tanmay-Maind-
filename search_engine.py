"""Private search engine: inverted index + TF-IDF ranking.

Runs entirely locally. It only indexes files in the ``documents/`` folder
next to this file - it makes no network calls and sends nothing anywhere.

How it works, in interview terms:
1. Tokenise every document (lowercase, strip punctuation, drop stopwords).
2. Build an inverted index: term -> {doc_id: term frequency}.
3. Score a query with TF-IDF, with a small boost when a term is in the title.
4. Return ranked results with a snippet centred on the first matching term.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from pathlib import Path

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "by", "at", "as", "it", "its",
    "this", "that", "from", "into", "you", "your", "we", "our",
}

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase, split on non-alphanumerics, drop stopwords."""
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


class Document:
    def __init__(self, doc_id: int, title: str, text: str, path: str):
        self.doc_id = doc_id
        self.title = title
        self.text = text
        self.path = path
        self.tokens = tokenize(text)
        self.term_freq = Counter(self.tokens)
        self.title_tokens = set(tokenize(title))


class SearchEngine:
    def __init__(self, documents: list[Document]):
        self.documents = documents
        self.num_docs = len(documents)
        # term -> {doc_id: tf}
        self.index: dict[str, dict[int, int]] = defaultdict(dict)
        for doc in documents:
            for term, tf in doc.term_freq.items():
                self.index[term][doc.doc_id] = tf
        # idf per term, smoothed so unseen-ish terms do not explode
        self.idf: dict[str, float] = {
            term: math.log(1 + self.num_docs / len(postings))
            for term, postings in self.index.items()
        }

    def search(self, query: str, top_n: int = 10) -> list[dict]:
        query_terms = tokenize(query)
        if not query_terms:
            return []
        scores: dict[int, float] = defaultdict(float)
        matched: dict[int, set[str]] = defaultdict(set)
        for term in set(query_terms):
            if term not in self.index:
                continue
            idf = self.idf[term]
            for doc_id, tf in self.index[term].items():
                # log TF keeps a repeated word from dominating the score
                score = (1 + math.log(tf)) * idf
                doc = self.documents[doc_id]
                if term in doc.title_tokens:
                    score *= 1.5  # title match is a stronger signal
                scores[doc_id] += score
                matched[doc_id].add(term)
        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        results = []
        for doc_id, score in ranked[:top_n]:
            doc = self.documents[doc_id]
            results.append({
                "title": doc.title,
                "path": doc.path,
                "score": round(score, 3),
                "matched_terms": sorted(matched[doc_id]),
                "snippet": make_snippet(doc.text, matched[doc_id]),
            })
        return results


def make_snippet(text: str, terms: set[str], window: int = 120) -> str:
    """Return a window of text around the first matched term, if any."""
    if not terms:
        return text[:200]
    lower = text.lower()
    pos = min((lower.find(t) for t in terms if lower.find(t) >= 0), default=0)
    start = max(0, pos - window // 2)
    end = min(len(text), pos + window)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"
    return snippet


def load_documents(documents_dir: Path) -> list[Document]:
    """Load .txt and .md files. First line is the title, rest is body."""
    docs = []
    files = sorted(documents_dir.glob("*.txt")) + sorted(documents_dir.glob("*.md"))
    for i, path in enumerate(files):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        lines = raw.strip().splitlines()
        title = lines[0].lstrip("# ").strip() if lines else path.stem
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else raw
        docs.append(Document(i, title, body, path.name))
    return docs


def build_engine(documents_dir: Path | None = None) -> SearchEngine:
    if documents_dir is None:
        documents_dir = Path(__file__).parent / "documents"
    return SearchEngine(load_documents(documents_dir))


if __name__ == "__main__":
    import json
    import sys

    engine = build_engine()
    query = " ".join(sys.argv[1:]) or "python"
    print(f"Indexed {engine.num_docs} documents, "
          f"{len(engine.index)} unique terms.")
    print(json.dumps(engine.search(query), indent=2, ensure_ascii=False))
