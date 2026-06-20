import json
import os
from datetime import datetime

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")

MODULE_ORDER = ["module_1", "module_2", "module_3", "module_4", "module_5"]
MODULE_TITLES = {
    "module_1": "Introduction to Agents",
    "module_2": "Agent Tools and MCP",
    "module_3": "Context Engineering: Sessions and Memory",
    "module_4": "Agent Quality: Evaluation, Logging, and Tracing",
    "module_5": "Prototype to Production",
}


def _load() -> dict:
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)


def _save(data: dict):
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_progress(student_id: str, module_id: str, score: int, total: int) -> dict:
    """Save or update a student's quiz result for a module."""
    data = _load()
    if student_id not in data:
        data[student_id] = {}

    passed = score >= 2
    data[student_id][module_id] = {
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100),
        "passed": passed,
        "completed_at": datetime.now().isoformat(),
    }
    _save(data)
    return {"saved": True, "student_id": student_id, "module_id": module_id, "passed": passed}


def get_progress(student_id: str) -> dict:
    """Return full progress summary for a student."""
    data = _load()
    student_data = data.get(student_id, {})

    completed = [m for m in MODULE_ORDER if student_data.get(m, {}).get("passed")]
    weak = [m for m in MODULE_ORDER if m in student_data and not student_data[m].get("passed")]
    not_started = [m for m in MODULE_ORDER if m not in student_data]

    next_module = None
    for m in MODULE_ORDER:
        if m not in student_data or not student_data[m].get("passed"):
            next_module = m
            break

    modules_detail = []
    for m in MODULE_ORDER:
        info = student_data.get(m)
        modules_detail.append({
            "module_id": m,
            "title": MODULE_TITLES[m],
            "status": "passed" if (info and info.get("passed")) else ("attempted" if info else "not_started"),
            "score": info.get("score") if info else None,
            "total": info.get("total") if info else None,
            "percentage": info.get("percentage") if info else None,
        })

    overall_pct = round((len(completed) / len(MODULE_ORDER)) * 100)

    return {
        "student_id": student_id,
        "overall_percentage": overall_pct,
        "completed_count": len(completed),
        "total_modules": len(MODULE_ORDER),
        "completed": [MODULE_TITLES[m] for m in completed],
        "weak_topics": [MODULE_TITLES[m] for m in weak],
        "not_started": [MODULE_TITLES[m] for m in not_started],
        "next_recommended": MODULE_TITLES.get(next_module, "All modules complete! Review weak topics."),
        "next_module_id": next_module,
        "modules": modules_detail,
    }
