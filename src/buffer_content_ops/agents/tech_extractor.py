"""Technical Extraction Agent.

Analyzes raw git commits, pull requests, and release markdown, extracting
structured engineering metrics, architectural shifts, and technical taxonomy.
"""

import re
from typing import ClassVar

from ..models import ReleaseInfo, TechnicalInsights


class TechExtractorAgent:
    """Extracts structured engineering facts and categorization."""

    KNOWN_STACK: ClassVar[list[str]] = [
        "Python",
        "FastAPI",
        "Docker",
        "GraphQL",
        "Buffer API",
        "Pydantic",
        "PostgreSQL",
        "LangGraph",
        "TypeScript",
        "Next.js",
        "Node.js",
    ]

    def analyze(self, release: ReleaseInfo) -> TechnicalInsights:
        text = f"{release.name}\n{release.body}\n" + "\n".join(release.commits)

        features: list[str] = []
        optimizations: list[str] = []
        fixes: list[str] = []
        breaking: list[str] = []

        for line in text.splitlines():
            line_clean = line.strip(" -*#")
            if not line_clean:
                continue

            lower = line_clean.lower()
            if any(k in lower for k in ["feat", "add", "implement", "support", "new"]):
                features.append(self._clean_bullet(line_clean))
            elif any(k in lower for k in ["perf", "optimiz", "speed", "cache", "latency"]):
                optimizations.append(self._clean_bullet(line_clean))
            elif any(k in lower for k in ["fix", "bug", "patch", "resolve"]):
                fixes.append(self._clean_bullet(line_clean))
            elif any(k in lower for k in ["breaking", "deprecated", "removed"]):
                breaking.append(self._clean_bullet(line_clean))

        # Detect tech stack
        detected_stack = [tech for tech in self.KNOWN_STACK if tech.lower() in text.lower()]
        if not detected_stack:
            detected_stack = ["Buffer API", "Python", "CLI Architecture"]

        # Determine overarching theme
        theme = "Automated Social Operations & API Orchestration"
        if features:
            theme = f"Release {release.tag_name}: {features[0]}"

        return TechnicalInsights(
            primary_theme=theme,
            features=features[:5] or ["Automated release-to-draft orchestration pipeline"],
            optimizations=optimizations[:3] or ["Streamlined API mutation lifecycle"],
            fixes=fixes[:3],
            breaking_changes=breaking,
            stack=detected_stack,
            architecture_notes="Decoupled multi-agent orchestration with human-governed Buffer draft safety gate.",
        )

    def _clean_bullet(self, text: str) -> str:
        # Strip conventional commits prefix e.g. feat(ops): -> Ops:
        cleaned = re.sub(r"^(feat|fix|perf|docs|chore|refactor)(\([^)]+\))?:\s*", "", text, flags=re.IGNORECASE)
        return cleaned.capitalize()
