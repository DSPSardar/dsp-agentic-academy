"""
DSP Agentic Academy — Main Gradio Application
Run: python app.py
"""

import os
import json
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

from agents.orchestrator import orchestrate
from agents.quiz import run_quiz, submit_quiz, quiz_feedback_message
from agents.progress import get_student_summary, format_progress_report, record_quiz_result

# ── Playground SVG diagrams ───────────────────────────────────────────────────

PLAYGROUNDS = {
    "agent_loop": """
<div style="font-family:sans-serif;padding:20px;background:#f8f9fa;border-radius:12px;">
  <h3 style="color:#1a73e8">🔄 The Agent Loop</h3>
  <p style="color:#555">How an AI agent thinks and acts in a continuous loop to reach its goal.</p>
  <svg viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg" width="100%">
    <defs>
      <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#1a73e8"/>
      </marker>
    </defs>
    <rect x="10" y="70" width="130" height="60" rx="10" fill="#e8f0fe" stroke="#1a73e8" stroke-width="2"/>
    <text x="75" y="100" text-anchor="middle" font-size="13" fill="#1a73e8" font-weight="bold">👁 Perceive</text>
    <text x="75" y="118" text-anchor="middle" font-size="11" fill="#555">Read situation</text>
    <rect x="190" y="70" width="130" height="60" rx="10" fill="#fce8e6" stroke="#ea4335" stroke-width="2"/>
    <text x="255" y="100" text-anchor="middle" font-size="13" fill="#ea4335" font-weight="bold">🧠 Think</text>
    <text x="255" y="118" text-anchor="middle" font-size="11" fill="#555">Decide action</text>
    <rect x="370" y="70" width="130" height="60" rx="10" fill="#e6f4ea" stroke="#34a853" stroke-width="2"/>
    <text x="435" y="100" text-anchor="middle" font-size="13" fill="#34a853" font-weight="bold">⚡ Act</text>
    <text x="435" y="118" text-anchor="middle" font-size="11" fill="#555">Use tool / reply</text>
    <rect x="550" y="70" width="130" height="60" rx="10" fill="#fef7e0" stroke="#fbbc04" stroke-width="2"/>
    <text x="615" y="100" text-anchor="middle" font-size="13" fill="#e37400" font-weight="bold">🔎 Observe</text>
    <text x="615" y="118" text-anchor="middle" font-size="11" fill="#555">Check result</text>
    <line x1="140" y1="100" x2="188" y2="100" stroke="#1a73e8" stroke-width="2" marker-end="url(#arrow)"/>
    <line x1="320" y1="100" x2="368" y2="100" stroke="#1a73e8" stroke-width="2" marker-end="url(#arrow)"/>
    <line x1="500" y1="100" x2="548" y2="100" stroke="#1a73e8" stroke-width="2" marker-end="url(#arrow)"/>
    <path d="M 615 130 Q 615 175 350 175 Q 85 175 75 130" stroke="#1a73e8" stroke-width="2" fill="none" marker-end="url(#arrow)" stroke-dasharray="6,3"/>
    <text x="350" y="192" text-anchor="middle" font-size="11" fill="#1a73e8">Loop continues until goal is reached</text>
  </svg>
</div>
""",

    "tool_call": """
<div style="font-family:sans-serif;padding:20px;background:#f8f9fa;border-radius:12px;">
  <h3 style="color:#34a853">🔧 Tool Calling Flow</h3>
  <p style="color:#555">How an agent calls an external tool and uses the result.</p>
  <svg viewBox="0 0 700 220" xmlns="http://www.w3.org/2000/svg" width="100%">
    <defs>
      <marker id="arrow2" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#34a853"/>
      </marker>
    </defs>
    <rect x="20" y="80" width="150" height="60" rx="10" fill="#e8f0fe" stroke="#1a73e8" stroke-width="2"/>
    <text x="95" y="108" text-anchor="middle" font-size="13" fill="#1a73e8" font-weight="bold">🤖 Agent</text>
    <text x="95" y="126" text-anchor="middle" font-size="11" fill="#555">Needs weather data</text>
    <rect x="270" y="80" width="160" height="60" rx="10" fill="#fef7e0" stroke="#fbbc04" stroke-width="2"/>
    <text x="350" y="105" text-anchor="middle" font-size="13" fill="#e37400" font-weight="bold">⚙️ Tool Call</text>
    <text x="350" y="122" text-anchor="middle" font-size="10" fill="#555">get_weather("Islamabad")</text>
    <text x="350" y="136" text-anchor="middle" font-size="10" fill="#555">→ returns result</text>
    <rect x="530" y="80" width="150" height="60" rx="10" fill="#e6f4ea" stroke="#34a853" stroke-width="2"/>
    <text x="605" y="108" text-anchor="middle" font-size="13" fill="#34a853" font-weight="bold">📦 Result</text>
    <text x="605" y="126" text-anchor="middle" font-size="11" fill="#555">"32°C, sunny"</text>
    <line x1="170" y1="110" x2="268" y2="110" stroke="#34a853" stroke-width="2" marker-end="url(#arrow2)"/>
    <line x1="430" y1="110" x2="528" y2="110" stroke="#34a853" stroke-width="2" marker-end="url(#arrow2)"/>
    <path d="M 605 140 Q 605 185 350 185 Q 100 185 95 140" stroke="#34a853" stroke-width="2" fill="none" stroke-dasharray="6,3" marker-end="url(#arrow2)"/>
    <text x="350" y="205" text-anchor="middle" font-size="11" fill="#34a853">Agent uses result to form its reply</text>
  </svg>
</div>
""",

    "mcp_flow": """
<div style="font-family:sans-serif;padding:20px;background:#f8f9fa;border-radius:12px;">
  <h3 style="color:#9c27b0">🔌 MCP Connector Flow</h3>
  <p style="color:#555">MCP (Model Context Protocol) lets agents discover and use tools through a standard interface — like USB for AI tools.</p>
  <svg viewBox="0 0 700 240" xmlns="http://www.w3.org/2000/svg" width="100%">
    <defs>
      <marker id="arrow3" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#9c27b0"/>
      </marker>
    </defs>
    <rect x="10" y="90" width="140" height="60" rx="10" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
    <text x="80" y="118" text-anchor="middle" font-size="13" fill="#9c27b0" font-weight="bold">🤖 Agent</text>
    <text x="80" y="136" text-anchor="middle" font-size="10" fill="#555">Asks: "What tools exist?"</text>
    <rect x="270" y="70" width="160" height="100" rx="10" fill="#ede7f6" stroke="#9c27b0" stroke-width="2.5"/>
    <text x="350" y="100" text-anchor="middle" font-size="13" fill="#9c27b0" font-weight="bold">🔌 MCP Server</text>
    <text x="350" y="118" text-anchor="middle" font-size="10" fill="#555">Tool registry</text>
    <text x="350" y="133" text-anchor="middle" font-size="10" fill="#555">explain_concept ✓</text>
    <text x="350" y="148" text-anchor="middle" font-size="10" fill="#555">generate_quiz ✓</text>
    <text x="350" y="163" text-anchor="middle" font-size="10" fill="#555">security_check ✓</text>
    <rect x="540" y="60" width="140" height="40" rx="8" fill="#e8f5e9" stroke="#4caf50" stroke-width="2"/>
    <text x="610" y="85" text-anchor="middle" font-size="12" fill="#2e7d32">📚 Docs Tool</text>
    <rect x="540" y="110" width="140" height="40" rx="8" fill="#e3f2fd" stroke="#2196f3" stroke-width="2"/>
    <text x="610" y="135" text-anchor="middle" font-size="12" fill="#1565c0">🧠 Memory Tool</text>
    <rect x="540" y="160" width="140" height="40" rx="8" fill="#fff3e0" stroke="#ff9800" stroke-width="2"/>
    <text x="610" y="185" text-anchor="middle" font-size="12" fill="#e65100">📊 Quiz Tool</text>
    <line x1="150" y1="120" x2="268" y2="120" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrow3)"/>
    <line x1="430" y1="90" x2="538" y2="80" stroke="#9c27b0" stroke-width="1.5" marker-end="url(#arrow3)"/>
    <line x1="430" y1="120" x2="538" y2="130" stroke="#9c27b0" stroke-width="1.5" marker-end="url(#arrow3)"/>
    <line x1="430" y1="150" x2="538" y2="178" stroke="#9c27b0" stroke-width="1.5" marker-end="url(#arrow3)"/>
  </svg>
</div>
""",

    "memory_flow": """
<div style="font-family:sans-serif;padding:20px;background:#f8f9fa;border-radius:12px;">
  <h3 style="color:#0097a7">💾 Memory and Session Flow</h3>
  <p style="color:#555">How agents remember short-term conversation context and save long-term progress.</p>
  <svg viewBox="0 0 700 220" xmlns="http://www.w3.org/2000/svg" width="100%">
    <rect x="10" y="30" width="200" height="160" rx="10" fill="#e0f7fa" stroke="#0097a7" stroke-width="2"/>
    <text x="110" y="55" text-anchor="middle" font-size="13" fill="#0097a7" font-weight="bold">💬 Conversation</text>
    <text x="110" y="80" text-anchor="middle" font-size="11" fill="#555">Turn 1: "What is MCP?"</text>
    <text x="110" y="100" text-anchor="middle" font-size="11" fill="#555">Turn 2: "Give me a quiz"</text>
    <text x="110" y="120" text-anchor="middle" font-size="11" fill="#555">Turn 3: "How did I do?"</text>
    <text x="110" y="148" text-anchor="middle" font-size="10" fill="#0097a7" font-style="italic">Short-term memory</text>
    <text x="110" y="164" text-anchor="middle" font-size="10" fill="#0097a7" font-style="italic">(lost on close)</text>
    <rect x="250" y="70" width="200" height="80" rx="10" fill="#fff8e1" stroke="#ffa000" stroke-width="2"/>
    <text x="350" y="98" text-anchor="middle" font-size="13" fill="#e65100" font-weight="bold">🤖 Agent</text>
    <text x="350" y="118" text-anchor="middle" font-size="11" fill="#555">Reads conversation</text>
    <text x="350" y="135" text-anchor="middle" font-size="11" fill="#555">Saves score to file</text>
    <rect x="490" y="30" width="200" height="160" rx="10" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
    <text x="590" y="55" text-anchor="middle" font-size="13" fill="#9c27b0" font-weight="bold">💾 progress.json</text>
    <text x="590" y="80" text-anchor="middle" font-size="11" fill="#555">module_1: passed ✅</text>
    <text x="590" y="100" text-anchor="middle" font-size="11" fill="#555">module_2: score 2/3</text>
    <text x="590" y="120" text-anchor="middle" font-size="11" fill="#555">module_3: not started</text>
    <text x="590" y="148" text-anchor="middle" font-size="10" fill="#9c27b0" font-style="italic">Long-term memory</text>
    <text x="590" y="164" text-anchor="middle" font-size="10" fill="#9c27b0" font-style="italic">(persists forever)</text>
    <line x1="210" y1="110" x2="248" y2="110" stroke="#0097a7" stroke-width="2" marker-end="url(#arrow)"/>
    <line x1="450" y1="110" x2="488" y2="110" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrow)"/>
  </svg>
</div>
""",

    "eval_flow": """
<div style="font-family:sans-serif;padding:20px;background:#f8f9fa;border-radius:12px;">
  <h3 style="color:#c62828">📊 Evaluation Flow</h3>
  <p style="color:#555">How the system checks if an agent's answers are good before trusting them.</p>
  <svg viewBox="0 0 700 180" xmlns="http://www.w3.org/2000/svg" width="100%">
    <defs>
      <marker id="arrow4" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#c62828"/>
      </marker>
    </defs>
    <rect x="10" y="60" width="120" height="60" rx="10" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
    <text x="70" y="88" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">📝 Answer</text>
    <text x="70" y="106" text-anchor="middle" font-size="10" fill="#555">Student reply</text>
    <rect x="175" y="60" width="120" height="60" rx="10" fill="#fff3e0" stroke="#ff9800" stroke-width="2"/>
    <text x="235" y="88" text-anchor="middle" font-size="12" fill="#e65100" font-weight="bold">📋 Rubric</text>
    <text x="235" y="106" text-anchor="middle" font-size="10" fill="#555">Check keywords</text>
    <rect x="340" y="60" width="120" height="60" rx="10" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
    <text x="400" y="88" text-anchor="middle" font-size="12" fill="#9c27b0" font-weight="bold">🔢 Score</text>
    <text x="400" y="106" text-anchor="middle" font-size="10" fill="#555">2/3 — Good</text>
    <rect x="505" y="60" width="180" height="60" rx="10" fill="#e8f5e9" stroke="#4caf50" stroke-width="2"/>
    <text x="595" y="85" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="bold">💬 Feedback</text>
    <text x="595" y="103" text-anchor="middle" font-size="10" fill="#555">"Great! Add MCP detail."</text>
    <text x="595" y="116" text-anchor="middle" font-size="10" fill="#555">→ Try again or continue</text>
    <line x1="130" y1="90" x2="173" y2="90" stroke="#c62828" stroke-width="2" marker-end="url(#arrow4)"/>
    <line x1="295" y1="90" x2="338" y2="90" stroke="#c62828" stroke-width="2" marker-end="url(#arrow4)"/>
    <line x1="460" y1="90" x2="503" y2="90" stroke="#c62828" stroke-width="2" marker-end="url(#arrow4)"/>
  </svg>
</div>
""",

    "human_loop": """
<div style="font-family:sans-serif;padding:20px;background:#f8f9fa;border-radius:12px;">
  <h3 style="color:#2e7d32">👤 Human-in-the-Loop Flow</h3>
  <p style="color:#555">For risky actions, the agent always asks a human to approve before proceeding.</p>
  <svg viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg" width="100%">
    <defs>
      <marker id="arrow5" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#2e7d32"/>
      </marker>
    </defs>
    <rect x="10" y="70" width="130" height="60" rx="10" fill="#e8f0fe" stroke="#1a73e8" stroke-width="2"/>
    <text x="75" y="98" text-anchor="middle" font-size="13" fill="#1a73e8" font-weight="bold">🤖 Agent</text>
    <text x="75" y="116" text-anchor="middle" font-size="10" fill="#555">Plans risky action</text>
    <rect x="200" y="70" width="150" height="60" rx="10" fill="#fff3e0" stroke="#ff9800" stroke-width="2"/>
    <text x="275" y="95" text-anchor="middle" font-size="12" fill="#e65100" font-weight="bold">⚠️ Pause</text>
    <text x="275" y="112" text-anchor="middle" font-size="10" fill="#555">"Should I send</text>
    <text x="275" y="126" text-anchor="middle" font-size="10" fill="#555">this email?"</text>
    <rect x="410" y="50" width="130" height="50" rx="10" fill="#e8f5e9" stroke="#4caf50" stroke-width="2"/>
    <text x="475" y="73" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="bold">✅ Approve</text>
    <text x="475" y="90" text-anchor="middle" font-size="10" fill="#555">Human says YES</text>
    <rect x="410" y="120" width="130" height="50" rx="10" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
    <text x="475" y="143" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">❌ Reject</text>
    <text x="475" y="160" text-anchor="middle" font-size="10" fill="#555">Human says NO</text>
    <rect x="600" y="70" width="90" height="60" rx="10" fill="#e8f0fe" stroke="#1a73e8" stroke-width="2"/>
    <text x="645" y="98" text-anchor="middle" font-size="12" fill="#1a73e8" font-weight="bold">⚡ Act</text>
    <text x="645" y="116" text-anchor="middle" font-size="10" fill="#555">Email sent</text>
    <line x1="140" y1="100" x2="198" y2="100" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrow5)"/>
    <line x1="350" y1="90" x2="408" y2="75" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrow5)"/>
    <line x1="350" y1="110" x2="408" y2="145" stroke="#c62828" stroke-width="2" marker-end="url(#arrow5)"/>
    <line x1="540" y1="75" x2="598" y2="90" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrow5)"/>
  </svg>
</div>
""",
}

