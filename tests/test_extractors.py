"""Tests for technical extractors."""

from pathlib import Path

from buffer_content_ops.extractors.changelog_parser import parse_changelog_file
from buffer_content_ops.extractors.github_release import fetch_github_release


def test_changelog_parser(tmp_path: Path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        """# Changelog
All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-11-07
### Added
- Multi-agent coordination engine.
- Buffer draft safety policy.

### Fixed
- GraphQL query syntax error.

## [1.1.0] - 2026-10-15
### Added
- Initial setup.
""",
        encoding="utf-8",
    )

    release = parse_changelog_file(str(changelog))
    assert release is not None
    assert release.tag_name == "v1.2.0"
    assert "Multi-agent coordination engine" in release.body
    assert "1.1.0" not in release.body


def test_github_release_fallback():
    release = fetch_github_release("nonexistent/repo-for-testing")
    assert release.tag_name == "v0.1.0"
    assert release.repository == "nonexistent/repo-for-testing"
    assert len(release.pr_numbers) > 0
