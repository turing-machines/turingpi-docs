#!/usr/bin/env python3
"""Import the ReadMe export of docs.turingpi.com into this Starlight project.

One-off migration tool, kept so the import can be re-run right before cutover.

    python3 -I scripts/readme_export.py  <export_dir>            # 1. dump ReadMe pages
    python3 -I scripts/readme_import.py  <export_dir> <img_dir> .  # 2. convert

<export_dir> holds nav.json + pages/*.json (see readme_export.py).
<img_dir> holds the files downloaded from files.readme.io, named by URL basename.

Writes:
  src/content/docs/{docs,page,changelog}/*.md   page content
  src/assets/img/*                              images (optimised by Astro at build)
  src/sidebar.json                              sidebar tree used by astro.config.mjs
  public/_redirects                             301s that keep every old URL working
"""
import json
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

EXPORT, IMGSRC, ROOT = (Path(a) for a in sys.argv[1:4])
CONTENT = ROOT / "src/content/docs"
ASSETS = ROOT / "src/assets/img"
PUBLIC = ROOT / "public"
MAX_IMG_WIDTH = 2000  # originals wider than this are downscaled before committing

# Redirects configured in the ReadMe dashboard, found by probing every slug that
# content or the v1.1 version links to. The dashboard may hold a few more.
README_REDIRECTS = {
    "accessing-nodes-filesystems": "tpi-accessing-nodes-filesystems",
    "connect-to-the-bmc": "turing-pi2-bmc-how-to-get-started",
    "installing-os-orin-nxnano": "orin-nxnano-flashing-os",
    "nvidia-jetson-nano-how-to-install-os": "nvidia-jetson-nano-flashing-os",
    "raspberry-pi-cm4-install-os-using-turing-pi2-cluster": "raspberry-pi-cm4-flashing-os",
    "turing-pi2-bmc-update": "turing-pi2-bmc-firmware-upgrade",
    "turing-pi2-tpi-cli": "tpi-usage",
    "usage": "tpi-usage",
    "bmc-ui": "turing-pi2-bmc-ui",
    "firmware-upgrade": "turing-pi2-bmc-firmware-upgrade",
    "how-tos": "turing-pi2-bmc-how-tos",
    "install-os": "raspberry-pi-cm4-flashing-os",
    "installation": "tpi-installation",
}
# Slugs that 404 on ReadMe today but are linked from content or exist only in the
# old v1.1 version; send them somewhere useful instead.
EXTRA_REDIRECTS = {
    "turing-rk1-flashing-firmware": "turing-rk1-flashing-os",
    "turing-rk1-installing-os-1": "turing-rk1-flashing-os",
    "turing-pi2-bmc-linux-os": "turing-pi2-bmc-intro-specs",
}
CATEGORY_LABELS = {
    "Turing Pi2": "Turing Pi 2",
    "AdvanceD topics": "Advanced Topics",
    "turing pi 1 docs": "Turing Pi 1",
}
SITE = "Turing Pi Docs"
ASIDES = {"📘": "note", "ℹ": "note", "👍": "tip", "✅": "tip", "🚧": "caution", "⚠": "caution", "❗": "danger", "🛑": "danger"}
CALLOUT_THEMES = {"default": "note", "info": "note", "okay": "tip", "warn": "caution", "error": "danger"}

warnings: list[str] = []


def warn(msg: str) -> None:
    warnings.append(msg)


# --------------------------------------------------------------------------- load

nav = json.loads((EXPORT / "nav.json").read_text())
pages = {}
for f in sorted((EXPORT / "pages").glob("*.json")):
    rec = json.loads(f.read_text())
    pages[(rec["kind"], rec["slug"])] = rec

has_content = {s for (k, s), r in pages.items() if k == "docs" and r["status"] == 200}
group_redirects = {}  # parent pages without content: ReadMe redirects them to the first child


def first_leaf(node):
    return node["slug"] if node["slug"] in has_content else first_leaf(node["pages"][0])


def walk(nodes, trail):
    for n in nodes:
        n["trail"] = trail
        if n["slug"] not in has_content and n["pages"]:
            group_redirects[n["slug"]] = first_leaf(n)
        walk(n["pages"], trail + [n["title"]])


