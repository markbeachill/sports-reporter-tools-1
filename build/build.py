#!/usr/bin/env python3
"""
Build the Sports Reporter Tools documentation site.

- .md tool files  -> rendered HTML pages WITH a "Copy prompt" button (copies raw .md)
- .docx documents -> rendered HTML pages (normal docs, no copy button)
- shared assets    -> styles.css, app.js, index.html landing page
- raw .md files copied into /prompts so Copy buttons fetch real source

Build-free output: plain HTML/CSS/JS served directly by GitHub Pages.
A .nojekyll file is written so Pages serves files as-is (no Jekyll processing).
"""

import os, re, html, glob, shutil, json
import markdown as md_lib
from docx import Document

SRC = "/home/claude/v2/sports-reporting-ai-tools"
OUT = "/home/claude/repo"
DOCS = os.path.join(OUT, "docs")

# ---------------------------------------------------------------------------
# Site navigation model
# ---------------------------------------------------------------------------
# Each page: slug, title, source file, kind ('md'|'docx'), group
PAGES = [
    # Tools (prompts) — md files, copiable
    dict(slug="sr1-match-report-analyser", title="Match Report Analyser — SR1",
         src="SR1-match-report-analyser-v0.6.md", kind="md", group="Tools"),
    dict(slug="sr2-match-report-coach", title="Match Report Coach (beginner route) — SR2",
         src="SR2-match-report-coach-beginner-route-v0.2.md", kind="md", group="Tools"),
    dict(slug="sr3-match-preview-analyser", title="Match Preview Analyser — SR3",
         src="SR3-match-preview-analyser-v0.5-beta.md", kind="md", group="Tools"),
    dict(slug="sr4-feature-analysis-tool", title="Feature Analysis Tool — SR4",
         src="SR4-feature-analysis-tool-v0.1.md", kind="md", group="Tools"),
    # Design notes (SRD)
    dict(slug="srd-01-tutor-design-rationale", title="Writing Tutor: Design Rationale — SRD-01",
         src="SRD-01-ai-sports-journalism-writing-tutor-design-rationale.docx", kind="docx", group="Design notes"),
    dict(slug="srd-02-readers-journey", title="The Reader's Journey — SRD-02",
         src="SRD-02-readers-journey-attachment-and-economy.docx", kind="docx", group="Design notes"),
    dict(slug="srd-03-important-because-it-isnt", title="Important Because It Isn't — SRD-03",
         src="SRD-03-important-because-it-isnt-conceptual-spine.docx", kind="docx", group="Design notes"),
    dict(slug="srd-04-voice", title="Voice — SRD-04",
         src="SRD-04-voice-fine-grain-of-economy-cliche-test.docx", kind="docx", group="Design notes"),
    dict(slug="srd-05-teaching-not-coaching", title="Teaching, Not Coaching — SRD-05",
         src="SRD-05-teaching-not-coaching-sr2-beginner-route.docx", kind="docx", group="Design notes"),
    dict(slug="srd-06-preview-and-social-currency", title="The Preview & Social Currency — SRD-06",
         src="SRD-06-preview-pull-before-event-social-currency.docx", kind="docx", group="Design notes"),
    # Evidence (SRE)
    dict(slug="sre-01-sr1-test-log", title="SR1 Match Report Analyser: Test Log — SRE-01",
         src="SRE-01-sr1-match-report-analyser-test-log.docx", kind="docx", group="Evidence"),
    # Papers (SRP)
    dict(slug="srp-01-paper-skeleton", title="Important Because It Isn't: Paper Skeleton — SRP-01",
         src="SRP-01-important-because-it-isnt-paper-skeleton.docx", kind="docx", group="Papers"),
    dict(slug="srp-02-previewing-the-unplayed-match", title="Previewing the Unplayed Match — SRP-02",
         src="SRP-02-previewing-the-unplayed-match-working-paper.docx", kind="docx", group="Papers"),
]

GROUP_ORDER = ["Tools", "Design notes", "Evidence", "Papers"]

GITHUB_REPO = "https://github.com/markbeachill/sports-reporter-tools"
ZIP_URL = "https://github.com/markbeachill/sports-reporter-tools/archive/refs/heads/main.zip"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_]+", "-", text)

def strip_frontmatter(text):
    """Remove leading YAML frontmatter and HTML comments for clean render,
    but keep them in the raw copy."""
    return text

# --- docx -> html ----------------------------------------------------------
def runs_to_html(p):
    out = []
    for r in p.runs:
        t = html.escape(r.text)
        if not t:
            continue
        if r.bold:
            t = f"<strong>{t}</strong>"
        if r.italic:
            t = f"<em>{t}</em>"
        out.append(t)
    return "".join(out)

