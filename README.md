# Private Search Engine

A search engine that runs entirely on your own machine. It indexes only
the documents you put in `documents/` — no account, no API key, no cloud
service, and no data leaving the machine.

## What it does

- **Indexer** (`search_engine.py`): tokenises documents, builds an
  inverted index (`term → {doc: term frequency}`), and computes IDF.
- **Ranking**: TF-IDF scoring, with a 1.5× boost for title matches.
  Repeated words use log TF so they can't dominate a result.
- **Snippets**: each result shows a window of text around the first
  matching term.
- **Web UI** (`app.py`): standard-library only, no dependencies.
  Search from a browser, or run `python3 search_engine.py <query>` on
  the command line.

## Run it

```bash
python3 app.py
# open http://127.0.0.1:8000
```

Add your own documents: drop `.txt` or `.md` files into `documents/`
(first line = title) and restart the app. The index rebuilds on startup.

## Tests

```bash
python3 -m pytest tests/ -q
# or, without pytest:
python3 -c "
from search_engine import build_engine
print(build_engine().search('redis cache'))
"
```

## Why this is a good resume project

It is not a CRUD wrapper around someone else's API. You can explain, in
an interview, the data structure (inverted index), the ranking math
(TF-IDF), the trade-offs (title boost, log TF, stopwords), and the
privacy property (local-only by construction) — and then demo it live.