for cat in nav:
    cat["label"] = CATEGORY_LABELS.get(cat["title"], cat["title"])
    walk(cat["pages"], [cat["label"]])

for (k, s), r in pages.items():  # redirects the export observed (status 301/302)
    m = re.search(r"/docs/([A-Za-z0-9_-]+)", r.get("location") or "")
    if k == "docs" and r["status"] in (301, 302) and m and s not in group_redirects:
        README_REDIRECTS.setdefault(s, m.group(1))

ALIASES = {**README_REDIRECTS, **EXTRA_REDIRECTS, **group_redirects}


def canon(slug: str) -> str:
    seen = set()
    while slug in ALIASES and slug not in seen:
        seen.add(slug)
        slug = ALIASES[slug]
    if slug not in has_content:
        warn(f"link to unknown doc slug: {slug}")
    return slug


# ------------------------------------------------------------------------- images

def detect_ext(p: Path) -> str:
    head = p.read_bytes()[:12]
    if head.startswith(b"\x89PNG"):
        return ".png"
    if head.startswith(b"\xff\xd8"):
        return ".jpg"
    if head[:4] == b"GIF8":
        return ".gif"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return ".webp"
    if b"<svg" in p.read_bytes()[:400]:
        return ".svg"
    raise ValueError(f"unknown image type: {p}")


image_map: dict[str, str] = {}  # readme url -> file name in src/assets/img


def local_image(url: str) -> str:
    if url in image_map:
        return image_map[url]
    src = IMGSRC / url.rsplit("/", 1)[1]
    if not src.exists():
        warn(f"image not downloaded: {url}")
        image_map[url] = url
        return url
    stem = re.sub(r"[^A-Za-z0-9_-]", "-", src.name.rsplit(".", 1)[0] if "." in src.name else src.name)
    name = stem + detect_ext(src)
    dst = ASSETS / name
    if not dst.exists():
        shutil.copyfile(src, dst)
        if dst.suffix in (".png", ".jpg"):
            w = int(subprocess.run(["sips", "-g", "pixelWidth", str(dst)], capture_output=True, text=True)
                    .stdout.split()[-1])
            if w > MAX_IMG_WIDTH:
                subprocess.run(["sips", "--resampleWidth", str(MAX_IMG_WIDTH), str(dst)], capture_output=True, check=True)
    image_map[url] = name
    return name


def img_ref(url: str, depth: int) -> str:
    name = local_image(url)
    if name.startswith("http"):
        return name
    # depth = folders below src/content/docs; +2 climbs out of docs/ and content/
    return "../" * (depth + 2) + "assets/img/" + name


# ---------------------------------------------------------------------- converters

def split_code(body: str):
    """Yield (is_code, text) chunks so prose transforms never touch fenced code."""
    out, buf, fence = [], [], None
    for line in body.split("\n"):
        m = re.match(r"^(\s*)(`{3,}|~{3,})(.*)$", line)
        if fence is None and m:
            out.append((False, "\n".join(buf)))
            buf = []
            fence = m.group(2)
            lang = m.group(3).strip().split(" ")[0].lower() if m.group(3).strip() else ""
            buf.append(f"{m.group(1)}{fence}{lang}")
        elif fence is not None and m and m.group(2).startswith(fence[0]) and len(m.group(2)) >= len(fence) and not m.group(3).strip():
            buf.append(line)
            out.append((True, "\n".join(buf)))
            buf, fence = [], None
        else:
            buf.append(line)
    if fence is not None:
        warn("unclosed code fence")
    out.append((fence is not None, "\n".join(buf)))
    return out


def attrs(s: str) -> dict:
    return {k: (a if a is not None else b) for k, a, b in re.findall(r'(\w+)=(?:"([^"]*)"|\{([^}]*)\})', s)}


def image_md(url: str, alt: str, depth: int, half: bool = False) -> str:
    alt = alt.replace("[", "").replace("]", "").strip()
    md = f"![{alt}]({img_ref(url, depth)})"
    return ("@@SBS@@" + md) if half else md