def docx_to_html(path):
    d = Document(path)
    body = []
    toc = []
    # first non-empty paras: title (h1), subtitle, context — treat first as page title handled elsewhere
    seen_real_heading = False
    para_index = 0
    intro_count = 0
    list_open = False

    def close_list():
        nonlocal list_open
        if list_open:
            body.append("</ul>")
            list_open = False

    paras = [p for p in d.paragraphs]
    # Identify the leading title block (paragraphs before first Heading style)
    first_heading_idx = None
    for i, p in enumerate(paras):
        if p.text.strip() and p.style and p.style.name.startswith("Heading"):
            first_heading_idx = i
            break

    for i, p in enumerate(paras):
        txt = p.text.strip()
        style = p.style.name if p.style else "None"
        if not txt:
            continue
        # Leading title block -> subtitle/lead paragraphs (skip the very first, it's the page H1)
        if first_heading_idx is not None and i < first_heading_idx:
            if i == 0:
                continue  # page title rendered from nav metadata
            close_list()
            body.append(f'<p class="lead">{runs_to_html(p)}</p>')
            continue
        if style.startswith("Heading"):
            close_list()
            level = 2 if "1" in style else 3
            hid = slugify(txt)
            inner = runs_to_html(p) or html.escape(txt)
            body.append(f'<h{level} id="{hid}"><a class="anchor" href="#{hid}">#</a>{inner}</h{level}>')
            toc.append((level, txt, hid))
        elif style == "List Paragraph":
            if not list_open:
                body.append("<ul>")
                list_open = True
            body.append(f"<li>{runs_to_html(p)}</li>")
        else:
            close_list()
            body.append(f"<p>{runs_to_html(p)}</p>")
    close_list()
    return "\n".join(body), toc

# --- md -> html ------------------------------------------------------------
def split_md(text):
    """Return (frontmatter_dict_text, leading_comments, body_md)."""
    return text

def md_to_html(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    body = raw
    # strip leading HTML comment blocks (routing metadata) from rendered view
    body = re.sub(r"^(<!--.*?-->\s*)+", "", body, flags=re.DOTALL)
    # strip YAML frontmatter from rendered view
    fm = ""
    m = re.match(r"^---\n(.*?)\n---\n", body, flags=re.DOTALL)
    if m:
        fm = m.group(1)
        body = body[m.end():]
    md = md_lib.Markdown(extensions=["extra", "toc", "sane_lists", "nl2br"])
    html_body = md.convert(body)
    # build toc from md headings
    toc = []
    for h in re.findall(r'<h([23]) id="([^"]+)">(.*?)</h[23]>', html_body):
        level, hid, inner = int(h[0]), h[1], re.sub("<[^>]+>", "", h[2])
        toc.append((level, inner, hid))
    return html_body, toc, raw, fm

# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
def render_sidebar(active_slug, prefix=""):
    parts = ['<nav class="sidebar-nav" aria-label="Documentation">']
    parts.append(f'<a class="nav-home" href="{prefix}index.html">Overview</a>')
    for g in GROUP_ORDER:
        parts.append(f'<div class="nav-group"><div class="nav-group-title">{html.escape(g)}</div>')
        for pg in PAGES:
            if pg["group"] != g:
                continue
            cls = "nav-link active" if pg["slug"] == active_slug else "nav-link"
            href = f'{prefix}{pg["slug"]}.html'
            parts.append(f'<a class="{cls}" href="{href}">{html.escape(pg["title"])}</a>')
        parts.append("</div>")
    parts.append(f'<div class="nav-group"><div class="nav-group-title">Testing</div>'
                 f'<a class="nav-link nav-external" href="{GITHUB_REPO}/tree/main/source/benchmark">Benchmark protocol ↗</a></div>')
    parts.append("</nav>")
    return "\n".join(parts)

def render_toc(toc, prefix=""):
    if not toc:
        return ""
    items = ['<div class="toc"><div class="toc-title">On this page</div><ul>']
    for level, text, hid in toc:
        cls = "toc-l3" if level == 3 else "toc-l2"
        items.append(f'<li class="{cls}"><a href="#{hid}">{html.escape(text)}</a></li>')
    items.append("</ul></div>")
    return "\n".join(items)

def page_shell(title, content_html, toc_html, sidebar_html, copy_block="", prefix="", description=""):
    desc = html.escape(description or title)
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}">
<title>{html.escape(title)} · Sports Reporter Tools</title>
<link rel="stylesheet" href="{prefix}styles.css">
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{prefix}index.html"><span class="brand-mark">SR</span><span class="brand-text">Sports Reporter Tools</span></a>
    <div class="topbar-actions">
      <a class="btn-ghost" href="{ZIP_URL}">Download ZIP</a>
      <a class="btn-ghost" href="{GITHUB_REPO}">GitHub</a>
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme" title="Toggle theme">◐</button>
      <button class="menu-toggle" id="menuToggle" aria-label="Toggle menu">☰</button>
    </div>
  </div>
