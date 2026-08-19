# Notebook execution verification

> **Historical snapshot:** the homework-roster portion of this report was
> superseded on August 18, 2026. The current public release boundary is checked
> by `tools/check_public_homework.py`. The lecture-notebook execution result
> below remains the relevant full-lecture verification.

This verification used Python 3.11.15 and the dependencies in `uv.lock`.
Graphviz 15.1.1 supplied the external `dot` executable used by graph-rendering
notebooks.

## Result

- 99 of 99 lecture notebooks executed successfully from a clean disposable
  copy of the working tree.
- 13 of 13 homework notebooks are valid, intentionally title-only nbformat 4.5
  notebooks with no assignment content or code.
- The five execution batches and the targeted rerun together covered every
  tracked source notebook exactly as checked by repository-relative path.
- `uv lock --check`, `uv sync --locked --dry-run`, notebook JSON validation,
  Python syntax checks, and `git diff --check` passed.

Notebook execution used each notebook's parent directory as its working
directory. Bundled course datasets were read from `lecturebook/data`; OpenML
MNIST and Torchvision CIFAR-10 were downloaded during the disposable test.

The execution produced non-fatal NumPy 2 deprecation warnings in some Lecture
23 notebooks, GPyTorch jitter/negative-variance warnings in a few numerical
examples, and terminal progress bars where `IProgress` was unavailable. No
stored error output was accepted as a pass.

## Classic Jupyter Book

The locked Jupyter Book 0.15.1 build produced 155 content pages. The URL audit
confirmed all 150 pages from the frozen `fall2026-gh-pages-baseline`, all 111
current activity links, all internal files and fragments, and all legacy lecture
anchors. The final build had one intentional warning: the helper notebook
`lecture01/make_figs.ipynb` remains published for URL compatibility but is not
shown in the table of contents.

## Reproduction

```bash
uv sync --locked
uv run --locked python tools/execute_notebooks.py \
  --timeout 7200 \
  --report notebook-execution-report.json
```

Use `--in-place` only when refreshed outputs should be written. The published
figure refresh was limited to the visual cells documented in
`planning/visual-output-refresh.json`, preserving unrelated historical outputs
and keeping the review focused.
