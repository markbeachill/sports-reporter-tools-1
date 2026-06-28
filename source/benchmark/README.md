# Benchmark Folder

This folder is for testing the sports reporting prompt tools in a reproducible way.

The aim is to move beyond persuasive one-off runs and create a small evidence base showing what the tools reliably do, where they fail, and how different models behave when given the same text and same prompt.

## What belongs here

Add benchmark material only when it can be tested repeatedly. A case should include:

- the article or article excerpt being analysed;
- the article type, such as match report, match preview or feature;
- the sport and publication context if known;
- whether the sample is strong, weak or mixed;
- the tool being tested;
- expected diagnostic behaviours;
- known traps or failure risks;
- run logs from one or more AI models.

Do not include copyrighted full articles unless you have the right to store and share them in this archive. For third-party articles, prefer short excerpts, links, notes or separately stored private copies where appropriate.

## Suggested benchmark workflow

1. Add a new case using `case-template.md`.
2. Place the sample text or notes in `cases/`.
3. Run the relevant tool in a fresh chat with no prior project context.
4. Save the run output or a summary in `results/`.
5. Score the run using `scoring-rubric.md`.
6. Repeat with another model or another fresh chat.
7. Record observations in `run-log-template.md` or a case-specific log.

## Minimum useful benchmark set

A first benchmark set should contain at least:

- three match reports: strong, weak and mixed;
- three match previews: strong, weak and mixed;
- one beginner-level report for SR2;
- one article with an obvious live angle;
- one article where the tool may be tempted to overclaim;
- one case from a sport other than football;
- one case where cliché is present but not structurally important;
- one case where cliché carries the emotional burden of the piece.

When the project moves into sports feature writing, add feature cases separately rather than blending them into the match-report benchmark.

## Folder structure

- `cases/` — source texts, excerpts or case notes.
- `fixtures/` — stable prompt versions, rubrics or reference materials used during testing.
- `results/` — model outputs, run summaries and scoring notes.
- `case-template.md` — template for adding a new benchmark case.
- `run-log-template.md` — template for recording individual runs.
- `scoring-rubric.md` — suggested evaluation criteria.
- `model-comparison-matrix.md` — simple structure for comparing runs across models.
