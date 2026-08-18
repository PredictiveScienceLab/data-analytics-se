#!/usr/bin/env python3
"""Migrate the Fall 2026 homework drafts from thirteen slots to ten.

This is a one-time, content-preserving migration.  It snapshots the affected
thirteen-homework drafts in ``planning/homework-bank`` before changing the
student-facing notebooks.  The active book contains Homework 1--10 only.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
import re
import shutil

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
HOMEWORK = ROOT / "lecturebook" / "homework"
BANK = ROOT / "planning" / "homework-bank" / "2026-08-18-13-set"


def read_notebook(number: int) -> nbf.NotebookNode:
    return nbf.read(HOMEWORK / f"homework-{number:02d}.ipynb", as_version=4)


def source_text(cell: nbf.NotebookNode) -> str:
    source = cell.source
    return "".join(source) if isinstance(source, list) else source


def reset_cell_ids(notebook: nbf.NotebookNode, number: int) -> None:
    for index, cell in enumerate(notebook.cells):
        token = f"homework-{number:02d}-{index}-{cell.cell_type}".encode()
        cell.id = hashlib.sha1(token).hexdigest()[:8]


def retarget(
    notebook: nbf.NotebookNode,
    *,
    old_number: int,
    new_number: int,
    title: str,
    coverage: str,
    due: str,
) -> nbf.NotebookNode:
    notebook = deepcopy(notebook)
    opening = source_text(notebook.cells[0])
    opening = re.sub(
        r"^# Homework \d+ — .*?$",
        f"# Homework {new_number} — {title}",
        opening,
        count=1,
        flags=re.MULTILINE,
    )
    opening = re.sub(
        r"^\*\*Coverage:\*\* .*?  $",
        f"**Coverage:** {coverage}  ",
        opening,
        count=1,
        flags=re.MULTILINE,
    )
    opening = re.sub(
        r"^\*\*Due:\*\* .*?, 11:59 p\.m\. ET  $",
        f"**Due:** {due}, 11:59 p.m. ET  ",
        opening,
        count=1,
        flags=re.MULTILINE,
    )
    notebook.cells[0].source = opening

    old_seed = f"539{old_number:02d}"
    new_seed = f"539{new_number:02d}"
    if old_seed != new_seed:
        for cell in notebook.cells:
            cell.source = source_text(cell).replace(old_seed, new_seed)

    reset_cell_ids(notebook, new_number)
    nbf.validate(notebook)
    return notebook


def placeholder(
    number: int, title: str, coverage: str, due: str
) -> nbf.NotebookNode:
    cell = nbf.v4.new_markdown_cell(
        f"""# Homework {number} — {title}

**Coverage:** {coverage}<br>
**Due:** {due}, 11:59 p.m. ET
"""
    )
    notebook = nbf.v4.new_notebook(cells=[cell], metadata={})
    reset_cell_ids(notebook, number)
    nbf.validate(notebook)
    return notebook


def merged_homework_02(
    old_02: nbf.NotebookNode, old_03: nbf.NotebookNode
) -> nbf.NotebookNode:
    # Keep one 25-point manual problem and one 75-point computational study.
    # This avoids concatenating two complete 100-point assignments.
    opening = deepcopy(old_03.cells[0])
    setup = deepcopy(old_03.cells[1])
    random_vector_math = deepcopy(old_02.cells[2:4])
    oscillator_study = deepcopy(old_03.cells[4:])
    notebook = nbf.v4.new_notebook(
        cells=[opening, setup, *random_vector_math, *oscillator_study],
        metadata=deepcopy(old_03.metadata),
    )
    return retarget(
        notebook,
        old_number=3,
        new_number=2,
        title="Random Vectors and Monte Carlo Uncertainty Propagation",
        coverage="Lectures 5–10",
        due="Sunday, September 13, 2026",
    )


def archive_sources() -> None:
    if BANK.exists():
        raise FileExistsError(
            f"Archive already exists: {BANK}. Refusing to overwrite it."
        )
    BANK.mkdir(parents=True)
    for number in (2, 3, 6, 7, 10, 12, 13):
        shutil.copy2(
            HOMEWORK / f"homework-{number:02d}.ipynb",
            BANK / f"homework-{number:02d}.ipynb",
        )
    shutil.copy2(
        ROOT / "planning" / "homework-redesign-blueprint.md",
        BANK / "homework-redesign-blueprint.md",
    )
    shutil.copy2(
        ROOT / "tools" / "build_homework_notebooks.py",
        BANK / "build_homework_notebooks.py",
    )
    (BANK / "README.md").write_text(
        """# Thirteen-homework draft bank

This directory preserves the affected, uncommitted thirteen-homework drafts
as they existed immediately before the Fall 2026 course changed to ten
assignments. These files are instructor planning artifacts and are not part of
the student-facing Jupyter Book.

The bank retains the two source assignments merged into new Homework 2, the
complete classification/clustering and sampling/VI drafts that require later
consolidation, and the three title-only held assignments.
""",
        encoding="utf-8",
    )


def write_notebook(number: int, notebook: nbf.NotebookNode) -> None:
    path = HOMEWORK / f"homework-{number:02d}.ipynb"
    nbf.write(notebook, path)
    print(f"Wrote {path.relative_to(ROOT)} ({len(notebook.cells)} cells)")


def main() -> None:
    originals = {number: read_notebook(number) for number in range(1, 14)}
    archive_sources()

    active = {
        1: retarget(
            originals[1], old_number=1, new_number=1,
            title="Probability and Mechanical Reliability",
            coverage="Lectures 1–4", due="Sunday, August 30, 2026",
        ),
        2: merged_homework_02(originals[2], originals[3]),
        3: retarget(
            originals[4], old_number=4, new_number=3,
            title="Prior Information and Bayesian Earthquake Rates",
            coverage="Lectures 11–12", due="Sunday, September 20, 2026",
        ),
        4: retarget(
            originals[5], old_number=5, new_number=4,
            title="Least Squares and Bayesian Elastic-Modulus Inference",
            coverage="Lectures 13–15", due="Sunday, September 27, 2026",
        ),
        5: placeholder(
            5, "Classification, Clustering, and Dimensionality Reduction",
            "Lectures 16–18", "Sunday, October 18, 2026",
        ),
        6: retarget(
            originals[8], old_number=8, new_number=6,
            title="State-Space Models and Kalman Filtering",
            coverage="Lectures 19–20", due="Sunday, October 25, 2026",
        ),
        7: retarget(
            originals[9], old_number=9, new_number=7,
            title="Gaussian-Process Prediction for NIST Ultrasonic Calibration",
            coverage="Lectures 21–22", due="Sunday, November 1, 2026",
        ),
        8: placeholder(
            8, "Bayesian Optimization for Model Calibration",
            "Lecture 23 and assigned model-calibration material",
            "Sunday, November 15, 2026",
        ),
        9: retarget(
            originals[11], old_number=11, new_number=9,
            title="Deep Neural-Network Regression",
            coverage="Lectures 24–25", due="Sunday, November 22, 2026",
        ),
        10: placeholder(
            10, "Physics-Informed Modeling and Posterior Characterization",
            "Lectures 26–28", "Sunday, December 6, 2026",
        ),
    }
    assert set(active) == set(range(1, 11))
    for number, notebook in active.items():
        write_notebook(number, notebook)

    for number in range(11, 14):
        path = HOMEWORK / f"homework-{number:02d}.ipynb"
        path.unlink()
        print(f"Removed {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
