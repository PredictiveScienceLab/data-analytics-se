#!/usr/bin/env python3
"""Execute Jupyter notebooks reproducibly with the active uv environment."""

from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import traceback

import nbformat
from nbclient import NotebookClient


SPLIT_MIME_TYPES = {"application/javascript", "image/svg+xml"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Execute notebooks with the current Python interpreter. Run this "
            "through `uv run --locked python tools/execute_notebooks.py`."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Notebook files or directories (default: lecturebook).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=7_200,
        help="Maximum seconds per code cell (default: 7200).",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Write outputs back only for notebooks that execute successfully.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("notebook-execution-report.json"),
        help="JSON report path.",
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop after the first failing notebook.",
    )
    return parser.parse_args()


def discover_notebooks(paths: list[Path]) -> list[Path]:
    requested = paths or [Path("lecturebook")]
    notebooks: set[Path] = set()
    for requested_path in requested:
        path = requested_path.resolve()
        if path.is_file():
            if path.suffix != ".ipynb":
                raise ValueError(f"Not a notebook: {requested_path}")
            notebooks.add(path)
            continue
        if not path.is_dir():
            raise FileNotFoundError(requested_path)
        for notebook in path.rglob("*.ipynb"):
            if "_build" not in notebook.parts and ".ipynb_checkpoints" not in notebook.parts:
                notebooks.add(notebook.resolve())
    return sorted(notebooks)


def configure_kernel(runtime_root: Path) -> None:
    data_dir = runtime_root / "jupyter"
    runtime_dir = runtime_root / "runtime"
    ipython_dir = runtime_root / "ipython"
    matplotlib_dir = runtime_root / "matplotlib"
    kernel_dir = data_dir / "kernels" / "python3"
    for directory in (runtime_dir, ipython_dir, matplotlib_dir, kernel_dir):
        directory.mkdir(parents=True, exist_ok=True)

    os.environ["JUPYTER_DATA_DIR"] = str(data_dir)
    os.environ["JUPYTER_RUNTIME_DIR"] = str(runtime_dir)
    os.environ["IPYTHONDIR"] = str(ipython_dir)
    os.environ["MPLCONFIGDIR"] = str(matplotlib_dir)
    os.environ.setdefault("MPLBACKEND", "Agg")

    kernel = {
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "Python (uv locked environment)",
        "language": "python",
    }
    (kernel_dir / "kernel.json").write_text(json.dumps(kernel, indent=2) + "\n")


def _split_mimebundle(bundle: dict[str, object]) -> None:
    for mime_type, value in list(bundle.items()):
        if isinstance(value, str) and (
            mime_type.startswith("text/") or mime_type in SPLIT_MIME_TYPES
        ):
            bundle[mime_type] = value.splitlines(keepends=True)


def serialize_notebook(notebook: nbformat.NotebookNode) -> str:
    """Preserve string cell sources while keeping multiline outputs diffable."""
    serializable = copy.deepcopy(notebook)
    for cell in serializable.cells:
        for attachment in cell.get("attachments", {}).values():
            _split_mimebundle(attachment)
        if cell.cell_type != "code":
            continue
        for output in cell.get("outputs", []):
            if output.output_type in {"execute_result", "display_data"}:
                _split_mimebundle(output.get("data", {}))
            elif output.output_type == "stream" and isinstance(output.text, str):
                output.text = output.text.splitlines(keepends=True)
    return nbformat.writes(serializable, version=4, split_lines=False)


def execute_one(path: Path, timeout: int, in_place: bool) -> dict[str, object]:
    started = time.monotonic()
    notebook = nbformat.read(path, as_version=4)
    if not notebook.cells:
        return {
            "path": str(path),
            "status": "empty",
            "seconds": round(time.monotonic() - started, 3),
        }
    if not any(cell.cell_type == "code" for cell in notebook.cells):
        return {
            "path": str(path),
            "status": "passed",
            "note": "no code cells",
            "seconds": round(time.monotonic() - started, 3),
        }

    client = NotebookClient(
        notebook,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
        record_timing=False,
        allow_errors=False,
    )
    client.execute()

    if in_place:
        serialized = serialize_notebook(notebook)
        path.write_text(serialized + ("" if serialized.endswith("\n") else "\n"))

    return {
        "path": str(path),
        "status": "passed",
        "seconds": round(time.monotonic() - started, 3),
    }


def main() -> int:
    args = parse_args()
    notebooks = discover_notebooks(args.paths)
    if not notebooks:
        raise SystemExit("No notebooks found.")

    results: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="data-analytics-notebooks-") as runtime:
        configure_kernel(Path(runtime))
        total = len(notebooks)
        for index, notebook in enumerate(notebooks, start=1):
            print(f"[{index}/{total}] {notebook}", flush=True)
            try:
                result = execute_one(notebook, args.timeout, args.in_place)
                print(
                    f"  {result['status']} in {result['seconds']} seconds",
                    flush=True,
                )
            except Exception as exc:  # keep auditing after a notebook failure
                result = {
                    "path": str(notebook),
                    "status": "failed",
                    "seconds": None,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                }
                print(f"  failed: {type(exc).__name__}: {exc}", flush=True)
            results.append(result)
            if result["status"] == "failed" and args.stop_on_error:
                break

    counts = {
        status: sum(result["status"] == status for result in results)
        for status in ("passed", "empty", "failed")
    }
    report = {
        "python": sys.executable,
        "timeout_seconds_per_cell": args.timeout,
        "in_place": args.in_place,
        "counts": counts,
        "results": results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Report: {args.report}")
    print(json.dumps(counts, sort_keys=True))
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
