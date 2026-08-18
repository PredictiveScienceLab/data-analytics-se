#!/usr/bin/env python3
"""Refresh only visual outputs while preserving review-friendly notebook history."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

import nbformat

from execute_notebooks import serialize_notebook


def notebook_at_ref(ref: str, path: Path) -> nbformat.NotebookNode:
    payload = subprocess.run(
        ["git", "show", f"{ref}:{path.as_posix()}"],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout
    return nbformat.reads(payload.decode(), as_version=4)


def is_visual(output: nbformat.NotebookNode) -> bool:
    data = output.get("data", {})
    return any(mime_type.startswith("image/") for mime_type in data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebooks", nargs="+", type=Path)
    parser.add_argument("--executed-root", type=Path, required=True)
    parser.add_argument("--baseline-ref", default="fall2026-github-baseline")
    parser.add_argument("--output-base-ref", default="HEAD")
    parser.add_argument(
        "--plan",
        type=Path,
        help="JSON object mapping notebook paths to visual-output cell indices.",
    )
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text()) if args.plan else {}

    summary: list[dict[str, object]] = []
    for path in args.notebooks:
        baseline = notebook_at_ref(args.baseline_ref, path)
        output_base = notebook_at_ref(args.output_base_ref, path)
        current = nbformat.read(path, as_version=4)
        executed = nbformat.read(args.executed_root / path, as_version=4)

        lengths = {len(baseline.cells), len(output_base.cells), len(current.cells), len(executed.cells)}
        if len(lengths) != 1:
            raise ValueError(f"Cell-count mismatch in {path}: {sorted(lengths)}")
        if [cell.source for cell in current.cells] != [cell.source for cell in executed.cells]:
            raise ValueError(f"Executed sources do not match the working tree: {path}")

        changed_code_cells = [
            index
            for index, (before, after) in enumerate(zip(baseline.cells, output_base.cells))
            if before.cell_type == after.cell_type == "code" and before.source != after.source
        ]
        if not changed_code_cells:
            raise ValueError(f"No visual-source change found relative to baseline: {path}")
        planned_cells = plan.get(path.as_posix())
        if planned_cells is None:
            planned_cells = [
                index
                for index in changed_code_cells
                if any(is_visual(output) for output in executed.cells[index].get("outputs", []))
            ]
        planned_cells = sorted(set(planned_cells))
        if not planned_cells:
            raise ValueError(f"No visual outputs selected for refresh: {path}")

        refreshed_cells = 0
        refreshed_outputs = 0
        for index, (target_cell, source_cell, executed_cell) in enumerate(
            zip(output_base.cells, current.cells, executed.cells)
        ):
            target_cell.source = source_cell.source
            if target_cell.cell_type != "code" or index not in planned_cells:
                continue
            visuals = [output for output in executed_cell.get("outputs", []) if is_visual(output)]
            if not visuals:
                continue
            nonvisual = [output for output in target_cell.get("outputs", []) if not is_visual(output)]
            target_cell.outputs = nonvisual + visuals
            refreshed_cells += 1
            refreshed_outputs += len(visuals)

        rendered = serialize_notebook(output_base)
        path.write_text(rendered + ("" if rendered.endswith("\n") else "\n"))
        summary.append(
            {
                "path": str(path),
                "source_changed_cells": changed_code_cells,
                "planned_visual_cells": planned_cells,
                "refreshed_cells": refreshed_cells,
                "refreshed_visual_outputs": refreshed_outputs,
            }
        )

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