# ── Module list ───────────────────────────────────────────────────────────────

MODULES = [
    ("module_1", "Module 1: Introduction to Agents"),
    ("module_2", "Module 2: Agent Tools and MCP"),
    ("module_3", "Module 3: Context Engineering: Sessions and Memory"),
    ("module_4", "Module 4: Agent Quality: Evaluation, Logging, and Tracing"),
    ("module_5", "Module 5: Prototype to Production"),
]

MODULE_PLAYGROUND = {
    "module_1": "agent_loop",
    "module_2": "tool_call",
    "module_3": "memory_flow",
    "module_4": "eval_flow",
    "module_5": "human_loop",
}

# ── State helpers ─────────────────────────────────────────────────────────────

def get_student_id(name: str) -> str:
    return name.strip().lower().replace(" ", "_") if name.strip() else "student_001"


# ── Tab: Learn (Chat) ─────────────────────────────────────────────────────────

def chat_with_tutor(user_message, history, student_name, selected_module):
    if not user_message.strip():
        return history, ""

    student_id = get_student_id(student_name)

    result = orchestrate(
        user_message=user_message,
        student_id=student_id,
        module_context=user_message,
    )

    if result.get("intent") == "quiz":
        module_id = result.get("module_id", "module_1")
        module_titles = {
            "module_1": "Introduction to Agents",
            "module_2": "Agent Tools and MCP",
            "module_3": "Sessions and Memory",
            "module_4": "Evaluation and Logging",
            "module_5": "Prototype to Production",
        }
        title = module_titles.get(module_id, module_id)
        response = (
            f"Great! Head over to the **📝 Quiz** tab to take the quiz on **{title}**.\n\n"
            f"Select the module from the dropdown and click **Start Quiz**."
        )
    else:
        response = result.get("response") or "I'm here to help. Ask me anything about AI agents!"

    history = history or []
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": response})
    return history, ""