def conv_image_jsx(text: str, depth: int) -> str:
    def repl(m):
        a = attrs(m.group(1))
        caption = (m.group(2) or "").strip()
        alt = a.get("alt") or caption
        half = a.get("width", "").strip().startswith("49")
        md = image_md(a["src"], alt, depth, half)
        if caption:
            md += f'\n\n<p class="img-caption">{caption}</p>'
        return md
    text = re.sub(r"<Image\s+([^>]*?)\s*/>()", repl, text, flags=re.S)
    return re.sub(r"<Image\s+([^>]*?)>(.*?)</Image>", repl, text, flags=re.S)


def conv_htmlblock(text: str, depth: int) -> str:
    def repl(m):
        html = m.group(1).strip()
        if re.fullmatch(r"(<br\s*/?>\s*)+", html) or html.startswith("<style"):
            return ""
        srcs = re.findall(r'<img[^>]*src="([^"]+)"', html)
        if srcs:
            return "\n".join(image_md(s, "", depth, half=len(srcs) > 1) for s in srcs)
        warn(f"HTMLBlock kept as raw HTML: {html[:60]!r}")
        return html
    return re.sub(r"<HTMLBlock>\{`(.*?)`\}</HTMLBlock>", repl, text, flags=re.S)


def wrap_sbs(text: str) -> str:
    """Group runs of half-width images into a side-by-side block."""
    lines, out, run = text.split("\n"), [], []

    def flush():
        if run:
            out.extend(['<div class="sbs">', "", "\n".join(run), "", "</div>"])
            run.clear()

    for line in lines:
        if line.startswith("@@SBS@@"):
            run.append(line[len("@@SBS@@"):])
        elif line.strip() == "" and run:
            continue
        else:
            flush()
            out.append(line)
    flush()
    return "\n".join(out)


def cell_md(html: str) -> str:
    paras = [p for p in re.split(r"\n\s*\n", textwrap.dedent(html).strip()) if p.strip()]
    parts = []
    for p in paras:
        ls = [l.strip() for l in p.split("\n")]
        parts.append("".join(l[:-1] + "<br>" if l.endswith("\\") else l + " " for l in ls).strip())
    return " ".join(parts).replace("|", "\\|")


