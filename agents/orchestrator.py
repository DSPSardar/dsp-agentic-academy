"""
Main Orchestrator Agent.
Routes student messages to the correct sub-agent based on intent detection.
Security check runs on EVERY message before routing.
"""

from agents.safety_evaluator import check_message_safety
from agents.tutor import tutor_respond
from agents.quiz import run_quiz, submit_quiz, quiz_feedback_message
from agents.progress import get_student_summary, format_progress_report

QUIZ_TRIGGERS = ["quiz me", "quiz on", "test me", "test on", "start quiz"]
PROGRESS_TRIGGERS = ["my progress", "what should i study", "next module", "next lesson",
                     "what did i complete", "how am i doing", "study next"]
SAFETY_DEMO_TRIGGERS = ["safety", "safe tool", "api key warning", "billing warning"]


def detect_intent(message: str) -> str:
    msg = message.lower().strip()
    if any(t in msg for t in QUIZ_TRIGGERS):
        return "quiz"
    if any(t in msg for t in PROGRESS_TRIGGERS):
        return "progress"
    if any(t in msg for t in SAFETY_DEMO_TRIGGERS):
        return "safety_demo"
    return "tutor"


def extract_module_from_message(message: str) -> str:
    msg = message.lower()
    if "module 1" in msg or "intro" in msg or "introduction" in msg:
        return "module_1"
    if "module 2" in msg or "tool" in msg or "mcp" in msg:
        return "module_2"
    if "module 3" in msg or "memory" in msg or "session" in msg:
        return "module_3"
    if "module 4" in msg or "eval" in msg or "logging" in msg:
        return "module_4"
    if "module 5" in msg or "production" in msg or "deploy" in msg or "a2a" in msg:
        return "module_5"
    return "module_1"


def orchestrate(
    user_message: str,
    student_id: str = "student_001",
    module_context: str = "",
    quiz_state: dict = None,
) -> dict:
    """
    Main entry point. Always runs security check first.
    Returns: {response, intent, safe, warning}
    """
    safety = check_message_safety(user_message)
    if not safety["safe"]:
        return {
            "response": f"🛑 **Safety Warning**\n\n{safety['warning']}",
            "intent": "safety_block",
            "safe": False,
            "warning": safety["warning"],
        }

    intent = detect_intent(user_message)

    if intent == "quiz":
        module_id = extract_module_from_message(user_message)
        quiz_data = run_quiz(module_id)
        return {
            "response": None,
            "intent": "quiz",
            "safe": True,
            "quiz_data": quiz_data,
            "module_id": module_id,
            "warning": None,
        }

    if intent == "progress":
        progress = get_student_summary(student_id)
        report = format_progress_report(progress)
        return {
            "response": report,
            "intent": "progress",
            "safe": True,
            "warning": None,
        }

    if intent == "safety_demo":
        return {
            "response": (
                "### Safety Coach\n\n"
                "Here are the key safety rules for AI agent development:\n\n"
                "1. **Never share API keys** — store them in a `.env` file\n"
                "2. **Avoid unsafe tool calls** — test tools in a safe environment first\n"
                "3. **Human approval for risky actions** — always add a review step\n"
                "4. **Cloud billing warning** — set spending limits before enabling paid APIs\n"
                "5. **Keep demo data fake** — never use real user data in tests\n\n"
                "Try pasting a fake API key to see the safety system in action!"
            ),
            "intent": "safety_demo",
            "safe": True,
            "warning": None,
        }

    response = tutor_respond(user_message, module_context)
    return {
        "response": response,
        "intent": "tutor",
        "safe": True,
        "warning": None,
    }