</header>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    {sidebar_html}
  </aside>
  <main class="content">
    <article class="doc">
      <h1>{html.escape(title)}</h1>
      {copy_block}
      {content_html}
    </article>
  </main>
  <aside class="toc-col">
    {toc_html}
  </aside>
</div>
<script src="{prefix}app.js"></script>
</body>
</html>
"""

def copy_block_for(slug, raw=""):
    encoded = html.escape(raw)
    return f"""<div class="prompt-bar">
  <div class="prompt-bar-text">
    <strong>This is a copiable AI prompt.</strong> Copy the full prompt below and paste it into your AI assistant, then follow its instructions.
  </div>
  <button class="copy-btn" data-src="prompts/{slug}.md">Copy prompt</button>
</div>
<div class="copy-status" id="copyStatus"></div>
<textarea id="rawPrompt" hidden aria-hidden="true">{encoded}</textarea>"""

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(DOCS, exist_ok=True)
    os.makedirs(os.path.join(DOCS, "prompts"), exist_ok=True)

    # Build each page
    landing_cards = {g: [] for g in GROUP_ORDER}
    for pg in PAGES:
        src = os.path.join(SRC, pg["src"])
        if pg["kind"] == "md":
            content, toc, raw, fm = md_to_html(src)
            # write raw prompt for copying
            with open(os.path.join(DOCS, "prompts", f'{pg["slug"]}.md'), "w", encoding="utf-8") as f:
                f.write(raw)
            copy_block = copy_block_for(pg["slug"], raw)
            desc = pg["title"] + " — copiable AI sports-writing analysis prompt."
        else:
            content, toc = docx_to_html(src)
            copy_block = ""
            desc = pg["title"] + " — design note / paper for the Sports Reporter Tools project."
        sidebar = render_sidebar(pg["slug"])
        toc_html = render_toc(toc)
        page = page_shell(pg["title"], content, toc_html, sidebar, copy_block, prefix="", description=desc)
        with open(os.path.join(DOCS, f'{pg["slug"]}.html'), "w", encoding="utf-8") as f:
            f.write(page)
        landing_cards[pg["group"]].append(pg)

    # Landing page
    write_landing(landing_cards)
    # Assets
    write_css()
    write_js()
    # Pages config: build-free
    open(os.path.join(DOCS, ".nojekyll"), "w").close()
    # README
    write_readme()
    print("Built", len(PAGES), "pages.")

def write_landing(cards):
    sidebar = render_sidebar("__home__")
    sections = []
    intros = {
        "Tools": "The runnable prompts (SR1–SR4). Each one is self-contained — copy it, paste it into an AI assistant, and paste in a match report, preview or feature.",
        "Design notes": "The SRD series — the design rationale and conceptual spine that shaped each analytical move the tools make.",
        "Evidence": "The SRE series — validation and test logs recording what was run and what was found.",
        "Papers": "The SRP series — working papers and article skeletons: the model, how it was built, and how it was tested against real writing.",
    }
    for g in GROUP_ORDER:
        items = []
        for pg in cards[g]:
            items.append(
                f'<a class="card" href="{pg["slug"]}.html">'
                f'<span class="card-title">{html.escape(pg["title"])}</span>'
                f'<span class="card-go">→</span></a>'
            )
        sections.append(
            f'<section class="group"><h2>{html.escape(g)}</h2>'
            f'<p class="group-intro">{intros[g]}</p>'
            f'<div class="card-grid">{"".join(items)}</div></section>'
        )
    content = f"""
    <p class="lead">A small toolkit and research archive for AI-supported sports-journalism teaching. The aim is not to make AI write sports journalism for students, but to help writers see how their writing works on a reader.</p>
    <p>The <strong>tools</strong> (SR1–SR4) are copiable prompts: take one, paste it into an AI assistant, and give it a match report, preview or feature to analyse. The supporting documents are organised in four streams — <strong>SR</strong> tools, <strong>SRD</strong> design notes, <strong>SRE</strong> evidence, and <strong>SRP</strong> papers — keeping practical tools, design rationale, test evidence and publishable drafts separate while preserving the development sequence.</p>
    <div class="prompt-bar" style="margin-top:1.5rem">
      <div class="prompt-bar-text"><strong>New here?</strong> Start with <a href="sr1-match-report-analyser.html">Match Report Analyser (SR1)</a>, or the beginner route <a href="sr2-match-report-coach.html">Match Report Coach (SR2)</a>. New in this version: the <a href="sr4-feature-analysis-tool.html">Feature Analysis Tool (SR4)</a>.</div>
    </div>
    {''.join(sections)}
    <section class="group"><h2 id="benchmark"><a class="anchor" href="#benchmark">#</a>Benchmark</h2>
      <p class="group-intro">The project includes a reproducible-testing protocol — a scoring rubric, case and run-log templates, and a model-comparison matrix — for validating tool runs across models. It is a working scaffold for contributors and lives in the repository rather than as library pages.</p>
      <div class="card-grid"><a class="card" href="{GITHUB_REPO}/tree/main/source/benchmark"><span class="card-title">Benchmark protocol & templates on GitHub</span><span class="card-go">↗</span></a></div>
    </section>
    """
    # landing has no right toc; build a toc of the groups instead
    toc = [(2, g, slugify(g)) for g in GROUP_ORDER] + [(2, "Benchmark", "benchmark")]
    # add ids to section h2s
    for g in GROUP_ORDER:
        content = content.replace(f'<h2>{html.escape(g)}</h2>', f'<h2 id="{slugify(g)}"><a class="anchor" href="#{slugify(g)}">#</a>{html.escape(g)}</h2>')
    toc_html = render_toc(toc)
    page = page_shell("Sports Reporter Tools", content, toc_html, sidebar,
                      prefix="", description="A library of AI analysis and tutoring tools for sports writing, with the design notes and papers behind them.")
    # replace the duplicated h1 (landing uses brand title)
    page = page.replace("<h1>Sports Reporter Tools</h1>", "<h1>Sports Reporter Tools</h1>")
    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)

def write_readme():
    txt = f"""# Sports Reporter Tools

