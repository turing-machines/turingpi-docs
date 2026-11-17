#!/usr/bin/env python3
"""Dump every page of docs.turingpi.com (ReadMe) to JSON, plus the sidebar tree.

    python3 -I scripts/readme_export.py <export_dir> [<img_dir>]

ReadMe embeds the raw page source in the HTML (<script id="ssr-props">), which is
more faithful than its /docs/<slug>.md export. Starting from the sidebar, the
script follows every doc link it finds in page bodies (plus the slugs of the old
v1.1 version), so hidden pages and dashboard redirects are captured too.
With <img_dir>, also downloads every files.readme.io file the pages reference.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

OUT = Path(sys.argv[1])
IMG = Path(sys.argv[2]) if len(sys.argv) > 2 else None
BASE = "https://docs.turingpi.com"
UA = {"User-Agent": "turingpi-docs-migration/1.0"}
(OUT / "pages").mkdir(parents=True, exist_ok=True)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)


def get(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    try:
        r = opener.open(req, timeout=30)
        return r.status, None, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location"), None


def ssr(html):
    return json.loads(re.search(r'<script id="ssr-props"[^>]*>(.*?)</script>', html, re.S).group(1))


def tree(pages):
    return [{"title": p["title"], "slug": p["slug"], "hidden": p.get("hidden", False),
             "pages": tree(p.get("pages", []))} for p in pages]


def slugs(pages):
    for p in pages:
        yield p["slug"]
        yield from slugs(p["pages"])


_, _, html = get("/docs/turing-pi2-intro")
nav = [{"title": c["title"], "pages": tree(c["pages"])} for c in ssr(html)["sidebar"]]
(OUT / "nav.json").write_text(json.dumps(nav, indent=1, ensure_ascii=False))

queue = [("docs", s) for c in nav for s in slugs(c["pages"])]
_, _, html11 = get("/v1.1/docs/turing-pi2-intro")
if html11:
    queue += [("docs", s) for c in ssr(html11)["sidebar"] for s in slugs(tree(c["pages"]))]
queue += [("page", "kickstarter-faq"), ("changelog", "turing-pi2-v25-list-of-improvements")]

done, img_urls = set(), set()
while queue:
    kind, slug = queue.pop(0)
    if (kind, slug) in done:
        continue
    done.add((kind, slug))
    st, loc, html = get(f"/{kind}/{slug}")
    rec = {"kind": kind, "slug": slug, "status": st, "location": loc}
    if html:
        doc = ssr(html).get("document") or {}
        rec.update(title=doc.get("title"), type=doc.get("type"), updated_at=doc.get("updated_at"),
                   metadata=doc.get("metadata"), content=doc.get("content"), parent=doc.get("parent"))
        body = (rec.get("content") or {}).get("body") or ""
        img_urls |= set(re.findall(r"https://files\.readme\.io/[^\s\"')<>\]]+", body))
        for s in re.findall(r"\(doc:([A-Za-z0-9_-]+)", body):
            queue.append(("docs", s))
        for k, s in re.findall(r"docs\.turingpi\.com(?:/v[\d.]+)?/(docs|page|changelog)/([A-Za-z0-9_-]+)", body):
            queue.append((k, s))
    elif loc:
        m = re.search(r"/(docs|page|changelog)/([A-Za-z0-9_-]+)", loc)
        if m:
            queue.append((m.group(1), m.group(2)))
    (OUT / "pages" / f"{kind}__{slug}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    print(st, kind, slug, loc or "")
    time.sleep(0.25)

if IMG:
    IMG.mkdir(parents=True, exist_ok=True)
    for u in sorted(img_urls):
        dst = IMG / u.rsplit("/", 1)[1]
        if not dst.exists():
            dst.write_bytes(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())
    print(f"images: {len(img_urls)}")