def conv_table_jsx(text: str) -> str:
    def repl(m):
        inner = m.group(1)
        head = re.search(r"<thead>(.*?)</thead>", inner, re.S)
        ths = [cell_md(c) for c in re.findall(r"<th[^>]*>(.*?)</th>", head.group(1), re.S)] if head else []
        rows = [[cell_md(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
                for tr in re.findall(r"<tr>(.*?)</tr>", re.search(r"<tbody>(.*?)</tbody>", inner, re.S).group(1), re.S)]
        n = max(len(ths), *(len(r) for r in rows))
        ths += [""] * (n - len(ths))
        md = ["| " + " | ".join(ths) + " |", "|" + "---|" * n]
        md += ["| " + " | ".join(r + [""] * (n - len(r))) + " |" for r in rows]
        return "\n".join(md)
    return re.sub(r"<Table[^>]*>(.*?)</Table>", repl, text, flags=re.S)


def conv_callout_jsx(text: str) -> str:
    def repl(m):
        a = attrs(m.group(1))
        body = textwrap.dedent(m.group(2)).strip()
        hm = re.fullmatch(r"#{1,6}\s*(.+)", body)
        if hm:
            body = f"**{hm.group(1).strip()}**"
        icon = a.get("icon", "")
        return f":::{CALLOUT_THEMES.get(a.get('theme', 'default'), 'note')}\n{icon} {body}".rstrip() + "\n:::"
    return re.sub(r"<Callout([^>]*)>(.*?)</Callout>", repl, text, flags=re.S)


def conv_blockquote_callouts(text: str) -> str:
    lines, out, i = text.split("\n"), [], 0
    emoji_re = re.compile(r"^>\s*(" + "|".join(map(re.escape, ASIDES)) + r")️?\s*(.*)$")
    while i < len(lines):
        m = emoji_re.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        block = [m.group(2)]
        i += 1
        while i < len(lines) and lines[i].startswith(">"):
            block.append(re.sub(r"^> ?", "", lines[i]))
            i += 1
        kind = ASIDES[m.group(1)]
        first, rest = block[0].strip(), block[1:]
        while rest and not rest[0].strip():
            rest = rest[1:]
        if first and rest:
            head, body = f":::{kind}[{first.replace(']', '')}]", rest
        else:
            head, body = f":::{kind}", ([first] if first else []) + rest
        if out and out[-1].strip():
            out.append("")
        out += [head, *body, ":::"]
        if i < len(lines) and lines[i].strip():
            out.append("")
    return "\n".join(out)


def conv_links(text: str) -> str:
    # heading ids are lower-case (github-slugger); ReadMe matched anchors case-insensitively
    text = re.sub(r"\(doc:([A-Za-z0-9_-]+)(#[^)\s]*)?",
                  lambda m: f"(/docs/{canon(m.group(1))}{(m.group(2) or '').lower()}", text)

    def abs_link(m):
        kind, slug, anchor = m.group(1), m.group(2), (m.group(3) or "").lower()
        if kind == "docs":
            slug = canon(slug)
        return f"/{kind}/{slug}{anchor}"
    text = re.sub(r"https?://docs\.turingpi\.com(?:/v[\d.]+)?/(docs|page|changelog)/([A-Za-z0-9_-]+)(?:\.md)?(#[^)\s\"']*)?",
                  abs_link, text)
    return text


def conv_md_images(text: str, depth: int) -> str:
    return re.sub(r"(!\[[^\]]*\]\()(https://files\.readme\.io/[^)\s]+)",
                  lambda m: m.group(1) + img_ref(m.group(2), depth), text)


def demote_h1(body: str) -> str:
    """ReadMe bodies sometimes use '#' for sections; Starlight renders the page title as h1."""
    chunks = split_code(body)
    if not any(re.search(r"^# ", t, re.M) for c, t in chunks if not c):
        return body
    return "\n".join(t if c else re.sub(r"^(#{1,5}) ", r"#\1 ", t, flags=re.M) for c, t in chunks)


def convert(body: str, depth: int) -> str:
    body = body.replace("\r\n", "\n")
    out = []
    for is_code, chunk in split_code(body):
        if is_code:
            out.append(chunk)
            continue
        t = conv_htmlblock(chunk, depth)
        t = conv_table_jsx(t)
        t = conv_callout_jsx(t)
        t = conv_image_jsx(t, depth)
        t = conv_md_images(t, depth)
        t = conv_blockquote_callouts(t)
        t = conv_links(t)
        t = wrap_sbs(t)
        out.append(t)
    body = demote_h1("\n".join(out))
    if "files.readme.io" in body:
        for u in re.findall(r"https://files\.readme\.io/[^)\s\"']+", body):
            warn(f"files.readme.io URL left in content: {u}")
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    return body


# ------------------------------------------------------------------- frontmatter

def plain(md: str) -> str:
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"[*_`]", "", md)
    md = re.sub(r"<[^>]+>", "", md)
    return re.sub(r"\s+", " ", md).strip()


def auto_description(body: str) -> str:
    for is_code, chunk in split_code(body):
        if is_code:
            continue
        for para in re.split(r"\n\s*\n", chunk):
            p = para.strip()
            if not p or p[0] in "#|<:!>*-" or p.startswith("@@") or re.match(r"^\d+\.", p):
                continue
            text = plain(p)
            if len(text) < 40:
                continue
            if len(text) > 160:
                text = text[:157].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
            return text
    return ""


def seo_title(rec: dict, trail: list[str]) -> str:
    meta = ((rec.get("metadata") or {}).get("title") or "").strip()
    meta = re.sub(r"\s*\|\s*Docs$", "", meta)
    if len(meta) > 8:
        return f"{meta} | {SITE}"
    ctx = " | ".join(reversed([t for t in trail if t not in ("Getting Started",)]))
    return f"{rec['title']} | {ctx} | {SITE}" if ctx else f"{rec['title']} | {SITE}"


def q(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def write_page(rec: dict, trail: list[str]) -> None:
    kind, slug = rec["kind"], rec["slug"]
    content = rec.get("content") or {}
    depth = 1  # src/content/docs/<kind>/<slug>.md
    body = convert(content.get("body") or "", depth)
    excerpt = (content.get("excerpt") or "").strip()
    desc = ((rec.get("metadata") or {}).get("description") or "").strip() or excerpt or auto_description(body)
    fm = [f"title: {q(rec['title'])}"]
    if desc:
        fm.append(f"description: {q(desc)}")
    fm += ["head:", "  - tag: title", f"    content: {q(seo_title(rec, trail))}"]
    if rec.get("updated_at"):
        fm.append(f"lastUpdated: {rec['updated_at'][:10]}")
    if excerpt:
        body = f'<p class="lead">{excerpt}</p>\n\n' + body
    path = CONTENT / kind / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + "\n".join(fm) + "\n---\n\n" + body)


# -------------------------------------------------------------------------- main

for d in (CONTENT / "docs", CONTENT / "page", CONTENT / "changelog", ASSETS):
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)

