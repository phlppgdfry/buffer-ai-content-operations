"""Business Storytelling Agent.

Translates technical artifacts and changes into executive, recruiter, and
business-analyst relevant narratives emphasizing ROI, velocity, and process optimization.
"""

from ..models import BusinessNarrative, TechnicalInsights


class BusinessStoryAgent:
    """Translates engineering outputs into high-engagement LinkedIn narratives."""

    def compose(self, repo_name: str, insights: TechnicalInsights) -> BusinessNarrative:
        feature_highlights = "\n".join(f"• {f}" for f in insights.features[:3])

        # Formulate strong recruiter/business hook
        hook = (
            f"🚀 Engineering is only half the battle — connecting developer activity directly to "
            f"business communication is where modern automation shines.\n\n"
            f"Just released {insights.primary_theme} in #{repo_name}."
        )

        problem = (
            "Engineering teams spend hours manually writing release summaries, changelogs, "
            "and marketing updates across disconnected platforms, risking stale announcements "
            "and unshared innovation."
        )

        solution = (
            f"We designed a multi-agent automation platform that monitors code repositories, "
            f"extracts key architectural advancements, and pushes structured drafts directly into "
            f"the Buffer API with a human-in-the-loop review policy.\n\n"
            f"Key additions:\n{feature_highlights}"
        )

        impact = (
            f"• Process Velocity: 100% automated release-to-social draft pipeline.\n"
            f"• Governance & Safety: Zero accidental publishing via mandatory Buffer draft staging.\n"
            f"• Architecture: Built with {', '.join(insights.stack[:4])}."
        )

        cta = (
            "👇 How does your team bridge the gap between git commits and public updates? "
            "Curious to hear how others handle developer advocacy automation."
        )

        hashtags = [
            "#BufferAPI",
            "#AIEngineering",
            "#WorkflowAutomation",
            "#Python",
            "#DevOps",
            "#LinkedInCapabilities",
        ]

        return BusinessNarrative(
            hook=hook,
            problem_statement=problem,
            solution_summary=solution,
            measurable_impact=impact,
            call_to_action=cta,
            hashtags=hashtags,
        )
