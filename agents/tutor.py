import os
from tools import explain_concept

SKILL_PATH = os.path.join(os.path.dirname(__file__), "..", "skills", "tutor_skill.md")

def _load_skill() -> str:
    try:
        with open(SKILL_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""


TUTOR_INSTRUCTION = """
You are a friendly AI tutor for DSP students learning about AI agents.
Your job is to explain concepts clearly and simply, as if the student is in 10th grade.

Rules:
- Always use simple words. Avoid jargon unless you explain it first.
- Use short analogies and real-life examples.
- Never ask for or suggest sharing API keys or secrets.
- End each explanation with: "Want me to quiz you on this? Just say 'Quiz me on [topic]'."
- Be encouraging and patient.
"""


def tutor_respond(user_message: str, module_context: str = "") -> str:
    """
    Generate a tutor response. Uses explain_concept tool first, then enriches with LLM.
    Falls back to tool-only response if LLM is unavailable.
    """
    api_key = os.environ.get("GOOGLE_API_KEY", "")

    topic_hint = module_context if module_context else user_message
    concept_result = explain_concept(topic_hint)
    tool_explanation = concept_result.get("explanation", "")
    module_title = concept_result.get("module", "")

    context_block = ""
    if module_title:
        context_block = f"\n\nModule context: {module_title}\n{tool_explanation}"

    if not api_key or api_key == "your_google_api_key_here":
        response = f"**{module_title or 'Learning with DSP Agentic Academy'}**\n\n"
        response += tool_explanation if tool_explanation else (
            f"Great question about '{user_message}'! "
            "Let me explain this concept in simple terms.\n\n"
            "AI agents are programs that can think, decide, and act to reach a goal. "
            "They use tools to interact with the world and memory to remember past steps."
        )
        response += "\n\n---\nWant me to quiz you on this? Just say **'Quiz me on [topic]'**."
        return response

    try:
        import google.generativeai as genai
        skill_text = _load_skill()
        system_prompt = TUTOR_INSTRUCTION + "\n\n" + skill_text
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt,
        )
        prompt = f"{user_message}{context_block}"
        result = model.generate_content(prompt)
        return result.text
    except Exception:
        return (
            f"**{module_title or 'DSP Agentic Academy'}**\n\n"
            f"{tool_explanation}\n\n"
            f"---\nWant me to quiz you on this? Just say **'Quiz me on [topic]'**."
        )
