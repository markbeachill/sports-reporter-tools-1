# Sports Reporting AI Tools

This folder contains a small toolkit and research archive for AI-supported sports journalism teaching. The central aim is not to make AI write sports journalism on behalf of students, but to help writers see how their sports writing works on a reader.

The project currently contains three runnable prompt tools and a set of supporting design, evidence and working-paper documents.

## Core idea

The project starts from a craft claim: sports writing is not only the transmission of facts about a match, athlete or competition. It is a managed reader experience. A good sports report, preview or feature gives the reader a way to care, understand, remember, judge or talk about what has happened or what is about to happen.

The project’s recurring concepts are:

- **reader journey**: what the reader is led to know, feel, expect and care about as the piece develops;
- **attachment**: the way sports writing recruits the reader into a team, person, rivalry, place, pressure or narrative line;
- **economy**: the discipline of making each word do useful work, especially in compressed match reporting;
- **voice as fine-grain economy**: the idea that voice is not decoration but phrase-level spending;
- **social currency**: what a piece gives the reader to say, share, argue or carry away;
- **safe arena**: the idea that sport creates a space where intense feeling can be experienced, narrated and contested without being the same kind of consequence-bearing public matter as politics, law or disaster reporting.

## Numbering system

The archive uses four document streams.

- **SR1–SR3**: runnable prompt tools.
- **SRD**: Sports Reporting Design papers and working notes.
- **SRE**: Sports Reporting Evidence, validation and test logs.
- **SRP**: Sports Reporting Papers, skeletons and article-level drafts.

This keeps practical tools, design rationale, testing evidence and publishable papers separate while preserving their development sequence.

## Contents

### Prompt tools

- **SR1-match-report-analyser-v0.6.md**  
  Expert-facing analyser for match reports. It examines reader journey, attachment, economy and voice, and gives diagnostic feedback without rewriting the piece.

- **SR2-match-report-coach-beginner-route-v0.2.md**  
  Beginner-facing coaching tool. It silently analyses broadly but teaches one reachable move clearly, rather than overwhelming a novice writer with full expert critique.

- **SR3-match-preview-analyser-v0.5-beta.md**  
- `SR4-feature-analysis-tool-v0.1.md` — beta feature analysis tool. Reads a pasted feature or sports feature, identifies its form and feature promise, and traces the reader journey from curiosity to meaning. Gives one teachable move by default.
  Beta analyser for match previews. It asks what the preview gives the reader before the event: a reason to care, a frame for understanding, and/or social currency.

### Design and theory notes

- **SRD-01-ai-sports-journalism-writing-tutor-design-rationale.docx**  
  Foundation note explaining why a sports journalism tutor needs domain-specific craft assumptions rather than a generic writing rubric.

- **SRD-02-readers-journey-attachment-and-economy.docx**  
  Develops the reader-journey model and the linked concepts of attachment and economy.

- **SRD-03-important-because-it-isnt-conceptual-spine.docx**  
  Sets out the project’s central conceptual claim about sport as an arena for intense but differently consequential feeling.

- **SRD-04-voice-fine-grain-of-economy-cliche-test.docx**  
  Adds voice to the model by treating phrase-level choices, cliché and live detail as matters of economy.

- **SRD-05-teaching-not-coaching-sr2-beginner-route.docx**  
  Explains why the beginner tool has to teach one useful move rather than present a shortened expert analysis.

- **SRD-06-preview-pull-before-event-social-currency.docx**  
  Extends the model from match reports to previews, where the reader is asked to pre-live an event and carry something into the match.

### Evidence and paper drafts

- **SRE-01-sr1-match-report-analyser-test-log.docx**  
  Early validation and test log for SR1, including caveats about priming, model-family effects and the need for cold re-testing.

- **SRP-01-important-because-it-isnt-paper-skeleton.docx**  
  Skeleton for a theoretical paper based on the project’s central conceptual claim.

- **SRP-02-previewing-the-unplayed-match-working-paper.docx**  
  Working paper on preview writing and the development of SR3. This is currently the most self-contained article-level document in the set.

## Recommended reading order

Read the archive in this order if you want the development story:

1. SRD-01 — AI sports journalism writing tutor design rationale
2. SRD-02 — Reader journey, attachment and economy
3. SRD-03 — Important Because It Isn’t
4. SRD-04 — Voice as fine-grain economy
5. SR1 — Match Report Analyser
6. SRE-01 — SR1 test log
7. SRD-05 — Teaching, Not Coaching
8. SR2 — Match Report Coach, beginner route
9. SRD-06 — Preview, pull and social currency
10. SR3 — Match Preview Analyser
11. SRP-01 — Important Because It Isn’t paper skeleton
12. SRP-02 — Previewing the Unplayed Match

## How to use the tools

For each tool, open the relevant Markdown prompt and paste it into an AI assistant. Then paste the student or sample article when requested. The tool should treat the pasted text as its evidence base and should not invent match facts, quotes, sources or background.

Suggested use:

- use **SR1** when the writer can handle full diagnostic analysis;
- use **SR2** with beginners or when the teaching aim is one practical next move;
- use **SR3** for previews rather than reports;
- log notable runs in the `benchmark` folder when testing tool performance.

## Ethical and editorial boundaries

These tools are intended for analysis, teaching and revision guidance. They are not intended to fabricate reporting. They should not invent facts, quotes, scenes, interviews, sources, statistics or match details. When a tool would need external verification, that need should be stated rather than silently filled in.

The tools should help the writer improve judgement. They should not take ownership of the student’s article.

## Benchmarking status

The `benchmark` folder contains a protocol, templates and scoring rubric for future validation. It does not contain live benchmark cases yet. Cases should be added only when the sample article, expected diagnostic behaviours and run conditions are documented clearly enough for repeat testing.

A useful benchmark set should include strong, weak and mixed examples across match reports, previews and later feature-writing pieces. It should also include samples from more than one sport, writing level and publication context.

## Current status

This is a strong beta-stage toolkit and practice-led research project. The craft theory is more developed than the evidence base. The next step is to make testing reproducible by adding benchmark cases, cold runs, model comparisons and expert judgement notes.
