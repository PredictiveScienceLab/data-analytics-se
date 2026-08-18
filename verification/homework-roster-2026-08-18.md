# Fall 2026 homework-roster verification

The student-facing Jupyter Book now contains exactly ten homework notebooks.
The roster is aligned with the syllabus dates and the holiday/exam-week
omissions.

| Homework | Coverage | Due date | Current state |
|---|---|---|---|
| 1 | Lectures 1–4 | Aug. 30 | Authored starter |
| 2 | Lectures 5–10 | Sept. 13 | Authored merged starter |
| 3 | Lectures 11–12 | Sept. 20 | Authored starter |
| 4 | Lectures 13–15 | Sept. 27 | Authored starter |
| 5 | Lectures 16–18 | Oct. 18 | Deliberate placeholder |
| 6 | Lectures 19–20 | Oct. 25 | Authored starter |
| 7 | Lectures 21–22 | Nov. 1 | Authored NIST Chwirut1 GP starter |
| 8 | Lecture 23 and model calibration | Nov. 15 | Deliberate placeholder |
| 9 | Lectures 24–25 | Nov. 22 | Authored starter |
| 10 | Lectures 26–28 | Dec. 6 | Deliberate placeholder; no PIV assumed |

Homework 11–13 were removed from the source directory, table of contents,
activity-link list, and clean HTML build. The superseded source drafts that
were useful for later consolidation remain in the instructor planning bank at
`planning/homework-bank/2026-08-18-13-set/`; they are not part of the book.

## Verification result

- All ten notebooks parse and pass `nbformat` validation.
- All ten starter notebooks execute successfully with Python 3.11 in the
  locked `uv` environment; the three placeholders contain no code cells.
- The classic Jupyter Book 0.15.1 clean build succeeds with 152 content pages.
- The one build warning is pre-existing: `lecture01/make_figs.ipynb` is built
  for URL compatibility but is not in the table of contents.
- The URL audit reports zero missing baseline pages, required homework pages,
  unexpected homework pages, activity pages, internal files, internal
  fragments, or legacy lecture anchors.
- The generated activity list contains 108 links and matches
  `activity_links.md` exactly.
- `git diff --check` passes.

## Reproduction

```bash
uv sync --locked
uv run --locked python tools/build_homework_notebooks.py
uv run --locked python tools/execute_notebooks.py lecturebook/homework
uv run --locked jupyter-book clean lecturebook --all
./make.sh
uv run --locked python tools/audit_site_urls.py
```
