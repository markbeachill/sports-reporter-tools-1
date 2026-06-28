# Sports Reporter Tools

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
