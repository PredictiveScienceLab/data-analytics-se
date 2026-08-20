#!/usr/bin/env python3
"""Reject unreleased homework or instructor solutions in the public tree."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys


APPROVED_HOMEWORK = {1, 2}
APPROVED_SHA256 = {
    1: "c010bfb755c693dd6058b900e27ddf45364afc7954bcf7b5622da3a77c1ffac3",
    2: "c5d85eb4cb2e51c81cc39c9341aded1131e2ecf0db507d214de4498b3c4a681b",
}
PUBLIC_HOMEWORK_ASSETS = {
    2: {
        "source": "lecturebook/data/homework/hw02_noaa_45007_2023_hourly.csv",
        "pages": (
            "_downloads/2747cd8e6187fc0555eae6d9570930fa/"
            "hw02_noaa_45007_2023_hourly.csv"
        ),
        "sha256": (
            "bfbe16098966b9c368e59e8c690f6b52"
            "fa38b97331cfe253b6a8d3c9fd66fe43"
        ),
    },
}
PUBLIC_HOMEWORK_DATA = {
    asset["source"]: asset["sha256"]
    for asset in PUBLIC_HOMEWORK_ASSETS.values()
}
PUBLIC_HOMEWORK_PAGES_DATA = {
    asset["pages"]: asset["sha256"]
    for asset in PUBLIC_HOMEWORK_ASSETS.values()
}
EXPECTED_HOMEWORK = set(range(1, 11))
HOMEWORK_PATH = re.compile(
    r"^lecturebook/homework/homework-(?P<number>\d{2})\.ipynb$"
)
PRIVATE_PATH_TOKEN = re.compile(
    r"solutions?|answer[-_ ]?keys?|instructor[-_ ]?keys?",
    re.IGNORECASE,
)
NUMBERED_HOMEWORK_ARTIFACT = re.compile(
    r"(?:homework|hw)[-_ ]?0*(?P<number>\d{1,2})(?=[^0-9]|$)",
    re.IGNORECASE,
)
PRIVATE_NOTEBOOK_TAGS = {
    "solution",
    "solutions",
    "answer-key",
    "instructor-key",
    "instructor-solution",
}
PRIVATE_SOURCE_MARKERS = (
    re.compile(r"^#{1,6}\s+(?:instructor\s+)?solutions?\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^#{1,6}\s+answer\s+key\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*(?:#\s*)?(?:BEGIN|END)\s+SOLUTION\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*\*\*Solution:\*\*", re.IGNORECASE | re.MULTILINE),
)
FORBIDDEN_AUTHORING_PATHS = {
    "planning/codex-homework-progression.md",
    "planning/genai-human-learning-evidence-review.md",
    "planning/homework-01-tentative.md",
    "planning/homework-redesign-blueprint.md",
    "tools/build_homework_notebooks.py",
    "tools/migrate_homework_to_ten.py",
    "tools/prepare_homework_data.py",
    "verification/homework-roster-2026-08-18.md",
}
FORBIDDEN_AUTHORING_PREFIXES = (
    "lecturebook/data/homework/",
    "planning/homework-bank/",
)
FORBIDDEN_PRIVATE_COMPONENTS = {
    "approved-homework-solutions",
    "homework-bank",
    "homework-unpublished",
    "student-drafts",
    "ta-approved-solutions",
}
ALLOWED_HOMEWORK_DIRECTORY_PATHS = {
    "lecturebook/homework/intro.md",
    *{
        f"lecturebook/homework/homework-{number:02d}.ipynb"
        for number in EXPECTED_HOMEWORK
    },
}
ALLOWED_NUMBERED_SOURCE_PATHS = (
    ALLOWED_HOMEWORK_DIRECTORY_PATHS | set(PUBLIC_HOMEWORK_DATA)
)
PAGES_HOMEWORK_SOURCE_PATH = re.compile(
    r"^_sources/homework/homework-(?P<number>\d{2})\.ipynb$"
)
ALLOWED_PAGES_HOMEWORK_SOURCE_PATHS = {
    "_sources/homework/intro.md",
    *{
        f"_sources/homework/homework-{number:02d}.ipynb"
        for number in EXPECTED_HOMEWORK
    },
}
ALLOWED_PAGES_HOMEWORK_HTML_PATHS = {
    "homework/intro.html",
    *{
        f"homework/homework-{number:02d}.html"
        for number in EXPECTED_HOMEWORK
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit the public homework release boundary."
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--index",
        action="store_true",
        help="Audit the staged Git index (for pre-commit checks).",
    )
    source.add_argument(
        "--ref",
        help="Audit a committed Git reference, such as HEAD.",
    )
    source.add_argument(
        "--pages-ref",
        help="Audit a committed gh-pages reference.",
    )
    source.add_argument(
        "--pages-directory",
        type=Path,
        help="Audit a generated Jupyter Book HTML directory before publication.",
    )
    return parser.parse_args()


def run_git(*arguments: str) -> bytes:
    return subprocess.check_output(("git", *arguments))


class RepositoryView:
    def __init__(self, *, use_index: bool, ref: str | None):
        self.use_index = use_index
        self.ref = ref

    def paths(self) -> list[str]:
        if self.ref:
            payload = run_git("ls-tree", "-r", "-z", "--name-only", self.ref)
        else:
            payload = run_git("ls-files", "-z", "--cached")
        paths = {item.decode() for item in payload.split(b"\0") if item}
        if not self.ref and not self.use_index:
            excluded_directories = {
                ".git",
                ".ipynb_checkpoints",
                ".venv",
                "__pycache__",
                "_build",
            }
            for directory, child_directories, filenames in os.walk("."):
                child_directories[:] = [
                    name
                    for name in child_directories
                    if name not in excluded_directories
                ]
                for filename in filenames:
                    path = Path(directory, filename).relative_to(".").as_posix()
                    paths.add(path)
        return sorted(paths)

    def read(self, path: str) -> bytes:
        if self.ref:
            return run_git("show", f"{self.ref}:{path}")
        if self.use_index:
            return run_git("show", f":{path}")
        return Path(path).read_bytes()


class DirectoryView:
    def __init__(self, root: Path):
        self.root = root

    def paths(self) -> list[str]:
        return sorted(
            path.relative_to(self.root).as_posix()
            for path in self.root.rglob("*")
            if path.is_file()
        )

    def read(self, path: str) -> bytes:
        return (self.root / path).read_bytes()


def source_text(cell: dict[str, object]) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(str(line) for line in source)
    return str(source)


def normalized_tag(tag: object) -> str:
    return re.sub(r"[ _]+", "-", str(tag).strip().lower())


def private_metadata_key(value: object) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if PRIVATE_PATH_TOKEN.search(normalized_tag(key)) and bool(child):
                return True
            if private_metadata_key(child):
                return True
    elif isinstance(value, list):
        return any(private_metadata_key(child) for child in value)
    return False


def audit_private_content(
    *, path: str, payload: bytes, errors: list[str]
) -> None:
    suffix = Path(path).suffix.lower()
    if suffix == ".md":
        try:
            text = payload.decode()
        except UnicodeDecodeError as error:
            errors.append(f"{path}: invalid UTF-8 Markdown: {error}")
            return
        for marker in PRIVATE_SOURCE_MARKERS:
            if marker.search(text):
                errors.append(f"{path}: contains a solution marker")
                break
        return
    if suffix != ".ipynb":
        return

    try:
        notebook = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        errors.append(f"{path}: invalid notebook JSON: {error}")
        return
    if private_metadata_key(notebook.get("metadata", {})):
        errors.append(f"{path}: notebook metadata contains a private solution key")
    for cell_index, cell in enumerate(notebook.get("cells", [])):
        metadata = cell.get("metadata", {})
        if private_metadata_key(metadata):
            errors.append(
                f"{path}: cell {cell_index} metadata contains a private solution key"
            )
        tags = metadata.get("tags", [])
        for tag in tags:
            normalized = normalized_tag(tag)
            if (
                normalized in PRIVATE_NOTEBOOK_TAGS
                or PRIVATE_PATH_TOKEN.search(normalized)
            ):
                errors.append(
                    f"{path}: cell {cell_index} has private tag {tag!r}"
                )
        text = source_text(cell)
        for marker in PRIVATE_SOURCE_MARKERS:
            if marker.search(text):
                errors.append(
                    f"{path}: cell {cell_index} contains a solution marker"
                )
                break


def audit_notebook(
    *, number: int, path: str, payload: bytes, errors: list[str]
) -> None:
    expected_digest = APPROVED_SHA256.get(number)
    if expected_digest is not None:
        actual_digest = hashlib.sha256(payload).hexdigest()
        if actual_digest != expected_digest:
            errors.append(
                f"{path}: approved notebook SHA-256 changed; "
                "review and update the release allowlist deliberately"
            )
    try:
        notebook = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        errors.append(f"{path}: invalid notebook JSON: {error}")
        return

    cells = notebook.get("cells")
    if not isinstance(cells, list) or not cells:
        errors.append(f"{path}: notebook must contain at least one cell")
        return

    first = cells[0]
    if first.get("cell_type") != "markdown":
        errors.append(f"{path}: first cell must be Markdown")
        return
    expected_title = f"# Homework {number}"
    first_source = source_text(first)
    first_lines = first_source.splitlines()
    if not first_lines or first_lines[0] != expected_title:
        errors.append(f"{path}: title must be exactly {expected_title!r}")

    if number not in APPROVED_HOMEWORK:
        if len(cells) != 1:
            errors.append(f"{path}: unreleased homework must have exactly one cell")
        if first_source != expected_title + "\n":
            errors.append(
                f"{path}: unreleased homework must contain only {expected_title!r}"
            )
        if first.get("metadata", {}) != {}:
            errors.append(f"{path}: unreleased title cell metadata must be empty")
        if first.get("attachments", {}) != {}:
            errors.append(f"{path}: unreleased title cell attachments must be empty")
    elif len(cells) == 1:
        errors.append(f"{path}: approved homework has no assignment content")

    homework_titles = 0
    for cell_index, cell in enumerate(cells):
        text = source_text(cell)
        homework_titles += len(
            re.findall(r"^#\s+Homework\s+\d+\s*$", text, re.MULTILINE)
        )
        if cell.get("cell_type") == "code":
            if cell.get("execution_count") is not None:
                errors.append(f"{path}: cell {cell_index} has an execution count")
            if cell.get("outputs", []):
                errors.append(f"{path}: cell {cell_index} contains stored output")
    if homework_titles != 1:
        errors.append(
            f"{path}: expected one exact level-one Homework title, found {homework_titles}"
        )


def audit_source_view(view: RepositoryView) -> list[str]:
    paths = view.paths()
    errors: list[str] = []
    if not APPROVED_HOMEWORK <= EXPECTED_HOMEWORK:
        errors.append("approved homework numbers must belong to the public roster")
    if set(APPROVED_SHA256) != APPROVED_HOMEWORK:
        errors.append("every approved homework must have exactly one pinned SHA-256")
    if not set(PUBLIC_HOMEWORK_ASSETS) <= APPROVED_HOMEWORK:
        errors.append("public homework data must belong to an approved homework")

    for path in paths:
        if PRIVATE_PATH_TOKEN.search(path):
            errors.append(f"private solution/key path is present: {path}")
        path_components = {component.lower() for component in Path(path).parts}
        if FORBIDDEN_PRIVATE_COMPONENTS.intersection(path_components):
            errors.append(f"private homework directory is present: {path}")
        if path in FORBIDDEN_AUTHORING_PATHS or (
            path.startswith(FORBIDDEN_AUTHORING_PREFIXES)
            and path not in PUBLIC_HOMEWORK_DATA
        ):
            errors.append(f"private homework authoring path is present: {path}")
        if (
            path.startswith("lecturebook/homework/")
            and path not in ALLOWED_HOMEWORK_DIRECTORY_PATHS
        ):
            errors.append(f"unexpected public homework-directory path: {path}")
        if (
            NUMBERED_HOMEWORK_ARTIFACT.search(path)
            and path not in ALLOWED_NUMBERED_SOURCE_PATHS
        ):
            errors.append(f"numbered homework artifact is outside its public path: {path}")

    for path, expected_digest in PUBLIC_HOMEWORK_DATA.items():
        if path not in paths:
            errors.append(f"missing approved homework data file: {path}")
            continue
        actual_digest = hashlib.sha256(view.read(path)).hexdigest()
        if actual_digest != expected_digest:
            errors.append(f"approved homework data SHA-256 changed: {path}")

    for path in paths:
        if Path(path).suffix.lower() in {".ipynb", ".md"}:
            audit_private_content(
                path=path,
                payload=view.read(path),
                errors=errors,
            )

    homework_paths: dict[int, str] = {}
    for path in paths:
        match = HOMEWORK_PATH.fullmatch(path)
        if match:
            number = int(match.group("number"))
            homework_paths[number] = path

    actual = set(homework_paths)
    if actual != EXPECTED_HOMEWORK:
        missing = sorted(EXPECTED_HOMEWORK - actual)
        extra = sorted(actual - EXPECTED_HOMEWORK)
        errors.append(f"homework roster mismatch: missing={missing}, extra={extra}")

    for number, path in sorted(homework_paths.items()):
        audit_notebook(
            number=number,
            path=path,
            payload=view.read(path),
            errors=errors,
        )

    return errors


def rendered_h1_titles(payload: bytes) -> list[str]:
    try:
        text = payload.decode()
    except UnicodeDecodeError:
        return []
    titles: list[str] = []
    for match in re.finditer(
        r"<h1(?:\s[^>]*)?>(.*?)</h1>", text, re.DOTALL | re.IGNORECASE
    ):
        title = re.sub(r"<[^>]+>", "", match.group(1))
        title = html.unescape(title)
        title = re.sub(r"\s+", " ", title).strip().removesuffix("#").strip()
        titles.append(title)
    return titles


def unreleased_page_is_title_only(payload: bytes, number: int) -> bool:
    try:
        text = payload.decode()
    except UnicodeDecodeError:
        return False
    article_match = re.search(
        r'<article\s+class="bd-article">(.*?)</article>',
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if article_match is None:
        return False
    article = re.sub(
        r"<script\b[^>]*>.*?</script>",
        "",
        article_match.group(1),
        flags=re.DOTALL | re.IGNORECASE,
    )
    section_match = re.search(
        rf'<section\b[^>]*\bid="homework-{number}"[^>]*>(.*?)</section>',
        article,
        re.DOTALL | re.IGNORECASE,
    )
    if section_match is None:
        return False
    outside_section = article[: section_match.start()] + article[section_match.end() :]
    if outside_section.strip():
        return False
    expected_h1 = re.compile(
        rf"\s*<h1>\s*Homework {number}\s*"
        r"<a\b[^>]*>\s*(?:#|¶)\s*</a>\s*</h1>\s*",
        re.DOTALL | re.IGNORECASE,
    )
    return expected_h1.fullmatch(section_match.group(1)) is not None


def search_index_document_ids(value: object) -> set[int]:
    if isinstance(value, int):
        return {value}
    if isinstance(value, list):
        return {item for item in value if isinstance(item, int)}
    return set()


def audit_pages_search_index(
    view: RepositoryView | DirectoryView, paths: list[str], errors: list[str]
) -> None:
    path = "searchindex.js"
    if path not in paths:
        errors.append("missing Pages search index: searchindex.js")
        return
    try:
        text = view.read(path).decode().strip()
    except UnicodeDecodeError as error:
        errors.append(f"searchindex.js: invalid UTF-8: {error}")
        return
    match = re.fullmatch(r"Search\.setIndex\((.*)\);?", text, re.DOTALL)
    if match is None:
        errors.append("searchindex.js: unexpected wrapper")
        return
    try:
        index = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        errors.append(f"searchindex.js: invalid index JSON: {error}")
        return

    docnames = index.get("docnames", [])
    filenames = index.get("filenames", [])
    titles = index.get("titles", [])
    terms = index.get("terms", {})
    titleterms = index.get("titleterms", {})
    if not all(isinstance(value, list) for value in (docnames, filenames, titles)):
        errors.append("searchindex.js: document arrays are malformed")
        return
    if not isinstance(terms, dict) or not isinstance(titleterms, dict):
        errors.append("searchindex.js: term mappings are malformed")
        return

    for number in sorted(EXPECTED_HOMEWORK - APPROVED_HOMEWORK):
        expected_docname = f"homework/homework-{number:02d}"
        document_ids = [
            document_id
            for document_id, docname in enumerate(docnames)
            if docname == expected_docname
        ]
        if len(document_ids) != 1:
            errors.append(
                f"searchindex.js: expected one {expected_docname!r} document"
            )
            continue
        document_id = document_ids[0]
        if document_id >= len(filenames) or document_id >= len(titles):
            errors.append(f"searchindex.js: {expected_docname!r} arrays are misaligned")
            continue
        if filenames[document_id] != f"{expected_docname}.ipynb":
            errors.append(f"searchindex.js: unexpected filename for Homework {number}")
        if html.unescape(str(titles[document_id])) != f"Homework {number}":
            errors.append(f"searchindex.js: unexpected title for Homework {number}")

        body_terms = {
            str(term)
            for term, references in terms.items()
            if document_id in search_index_document_ids(references)
        }
        if body_terms:
            errors.append(
                f"searchindex.js: Homework {number} has indexed body terms: "
                f"{sorted(body_terms)}"
            )
        indexed_title_terms = {
            str(term)
            for term, references in titleterms.items()
            if document_id in search_index_document_ids(references)
        }
        expected_title_terms = {"homework", str(number)}
        if indexed_title_terms != expected_title_terms:
            errors.append(
                f"searchindex.js: Homework {number} title terms are "
                f"{sorted(indexed_title_terms)}, expected {sorted(expected_title_terms)}"
            )


def audit_pages_view(view: RepositoryView | DirectoryView) -> list[str]:
    paths = view.paths()
    errors: list[str] = []
    if not APPROVED_HOMEWORK <= EXPECTED_HOMEWORK:
        errors.append("approved homework numbers must belong to the public roster")
    if set(APPROVED_SHA256) != APPROVED_HOMEWORK:
        errors.append("every approved homework must have exactly one pinned SHA-256")
    if not set(PUBLIC_HOMEWORK_ASSETS) <= APPROVED_HOMEWORK:
        errors.append("public homework data must belong to an approved homework")

    for path in paths:
        if PRIVATE_PATH_TOKEN.search(path):
            errors.append(f"private solution/key path is present in Pages: {path}")
        path_components = {component.lower() for component in Path(path).parts}
        if FORBIDDEN_PRIVATE_COMPONENTS.intersection(path_components):
            errors.append(f"private homework directory is present in Pages: {path}")
        if (
            path.startswith("_sources/homework/")
            and path not in ALLOWED_PAGES_HOMEWORK_SOURCE_PATHS
        ):
            errors.append(f"unexpected Pages homework source path: {path}")
        if (
            path.startswith("homework/")
            and path not in ALLOWED_PAGES_HOMEWORK_HTML_PATHS
        ):
            errors.append(f"unexpected rendered homework path: {path}")
        if (
            NUMBERED_HOMEWORK_ARTIFACT.search(path)
            and path not in (
                ALLOWED_PAGES_HOMEWORK_SOURCE_PATHS
                | ALLOWED_PAGES_HOMEWORK_HTML_PATHS
                | set(PUBLIC_HOMEWORK_PAGES_DATA)
            )
        ):
            errors.append(f"numbered homework artifact is outside its Pages path: {path}")

    for path, expected_digest in PUBLIC_HOMEWORK_PAGES_DATA.items():
        if path not in paths:
            errors.append(f"missing approved Pages data file: {path}")
            continue
        actual_digest = hashlib.sha256(view.read(path)).hexdigest()
        if actual_digest != expected_digest:
            errors.append(f"approved Pages data SHA-256 changed: {path}")

    for path in paths:
        if Path(path).suffix.lower() in {".ipynb", ".md"}:
            audit_private_content(path=path, payload=view.read(path), errors=errors)

    homework_sources: dict[int, str] = {}
    for path in paths:
        match = PAGES_HOMEWORK_SOURCE_PATH.fullmatch(path)
        if match:
            homework_sources[int(match.group("number"))] = path

    actual_sources = set(homework_sources)
    if actual_sources != EXPECTED_HOMEWORK:
        missing = sorted(EXPECTED_HOMEWORK - actual_sources)
        extra = sorted(actual_sources - EXPECTED_HOMEWORK)
        errors.append(
            f"Pages homework source roster mismatch: missing={missing}, extra={extra}"
        )

    for number, path in sorted(homework_sources.items()):
        audit_notebook(
            number=number,
            path=path,
            payload=view.read(path),
            errors=errors,
        )

    for number in sorted(EXPECTED_HOMEWORK):
        path = f"homework/homework-{number:02d}.html"
        if path not in paths:
            errors.append(f"missing rendered homework page: {path}")
            continue
        expected_title = f"Homework {number}"
        titles = rendered_h1_titles(view.read(path))
        if not titles or any(title != expected_title for title in titles):
            errors.append(
                f"{path}: every rendered H1 must be {expected_title!r}; found {titles}"
            )
        if number not in APPROVED_HOMEWORK and not unreleased_page_is_title_only(
            view.read(path), number
        ):
            errors.append(f"{path}: unreleased rendered page is not title-only")

    audit_pages_search_index(view, paths, errors)
    return errors


def main() -> int:
    args = parse_args()
    if args.pages_ref:
        view = RepositoryView(use_index=False, ref=args.pages_ref)
        errors = audit_pages_view(view)
        audit_label = "Published Pages homework audit"
    elif args.pages_directory:
        if not args.pages_directory.is_dir():
            print(
                f"Published Pages homework audit FAILED:\n"
                f"- build directory does not exist: {args.pages_directory}",
                file=sys.stderr,
            )
            return 1
        errors = audit_pages_view(DirectoryView(args.pages_directory))
        audit_label = "Generated Pages homework audit"
    else:
        view = RepositoryView(use_index=args.index, ref=args.ref)
        errors = audit_source_view(view)
        audit_label = "Public homework audit"

    if errors:
        print(f"{audit_label} FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    approved = ", ".join(str(number) for number in sorted(APPROVED_HOMEWORK))
    unreleased = ", ".join(
        str(number) for number in sorted(EXPECTED_HOMEWORK - APPROVED_HOMEWORK)
    )
    print(
        f"{audit_label} passed: approved={{{approved}}}; "
        f"unreleased={{{unreleased}}} are title-only; no solution or private-authoring "
        "paths are present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