# ── Tab: Playground ───────────────────────────────────────────────────────────

def show_playground(demo_name):
    return PLAYGROUNDS.get(demo_name, "<p>Select a demo above.</p>")


# ── Tab: Quiz ─────────────────────────────────────────────────────────────────

quiz_state = {}


def start_quiz(module_id, student_name):
    global quiz_state
    quiz_data = run_quiz(module_id)
    if "error" in quiz_data:
        return f"Error: {quiz_data['error']}", gr.update(visible=False)

    quiz_state = {
        "module_id": quiz_data["module_id"],
        "questions": quiz_data["questions"],
        "student_id": get_student_id(student_name),
    }

    q = quiz_data["questions"]
    display = f"### Quiz: {quiz_data['module']} ({quiz_data['total']} questions)\n\n"
    for i, question in enumerate(q, 1):
        display += f"**Q{i}: {question['question']}**\n"
        for opt in question["options"]:
            display += f"- {opt}\n"
        display += "\n"

    return display, gr.update(visible=True)


def submit_answers(ans1, ans2, ans3, student_name):
    global quiz_state
    if not quiz_state:
        return "Please start a quiz first."

    questions = quiz_state.get("questions", [])
    answers = {}
    raw = [ans1, ans2, ans3]
    for i, q in enumerate(questions):
        ans = raw[i].strip().upper() if i < len(raw) else ""
        if len(ans) > 1:
            ans = ans[0]
        answers[q["id"]] = ans

    grade = submit_quiz(quiz_state["module_id"], answers)
    feedback = quiz_feedback_message(grade)

    if grade.get("passed"):
        record_quiz_result(
            quiz_state["student_id"],
            quiz_state["module_id"],
            grade["score"],
            grade["total"],
        )

    return feedback


