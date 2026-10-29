"""Web UI for the private search engine. Standard library only.

Run:  python3 app.py
Then open http://127.0.0.1:8000 in a browser and search.
No data leaves this machine: the index is built from documents/ at startup.
"""

from __future__ import annotations

import html
import json
import re
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from search_engine import build_engine

ENGINE = build_engine()
PORT = 8000


def web_summary(query: str):
    """Best-effort Wikipedia summary for a person/topic. None on any failure.

    This is the only external call the local app makes, and only when you
    search. Local documents are still searched privately on your machine.
    """
    try:
        search_url = (
            "https://en.wikipedia.org/w/api.php?action=query&list=search"
            f"&srsearch={urllib.parse.quote(query)}&format=json"
        )
        req = urllib.request.Request(search_url, headers={"User-Agent": "PrivateSearch/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            search_results = json.load(resp)["query"]["search"]
        top = search_results[0]
        title = top["title"]
        articles = [
            {
                "title": s["title"],
                "snippet": re.sub(r"<[^>]+>", "", s.get("snippet", "")),
                "url": "https://en.wikipedia.org/wiki/"
                + urllib.parse.quote(s["title"].replace(" ", "_")),
            }
            for s in search_results[:8]
        ]
        req = urllib.request.Request(
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + urllib.parse.quote(title),
            headers={"User-Agent": "PrivateSearch/1.0"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.load(resp)
        return {
            "articles": articles,
            "title": data.get("title", title),
            "description": data.get("description", ""),
            "extract": data.get("extract", ""),
            "image": (data.get("thumbnail") or {}).get("source", ""),
            "url": (data.get("content_urls") or {}).get("desktop", {}).get("page", ""),
        }
    except Exception:
        return None


def page(query: str = "", results: list | None = None, web: dict | None = None) -> bytes:
    q = html.escape(query, quote=True)
    body = f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>Private Search</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 16px; }}
input {{ width: 70%; padding: 10px; font-size: 16px; }}
button {{ padding: 10px 16px; font-size: 16px; }}
.result {{ margin: 20px 0; }} .score {{ color: #666; font-size: 13px; }}
small {{ color: #666; }}
</style></head><body>
<h1>Private Search</h1>
<p><small>Runs locally. Local documents are indexed from <code>documents/</code>
only, and this app stores no search history and no watch history.
A web card below is fetched only when you search, to show info,
photos and videos for a person or topic from many free sites,
not only YouTube.</small></p>
<form><input name="q" value="{q}" placeholder="Search your documents…" autofocus>
<button>Search</button></form>
"""
    if query and web and web.get("extract"):
        enc = urllib.parse.quote(query)
        img = (
            f'<img src="{html.escape(web["image"])}" style="width:180px;border-radius:12px">'
            if web.get("image") else ""
        )
        body += (
            f'<div style="border:1px solid #ddd;border-radius:12px;padding:16px">'
            f'<h2>From the web — {html.escape(web["title"])}</h2>'
            f'{img}<p>{html.escape(web["description"])}</p>'
            f'<p>{html.escape(web["extract"])}</p>'
            f'<p><a href="{html.escape(web["url"])}">Read more on Wikipedia</a> · '
            f'<a href="https://commons.wikimedia.org/w/index.php?search={enc}&title=Special:MediaSearch&type=image">Photos on Commons</a> · '
            f'<a href="https://commons.wikimedia.org/w/index.php?search={enc}&title=Special:MediaSearch&type=video">Videos on Commons</a> · '
            f'<a href="https://archive.org/search?query={enc}">Videos on Archive.org</a> · '
            f'<a href="https://www.dailymotion.com/search/{enc}">Videos on Dailymotion</a> · '
            f'<a href="https://search.joinpeertube.org/search?search={enc}">Videos on PeerTube</a> · '
            f'<a href="https://www.youtube.com/results?search_query={enc}">More videos on YouTube</a></p></div>'
        )
        articles_html = "".join(
            f'<div><b><a href="{html.escape(a["url"])}">{html.escape(a["title"])}</a></b>'
            f'<div><small>{html.escape(a["snippet"])}… · Wikipedia</small></div></div>'
            for a in web.get("articles", [])
        )
        body += (
            f'<div style="border:1px solid #ddd;border-radius:12px;padding:16px;margin-top:16px">'
            f"<h2>Results from the internet</h2>{articles_html}"
            f'<p><b>Search the whole web:</b> '
            f'<a href="https://www.google.com/search?q={enc}">Google</a> · '
            f'<a href="https://www.bing.com/search?q={enc}">Bing</a> · '
            f'<a href="https://duckduckgo.com/?q={enc}">DuckDuckGo</a> · '
            f'<a href="https://search.brave.com/search?q={enc}">Brave</a></p></div>'
        )
    if query:
        if not results:
            body += f"<p>No results for <b>{q}</b>.</p>"
        else:
            body += f"<p>{len(results)} result(s) for <b>{q}</b>:</p>"
            for r in results:
                body += (
                    f'<div class="result"><b>{html.escape(r["title"])}</b> '
                    f'<span class="score">score {r["score"]} · {html.escape(r["path"])}</span>'
                    f'<div>{html.escape(r["snippet"])}</div></div>'
                )
    body += "</body></html>"
    return body.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query).get("q", [""])[0]
        results = ENGINE.search(query) if query.strip() else None
        web = web_summary(query) if query.strip() else None
        data = page(query, results, web)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):  # keep the terminal quiet
        pass


if __name__ == "__main__":
    print(f"Private search running at http://127.0.0.1:{PORT}/ "
          f"({ENGINE.num_docs} documents indexed)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