trail_of = {}


def collect(nodes):
    for n in nodes:
        trail_of[n["slug"]] = n["trail"]
        collect(n["pages"])


for cat in nav:
    collect(cat["pages"])

for (kind, slug), rec in sorted(pages.items()):
    if rec["status"] != 200:
        continue
    parent = ((rec.get("parent") or {}).get("uri") or "").rsplit("/", 1)[-1]
    trail = trail_of.get(slug) or (trail_of.get(parent, []) + [n["title"] for c in nav for n in c["pages"] if n["slug"] == parent])
    if kind == "changelog":
        trail = ["Changelog"]
    write_page(rec, trail)

# changelog index (ReadMe had a list page at /changelog)
entries = sorted(((r["updated_at"] or "", r) for (k, _), r in pages.items() if k == "changelog"), reverse=True)
(CONTENT / "changelog" / "index.md").write_text(
    "---\ntitle: Changelog\ndescription: Hardware revisions and notable changes to Turing Pi boards.\n---\n\n"
    + "\n".join(f"- [{r['title']}](/changelog/{r['slug']}) — {d[:10]}" for d, r in entries) + "\n")


# sidebar --------------------------------------------------------------------
def sb(nodes):
    items = []
    for n in nodes:
        link = f"/docs/{n['slug']}"
        if not n["pages"]:
            items.append({"label": n["title"], "link": link})
            continue
        sub = sb(n["pages"])
        if n["slug"] in has_content:
            sub.insert(0, {"label": "Overview", "link": link})
        items.append({"label": n["title"], "collapsed": True, "items": sub})
    return items


sidebar = [{"label": c["label"], "items": sb(c["pages"])} for c in nav]
sidebar.append({"label": "Changelog", "link": "/changelog"})
(ROOT / "src/sidebar.json").write_text(json.dumps(sidebar, indent=2, ensure_ascii=False) + "\n")

# redirects ------------------------------------------------------------------
red = ["# Generated by scripts/readme_import.py: keeps every docs.turingpi.com URL from ReadMe working.",
       "/docs                 /docs/turing-pi2-intro  301",
       "/docs/                /docs/turing-pi2-intro  301"]
for src, dst in sorted(ALIASES.items()):
    red.append(f"/docs/{src}  /docs/{canon(dst)}  301")
red.append("/docs/turing-pi2-v25-list-of-improvements  /changelog/turing-pi2-v25-list-of-improvements  301")
red += ["# ReadMe also served every page under its version prefix",
        "/v2.0.0/*  /:splat  301",
        "/v1.1/*  /:splat  301"]
(PUBLIC / "_redirects").write_text("\n".join(red) + "\n")

n_pages = sum(1 for _ in CONTENT.rglob("*.md"))
print(f"pages: {n_pages}, images: {len(list(ASSETS.iterdir()))}, redirects: {len(red) - 2}")
for w in sorted(set(warnings)):
    print("WARN", w)
