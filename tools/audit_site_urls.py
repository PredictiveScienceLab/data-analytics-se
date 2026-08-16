#!/usr/bin/env python3
"""Audit a classic Jupyter Book build against the published URL baseline."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlsplit


PUBLIC_PREFIX = "/data-analytics-se/"
PUBLIC_BASE = "https://predictivesciencelab.github.io/data-analytics-se/"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value for name, value in attrs if value is not None}
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a" and "name" in values:
            self.ids.add(values["name"])
        for attribute in ("href", "src"):
            if attribute in values:
                self.links.append((attribute, values[attribute]))


def parser_for(text: str) -> LinkParser:
    parser = LinkParser()
    parser.feed(text)
    return parser


def git_output(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout


def is_content_html(path: str) -> bool:
    return (
        path.endswith(".html")
        and path not in {"search.html", "genindex.html"}
        and not (path.startswith("_static/") and path.endswith("macros.html"))
    )


def baseline_paths(ref: str) -> list[str]:
    paths = git_output("ls-tree", "-r", "--name-only", ref).splitlines()
    return sorted(path for path in paths if is_content_html(path))


def activity_paths(path: Path) -> list[str]:
    routes: list[str] = []
    for line in path.read_text().splitlines():
        line = line.strip().removeprefix("+").strip()
        if line.startswith(PUBLIC_BASE):
            routes.append(line.removeprefix(PUBLIC_BASE))
    return sorted(set(routes))


def resolve_local_target(site_root: Path, source: Path, raw_url: str) -> tuple[Path, str] | None:
    parsed = urlsplit(raw_url)
    if parsed.scheme or parsed.netloc or raw_url.startswith(("mailto:", "javascript:", "data:")):
        return None

    url_path = unquote(parsed.path)
    if url_path.startswith(PUBLIC_PREFIX):
        target = site_root / url_path.removeprefix(PUBLIC_PREFIX)
    elif url_path.startswith("/"):
        return None
    elif url_path:
        target = source.parent / url_path
    else:
        target = source

    if url_path.endswith("/"):
        target = target / "index.html"
    return target.resolve(), unquote(parsed.fragment)


def main() -> int:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--site", type=Path, default=Path("lecturebook/_build/html"))
    argument_parser.add_argument("--baseline-ref", default="fall2026-gh-pages-baseline")
    argument_parser.add_argument("--activity-links", type=Path, default=Path("activity_links.md"))
    argument_parser.add_argument("--report", type=Path, default=Path("site-url-audit.json"))
    args = argument_parser.parse_args()

    site = args.site.resolve()
    candidate = {
        str(path.relative_to(site)): path
        for path in site.rglob("*.html")
        if is_content_html(str(path.relative_to(site)))
    }
    baseline = baseline_paths(args.baseline_ref)
    missing_baseline = sorted(set(baseline) - set(candidate))

    activities = activity_paths(args.activity_links)
    missing_activities = sorted(route for route in activities if route not in candidate)

    parsed_pages: dict[Path, LinkParser] = {}
    broken_files: list[dict[str, str]] = []
    broken_fragments: list[dict[str, str]] = []
    for relative, source in sorted(candidate.items()):
        parsed = parser_for(source.read_text(errors="replace"))
        parsed_pages[source.resolve()] = parsed
        for attribute, url in parsed.links:
            resolved = resolve_local_target(site, source, url)
            if resolved is None:
                continue
            target, fragment = resolved
            if not target.exists():
                broken_files.append(
                    {"source": relative, "attribute": attribute, "url": url}
                )
                continue
            if fragment and target.suffix == ".html":
                target_parser = parsed_pages.get(target)
                if target_parser is None:
                    target_parser = parser_for(target.read_text(errors="replace"))
                    parsed_pages[target] = target_parser
                if fragment not in target_parser.ids:
                    broken_fragments.append({"source": relative, "url": url})

    missing_lecture_anchors: list[dict[str, str]] = []
    for route in baseline:
        if not route.startswith("lecture") or route not in candidate:
            continue
        old_parser = parser_for(git_output("show", f"{args.baseline_ref}:{route}"))
        new_parser = parsed_pages.get(candidate[route].resolve())
        if new_parser is None:
            new_parser = parser_for(candidate[route].read_text(errors="replace"))
        for fragment in sorted(old_parser.ids - new_parser.ids):
            missing_lecture_anchors.append({"route": route, "fragment": fragment})

    report = {
        "site": str(site),
        "baseline_ref": args.baseline_ref,
        "counts": {
            "candidate_content_pages": len(candidate),
            "baseline_content_pages": len(baseline),
            "activity_links": len(activities),
            "missing_baseline_pages": len(missing_baseline),
            "missing_activity_pages": len(missing_activities),
            "broken_internal_files": len(broken_files),
            "broken_internal_fragments": len(broken_fragments),
            "missing_legacy_lecture_anchors": len(missing_lecture_anchors),
        },
        "missing_baseline_pages": missing_baseline,
        "missing_activity_pages": missing_activities,
        "broken_internal_files": broken_files,
        "broken_internal_fragments": broken_fragments,
        "missing_legacy_lecture_anchors": missing_lecture_anchors,
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["counts"], indent=2))
    print(f"Report: {args.report}")
    failures = sum(
        report["counts"][key]
        for key in (
            "missing_baseline_pages",
            "missing_activity_pages",
            "broken_internal_files",
            "broken_internal_fragments",
            "missing_legacy_lecture_anchors",
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