# ── Tab: Progress ─────────────────────────────────────────────────────────────

def show_progress(student_name):
    student_id = get_student_id(student_name)
    progress = get_student_summary(student_id)
    return format_progress_report(progress)


# ── Tab: Safety Coach ─────────────────────────────────────────────────────────

def test_safety(message):
    from tools.security_check import security_check
    result = security_check(message)
    if result["safe"]:
        return "✅ **Message is safe.** No secrets, billing triggers, or personal data detected."
    return f"🛑 **{result['risk_type'].replace('_', ' ').title()} Detected**\n\n{result['warning']}"


# ── Build Gradio UI ───────────────────────────────────────────────────────────

CUSTOM_CSS = """
.header-box { background: linear-gradient(135deg, #1a73e8, #0d47a1);
              color: white; padding: 24px; border-radius: 12px; margin-bottom: 16px; }
.header-box h1 { margin: 0; font-size: 28px; }
.header-box p  { margin: 6px 0 0; opacity: 0.9; }
"""

with gr.Blocks(title="DSP Agentic Academy") as demo:

    gr.HTML("""
    <div class="header-box">
      <h1>🎓 DSP Agentic Academy</h1>
      <p>Your AI-powered learning companion for mastering AI Agents, Tools, MCP, Memory, Evaluation, and Multi-Agent Systems.</p>
    </div>
    """)

    with gr.Row():
        student_name = gr.Textbox(
            label="Your Name (used to track progress)",
            placeholder="e.g. Abdul",
            value="Student",
            scale=3,
        )
        gr.Markdown("*Enter your name to save progress across sessions.*", scale=2)

    with gr.Tabs():

        # ── Tab 1: Learn ──────────────────────────────────────────────────────
        with gr.Tab("📚 Learn"):
            gr.Markdown("### Chat with the Tutor Agent\nAsk any question about AI agents, MCP, memory, evaluation, or more.")
            with gr.Row():
                module_dropdown = gr.Dropdown(
                    choices=[("(Free question — no module)", "")] + [(title, mid) for mid, title in MODULES],
                    value="",
                    label="Select a Module (optional)",
                    scale=2,
                )
            chatbot = gr.Chatbot(height=400, label="Tutor Agent")
            with gr.Row():
                user_input = gr.Textbox(
                    placeholder='Try: "What is MCP?" or "Quiz me on tools" or "My progress"',
                    label="Your message",
                    scale=5,
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)

            send_btn.click(
                chat_with_tutor,
                inputs=[user_input, chatbot, student_name, module_dropdown],
                outputs=[chatbot, user_input],
            )
            user_input.submit(
                chat_with_tutor,
                inputs=[user_input, chatbot, student_name, module_dropdown],
                outputs=[chatbot, user_input],
            )

            gr.Examples(
                examples=[
                    ["What is an AI agent?"],
                    ["Explain MCP like I am in 10th grade"],
                    ["What is human-in-the-loop?"],
                    ["Quiz me on tools"],
                    ["What should I study next?"],
                    ["Here is my API key: AIzaSy123456789"],
                ],
                inputs=user_input,
                label="Try these examples",
            )

        # ── Tab 2: Playground ─────────────────────────────────────────────────
        with gr.Tab("🎮 Playground"):
            gr.Markdown("### Visual Playground\nSee how AI agent systems work step-by-step.")
            demo_choice = gr.Radio(
                choices=[
                    ("Agent Thinking Loop", "agent_loop"),
                    ("Tool Calling Flow", "tool_call"),
                    ("MCP Connector Flow", "mcp_flow"),
                    ("Memory & Session Flow", "memory_flow"),
                    ("Evaluation Flow", "eval_flow"),
                    ("Human-in-the-Loop", "human_loop"),
                ],
                value="agent_loop",
                label="Choose a Demo",
            )
            playground_display = gr.HTML(value=PLAYGROUNDS["agent_loop"])
            demo_choice.change(show_playground, inputs=demo_choice, outputs=playground_display)

        # ── Tab 3: Quiz ───────────────────────────────────────────────────────
        with gr.Tab("📝 Quiz"):
            gr.Markdown("### Take a Quiz\nTest your knowledge on each module. Score 2/3 or higher to mark it complete.")
            quiz_module = gr.Dropdown(
                choices=[(title, mid) for mid, title in MODULES],
                value="module_1",
                label="Choose a Module",
            )
            start_btn = gr.Button("Start Quiz", variant="primary")
            quiz_display = gr.Markdown("")
            with gr.Column(visible=False) as answer_section:
                ans1 = gr.Textbox(label="Answer to Q1 (type the letter: A, B, C, or D)", placeholder="A")
                ans2 = gr.Textbox(label="Answer to Q2", placeholder="B")
                ans3 = gr.Textbox(label="Answer to Q3", placeholder="C")
                submit_btn = gr.Button("Submit Answers", variant="primary")
            result_display = gr.Markdown("")

            start_btn.click(
                start_quiz,
                inputs=[quiz_module, student_name],
                outputs=[quiz_display, answer_section],
            )
            submit_btn.click(
                submit_answers,
                inputs=[ans1, ans2, ans3, student_name],
                outputs=[result_display],
            )

        # ── Tab 4: Progress ───────────────────────────────────────────────────
        with gr.Tab("📊 Progress"):
            gr.Markdown("### Your Learning Progress\nSee completed modules, weak topics, and your next recommended module.")
            refresh_btn = gr.Button("Refresh Progress", variant="primary")
            progress_display = gr.Markdown("")
            refresh_btn.click(show_progress, inputs=[student_name], outputs=[progress_display])

        # ── Tab 5: Safety Coach ───────────────────────────────────────────────
        with gr.Tab("🛡️ Safety Coach"):
            gr.Markdown("""
### Safety Coach
Learn about AI agent safety rules by testing messages.
The safety system scans every message before the agent responds.

**Rules to know:**
- Never share API keys or secret tokens
- Always set billing limits before cloud deployment
- Never include personal data in learning tools
- Use human approval for risky agent actions
""")
            with gr.Row():
                safety_input = gr.Textbox(
                    label="Test a message",
                    placeholder='Try: "My API key is AIzaSy123456" or "deploy to cloud with billing"',
                    scale=4,
                )
                safety_btn = gr.Button("Check Safety", variant="primary", scale=1)
            safety_result = gr.Markdown("")
            safety_btn.click(test_safety, inputs=[safety_input], outputs=[safety_result])

            gr.Examples(
                examples=[
                    ["Here is my API key: AIzaSy1234567890abcdefghijklmnopqrstuvwx"],
                    ["How do I enable billing and deploy to cloud?"],
                    ["My password is secret123"],
                    ["What is MCP?"],
                    ["Quiz me on memory"],
                ],
                inputs=safety_input,
                label="Test these examples",
            )

        # ── Tab 6: About ──────────────────────────────────────────────────────
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
## DSP Agentic Academy

