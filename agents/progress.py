from tools import save_progress, get_progress


def record_quiz_result(student_id: str, module_id: str, score: int, total: int) -> dict:
    """Save a quiz result and return confirmation."""
    return save_progress(student_id, module_id, score, total)


def get_student_summary(student_id: str) -> dict:
    """Return full progress summary for a student."""
    return get_progress(student_id)


def format_progress_report(progress: dict) -> str:
    """Format progress data into a readable dashboard string."""
    if "error" in progress:
        return f"Error: {progress['error']}"

    lines = [
        f"## Progress Dashboard — Student: {progress['student_id']}",
        f"**Overall Progress: {progress['overall_percentage']}%** "
        f"({progress['completed_count']}/{progress['total_modules']} modules completed)",
        "",
        "### Module Status",
    ]

    for m in progress["modules"]:
        if m["status"] == "passed":
            icon = "✅"
            detail = f"{m['score']}/{m['total']} ({m['percentage']}%)"
        elif m["status"] == "attempted":
            icon = "🔄"
            detail = f"{m['score']}/{m['total']} — needs retry"
        else:
            icon = "⬜"
            detail = "not started"
        lines.append(f"{icon} **{m['title']}** — {detail}")

    if progress["weak_topics"]:
        lines.append("")
        lines.append("### Weak Topics (retry recommended)")
        for t in progress["weak_topics"]:
            lines.append(f"- {t}")

    lines.append("")
    lines.append(f"### Next Recommended Module")
    lines.append(f"**{progress['next_recommended']}**")

    return "\n".join(lines)
