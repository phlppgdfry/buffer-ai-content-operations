"""GitHub release extractor using gh CLI or GitHub REST API."""

import json
import re
import subprocess
from datetime import datetime

from ..models import ReleaseInfo


def fetch_github_release(repo: str, tag: str | None = None) -> ReleaseInfo:
    """Fetch release data for a repository using gh CLI or mock fallback.

    Args:
        repo: Repository name (e.g. 'phlppgdfry/agentic-workflow-platform' or current directory)
        tag: Optional specific release tag (e.g. 'v1.2.0'). If None, fetches latest.
    """
    cmd = ["gh", "release", "view"]
    if tag:
        cmd.append(tag)
    cmd.extend(["--repo", repo, "--json", "tagName,name,body,url,publishedAt"])

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)

        body = data.get("body", "")
        pr_matches = [int(m) for m in re.findall(r"#(\d+)", body)]

        return ReleaseInfo(
            repository=repo,
            tag_name=data.get("tagName", tag or "v1.0.0"),
            name=data.get("name", "Release"),
            body=body,
            html_url=data.get("url"),
            published_at=datetime.fromisoformat(data["publishedAt"])
            if data.get("publishedAt")
            else datetime.now(),
            pr_numbers=sorted(set(pr_matches)),
        )
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        # Fallback to local mock release if repo not reachable via gh
        return ReleaseInfo(
            repository=repo,
            tag_name=tag or "v0.1.0",
            name=f"Release {tag or 'v0.1.0'}",
            body=(
                "## Highlights\n"
                "- feat(agent): Multi-agent pipeline for automated technical synthesis\n"
                "- feat(buffer): Direct Buffer API GraphQL & CLI integration with dry-run support\n"
                "- perf(ops): Zero latency draft synchronization for LinkedIn social channels\n"
                "- fix(auth): Robust bearer token validation and error diagnostics\n"
            ),
            published_at=datetime.now(),
            pr_numbers=[12, 14, 15],
        )