**Track:** Agents for Good (Kaggle Capstone)

**What this project demonstrates:**

| Course Concept | Implementation |
|---|---|
| ADK (Agent Development Kit) | Structured agents in `agents/` with instructions and tools |
| Tool Use | 6 local tools: explain, quiz, grade, progress, security, evaluate |
| MCP (Model Context Protocol) | Local MCP server at `mcp_server/server.py` with tool discovery |
| Agent Skills | Reusable `skills/tutor_skill.md` and `skills/evaluator_skill.md` |
| Security | `security_check()` runs on every message before agent responds |
| Evaluation | Rubric-based evaluation with test cases in `tests/` |
| Multi-Agent Systems | Orchestrator routes to Tutor, Quiz, Progress, Safety agents |
| Memory | `data/progress.json` persists across sessions |

**Architecture:**
```
Student Message
      ↓
Security Check (always first)
      ↓
Orchestrator Agent
  ├── Tutor Agent → explain_concept tool
  ├── Quiz Agent → generate_quiz / grade_quiz tools
  ├── Progress Agent → save_progress / get_progress tools
  └── Safety Agent → security_check / evaluate_answer tools
```

**MCP Server:** Run `python -m mcp_server.server` to start the local tool server on port 8765.

**Program:** [Digital Services Program](https://www.digitalservicesprogram.com/)
""")

if __name__ == "__main__":
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        theme=gr.themes.Soft(primary_hue="blue"),
        css=CUSTOM_CSS,
    )
