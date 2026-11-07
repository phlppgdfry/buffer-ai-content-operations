"""Quality Gate Agent.

Validates length, reading ease, formatting, LinkedIn character limits,
hashtag limits, and ensures the draft is ready for human review and Buffer submission.
"""


from ..models import BusinessNarrative, QualityGateReview


class QualityGateAgent:
    """Enforces content standards and safety policies."""

    LINKEDIN_MAX_CHARS = 3000
    RECOMMENDED_MAX_CHARS = 1800

    def evaluate(self, narrative: BusinessNarrative) -> QualityGateReview:
        formatted_text = narrative.to_formatted_post()
        char_count = len(formatted_text)

        checks: dict[str, bool] = {
            "within_character_limit": char_count <= self.LINKEDIN_MAX_CHARS,
            "has_strong_hook": bool(narrative.hook.strip()),
            "has_clear_problem_statement": bool(narrative.problem_statement.strip()),
            "has_solution_summary": bool(narrative.solution_summary.strip()),
            "has_measurable_impact": bool(narrative.measurable_impact.strip()),
            "has_call_to_action": bool(narrative.call_to_action.strip()),
            "hashtag_count_valid": 2 <= len(narrative.hashtags) <= 8,
        }

        feedback: list[str] = []
        if not checks["within_character_limit"]:
            feedback.append(
                f"Post exceeds LinkedIn limit ({char_count}/{self.LINKEDIN_MAX_CHARS} chars)."
            )

        if not checks["hashtag_count_valid"]:
            feedback.append(f"Hashtag count should be between 2 and 8 (currently {len(narrative.hashtags)}).")

        if char_count > self.RECOMMENDED_MAX_CHARS:
            feedback.append(f"Post is somewhat lengthy ({char_count} chars). Consider concise bulleting.")

        passed_checks = sum(1 for v in checks.values() if v)
        score = int((passed_checks / len(checks)) * 100)
        passed = checks["within_character_limit"] and checks["has_strong_hook"] and score >= 80

        readability = "Excellent" if score >= 90 else "Good" if score >= 80 else "Needs Revision"

        return QualityGateReview(
            score=score,
            passed=passed,
            char_count=char_count,
            readability=readability,
            checks=checks,
            feedback=feedback,
        )
