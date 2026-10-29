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

## Website version (GitHub Pages)

GitHub Pages can only serve static files, so it cannot run the Python
app above. `index.html` is a static, client-side version of the same
search engine: the same documents, the same tokenising, inverted index,
TF-IDF ranking, title boost, and snippets — all in JavaScript, all in
the browser — plus a clean dark UI and, for a person or topic, a web
card from Wikipedia, photos from Wikimedia Commons, and videos played
right in the page from many free sites — Wikimedia Commons,
Internet Archive, Dailymotion, and PeerTube — plus a YouTube search
link. Web info uses free public APIs with no account and no key;
local documents are still searched entirely in your browser.

## Privacy: no history

This search engine stores no search history and no watch history:
no cookies, no localStorage, no saved list, no account. The page
itself records nothing you search or play. When you play a video,
that video site itself will see that play, just like visiting it
directly — this page does not record it.

To publish it: in the repo, go to Settings → Pages → Build and
deployment → Deploy from a branch, choose `main` and `/ (root)`, and
save. The site will then be at
`https://tanmaymaind.github.io/private-search-engine-by-Tanmay-Maind-/`

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
