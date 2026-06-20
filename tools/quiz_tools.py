import json
import os

MODULES_DIR = os.path.join(os.path.dirname(__file__), "..", "modules")

MODULE_FILE_MAP = {
    "module_1": "module_1_intro",
    "module_2": "module_2_tools_mcp",
    "module_3": "module_3_memory",
    "module_4": "module_4_evaluation",
    "module_5": "module_5_production",
    "intro": "module_1_intro",
    "introduction": "module_1_intro",
    "tools": "module_2_tools_mcp",
    "mcp": "module_2_tools_mcp",
    "memory": "module_3_memory",
    "session": "module_3_memory",
    "evaluation": "module_4_evaluation",
    "logging": "module_4_evaluation",
    "production": "module_5_production",
    "deployment": "module_5_production",
    "a2a": "module_5_production",
}


def generate_quiz(module_name: str) -> dict:
    """Return quiz questions for the given module."""
    key = module_name.lower().strip()
    filename = MODULE_FILE_MAP.get(key)

    if filename is None:
        for k, v in MODULE_FILE_MAP.items():
            if k in key:
                filename = v
                break

    if filename is None:
        return {
            "error": f"Module '{module_name}' not found. Available: intro, tools/mcp, memory, evaluation, production.",
            "questions": [],
        }

    path = os.path.join(MODULES_DIR, f"{filename}.json")
    with open(path, "r") as f:
        module = json.load(f)

    questions = []
    for q in module["quiz_questions"]:
        questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
        })

    return {
        "module": module["title"],
        "module_id": module["id"],
        "questions": questions,
        "total": len(questions),
    }


def grade_quiz(module_id: str, student_answers: dict) -> dict:
    """
    Grade quiz answers.
    student_answers: {"q1": "B", "q2": "C", "q3": "A"}
    Returns score, feedback per question, pass/fail.
    """
    filename_map = {
        "module_1": "module_1_intro",
        "module_2": "module_2_tools_mcp",
        "module_3": "module_3_memory",
        "module_4": "module_4_evaluation",
        "module_5": "module_5_production",
    }
    filename = filename_map.get(module_id)
    if not filename:
        return {"error": "Invalid module_id", "score": 0}

    path = os.path.join(MODULES_DIR, f"{filename}.json")
    with open(path, "r") as f:
        module = json.load(f)

    correct = 0
    feedback = []
    for q in module["quiz_questions"]:
        qid = q["id"]
        student_ans = student_answers.get(qid, "").strip().upper()
        is_correct = student_ans == q["answer"].upper()
        if is_correct:
            correct += 1
        feedback.append({
            "id": qid,
            "question": q["question"],
            "your_answer": student_ans,
            "correct_answer": q["answer"],
            "is_correct": is_correct,
            "explanation": q["explanation"],
        })

    total = len(module["quiz_questions"])
    passed = correct >= 2

    return {
        "module": module["title"],
        "module_id": module_id,
        "score": correct,
        "total": total,
        "percentage": round((correct / total) * 100),
        "passed": passed,
        "feedback": feedback,
        "message": (
            f"Great job! You passed with {correct}/{total}."
            if passed
            else f"You got {correct}/{total}. Review the module and try again — you can do it!"
        ),
    }
