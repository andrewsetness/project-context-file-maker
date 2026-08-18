"""Guards so a fresh clone does not depend on unpublished sibling repos."""

from pathlib import Path

SKIP_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".cursor",
    "node_modules",
}

# Paths a public clone cannot follow. Company/product names are allowed.
FORBIDDEN_SNIPPETS = (
    "project-setness-consulting",
    "PLAN_PA2.3",
    "../Albert/",
    "..\\Albert\\",
    "../03-business/",
    "..\\03-business\\",
)

SCAN_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".py", ".mdc"}


def _iter_tracked_text_files(project_root: Path):
    for path in project_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if path.name == "test_self_contained.py":
            continue
        yield path


def test_docs_do_not_point_at_unpublished_sibling_repos(project_root):
    offenders = []
    for path in _iter_tracked_text_files(project_root):
        text = path.read_text(encoding="utf-8")
        for snippet in FORBIDDEN_SNIPPETS:
            if snippet in text:
                rel = path.relative_to(project_root)
                offenders.append(f"{rel}: {snippet}")
    assert offenders == [], (
        "A fresh clone cannot follow these sibling-local references:\n"
        + "\n".join(offenders)
    )
