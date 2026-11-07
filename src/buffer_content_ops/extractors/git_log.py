"""Git history extractor for local repositories."""

import subprocess
from pathlib import Path

from ..models import ReleaseInfo


def extract_git_commits(
    repo_path: str = ".",
    since_tag: str | None = None,
    max_commits: int = 25,
) -> list[str]:
    """Extract git commit messages from a local repository."""
    cmd = ["git", "-C", repo_path, "log", f"-n{max_commits}", "--oneline", "--no-merges"]
    if since_tag:
        cmd.insert(4, f"{since_tag}..HEAD")

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
        return lines
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def create_release_from_local_git(repo_path: str = ".", version: str = "v0.1.0") -> ReleaseInfo:
    """Build a ReleaseInfo directly from local git status and recent commit messages."""
    commits = extract_git_commits(repo_path)
    body = "## Recent Commits\n" + "\n".join(f"- {c}" for c in commits[:10])

    path_obj = Path(repo_path).resolve()
    repo_name = path_obj.name

    return ReleaseInfo(
        repository=repo_name,
        tag_name=version,
        name=f"{repo_name} {version}",
        body=body,
        commits=commits,
    )