A documentation library and research archive for AI-supported sports-journalism
teaching: runnable analysis/tutoring prompts, plus the design notes, evidence
logs and working papers behind them.

**Live site:** https://markbeachill.github.io/sports-reporter-tools/

## What's here

The archive uses four document streams:

- **Tools (SR1–SR4)** — copiable AI prompts. Open a tool page and press
  **Copy prompt** to copy the full prompt, then paste it into an AI assistant.
  SR1 match-report analyser, SR2 beginner coach, SR3 preview analyser,
  SR4 feature analysis tool.
- **Design notes (SRD)** — the design rationale and conceptual spine.
- **Evidence (SRE)** — validation and test logs.
- **Papers (SRP)** — working papers and article skeletons.

The original source documents (`.md` and `.docx`) and the **benchmark/**
testing protocol live in `source/`. The benchmark is a reproducible-testing
scaffold (rubric, templates, model-comparison matrix) and is linked from the
site rather than rendered as pages.

## How it's built

The site is plain static HTML/CSS/JS in `docs/` — **no build step is required to
serve it**. GitHub Pages serves the `docs/` folder directly. A `.nojekyll` file is
included so Pages serves the files as-is.

The HTML was generated from the source files with `build/build.py`. The raw prompt
files live in `docs/prompts/` and are also embedded in each tool page, so the
**Copy prompt** buttons work whether or not the page can fetch.

### Publishing on GitHub Pages

1. Push this repo to `https://github.com/markbeachill/sports-reporter-tools`.
2. In the repo: **Settings → Pages**.
3. Under **Build and deployment**, set **Source: Deploy from a branch**.
4. Choose **Branch: `main`** and **Folder: `/docs`**, then **Save**.
5. The site publishes at the URL above (give it a minute on first deploy).

No Actions workflow or build command is needed.

## Note on the source README

The upstream `source/README.md` has a small copy-paste glitch: the SR4 bullet
was inserted inside the SR3 description. The site renders SR3 and SR4 correctly;
worth fixing in the source when convenient.
"""
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(txt)

def write_css():
    css = CSS
    with open(os.path.join(DOCS, "styles.css"), "w", encoding="utf-8") as f:
        f.write(css)

def write_js():
    with open(os.path.join(DOCS, "app.js"), "w", encoding="utf-8") as f:
        f.write(JS)

# CSS / JS loaded from sibling files
with open(os.path.join(os.path.dirname(__file__), "styles.css"), encoding="utf-8") as _f:
    CSS = _f.read()
with open(os.path.join(os.path.dirname(__file__), "app.js"), encoding="utf-8") as _f:
    JS = _f.read()

if __name__ == "__main__":
    build()
