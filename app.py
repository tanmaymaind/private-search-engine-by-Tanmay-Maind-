"""Web UI for the private search engine. Standard library only.

Run:  python3 app.py
Then open http://127.0.0.1:8000 in a browser and search.
No data leaves this machine: the index is built from documents/ at startup.
"""

from __future__ import annotations

import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from search_engine import build_engine

ENGINE = build_engine()
PORT = 8000


def page(query: str = "", results: list | None = None) -> bytes:
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
<p><small>Runs locally. Only indexes files in <code>documents/</code>.
No external calls, no tracking.</small></p>
<form><input name="q" value="{q}" placeholder="Search your documents…" autofocus>
<button>Search</button></form>
"""
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
        data = page(query, results)
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
