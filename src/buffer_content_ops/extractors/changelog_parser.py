"""Changelog parser for CHANGELOG.md files."""

import re
from pathlib import Path

from ..models import ReleaseInfo


def parse_changelog_file(file_path: str = "CHANGELOG.md") -> ReleaseInfo | None:
    """Parse the most recent section from a Keep A Changelog formatted file."""
    path = Path(file_path)
    if not path.exists():
        return None

    content = path.read_text(encoding="utf-8")

    # Match latest version section like: ## [1.0.0] - 2026-11-07 or ## v1.0.0
    version_pattern = re.compile(
        r"^##\s+\[?v?(\d+\.\d+\.\d+[^\]\n]*)\]?(?:\s*-\s*(\d{4}-\d{2}-\d{2}))?",
        re.MULTILINE,
    )
    matches = list(version_pattern.finditer(content))
    if not matches:
        return None

    first = matches[0]
    version = first.group(1).strip()

    # Section ends at next '## ' or end of file
    start_pos = first.end()
    end_pos = matches[1].start() if len(matches) > 1 else len(content)
    body = content[start_pos:end_pos].strip()

    return ReleaseInfo(
        repository=path.parent.name or "local-project",
        tag_name=f"v{version}",
        name=f"Release v{version}",
        body=body,
    )
