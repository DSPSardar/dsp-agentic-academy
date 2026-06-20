import os
from tools import security_check, evaluate_answer

SKILL_PATH = os.path.join(os.path.dirname(__file__), "..", "skills", "evaluator_skill.md")

SAFETY_INSTRUCTION = """
You are the Safety and Evaluation Agent for DSP Agentic Academy.
Your job is to:
1. Detect and warn about unsafe content (secrets, billing, personal data).
2. Evaluate student free-text answers fairly and kindly.
3. Give improvement suggestions in a supportive tone.

Rules:
- Always be kind and encouraging.
- Never shame a student for a wrong answer.
- Explain clearly why something is unsafe without being scary.
"""


def check_message_safety(user_message: str) -> dict:
    """Run security check on a user message. Returns safe/unsafe status."""
    return security_check(user_message)


def evaluate_student_answer(answer: str, topic: str, expected_keywords: list) -> dict:
    """Evaluate a free-text answer using rubric and optional LLM feedback."""
    rubric = {
        "expected_keywords": expected_keywords,
        "min_keywords": max(1, len(expected_keywords) // 2),
        "topic": topic,
    }
    return evaluate_answer(answer, rubric)


def format_evaluation(eval_result: dict) -> str:
    """Format evaluation result into a readable response."""
    lines = [
        f"### Answer Evaluation",
        f"**Score: {eval_result['score']}/3 ({eval_result['percentage']}%)**",
        "",
        eval_result["feedback"],
    ]

    if eval_result.get("keywords_found"):
        lines.append(f"\n**Key ideas you covered:** {', '.join(eval_result['keywords_found'])}")

    if eval_result.get("suggestions"):
        lines.append("\n**Suggestions to improve:**")
        for s in eval_result["suggestions"]:
            lines.append(f"- {s}")

    return "\n".join(lines)
