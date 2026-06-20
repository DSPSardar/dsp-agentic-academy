import os
from tools import generate_quiz, grade_quiz

QUIZ_INSTRUCTION = """
You are the Quiz Agent for DSP Agentic Academy.
Your job is to present quiz questions clearly, collect answers, and give kind, helpful feedback.

Rules:
- Present one question at a time.
- After grading, explain every wrong answer kindly.
- Always encourage the student to try again if they did not pass.
- Never reveal the correct answer before the student answers.
"""


def run_quiz(module_name: str) -> dict:
    """Generate quiz for a module. Returns questions ready to display."""
    return generate_quiz(module_name)


def submit_quiz(module_id: str, answers: dict) -> dict:
    """Grade submitted answers and return detailed feedback."""
    return grade_quiz(module_id, answers)


def quiz_feedback_message(grade_result: dict) -> str:
    """Format grade result into a readable feedback message."""
    if "error" in grade_result:
        return f"Error: {grade_result['error']}"

    lines = [
        f"### Quiz Results: {grade_result['module']}",
        f"**Score: {grade_result['score']}/{grade_result['total']} ({grade_result['percentage']}%)**",
        f"**{'PASSED' if grade_result['passed'] else 'NOT PASSED YET'}**",
        "",
        grade_result["message"],
        "",
        "### Question Breakdown",
    ]

    for fb in grade_result["feedback"]:
        status = "✓" if fb["is_correct"] else "✗"
        lines.append(f"\n**{status} {fb['question']}**")
        lines.append(f"Your answer: **{fb['your_answer']}** | Correct: **{fb['correct_answer']}**")
        if not fb["is_correct"]:
            lines.append(f"*{fb['explanation']}*")

    return "\n".join(lines)
