def evaluate_answer(answer: str, rubric: dict) -> dict:
    """
    Evaluate a free-text student answer against a rubric.
    rubric: {
        "expected_keywords": ["agent", "loop", "tool"],
        "min_keywords": 2,
        "topic": "AI Agents"
    }
    Returns score, feedback, and suggestions.
    """
    if not answer or not answer.strip():
        return {
            "score": 0,
            "max_score": 3,
            "feedback": "Your answer was empty. Try writing at least one sentence about the topic.",
            "suggestions": ["Write what you know, even if you are not sure."],
            "keywords_found": [],
            "keywords_missing": rubric.get("expected_keywords", []),
        }

    answer_lower = answer.lower()
    expected = [kw.lower() for kw in rubric.get("expected_keywords", [])]
    min_kw = rubric.get("min_keywords", 2)
    topic = rubric.get("topic", "this topic")

    found = [kw for kw in expected if kw in answer_lower]
    missing = [kw for kw in expected if kw not in answer_lower]

    score = min(3, len(found))

    if score == 3:
        feedback = f"Excellent! Your answer about {topic} covers all the key ideas."
        suggestions = []
    elif score == 2:
        feedback = f"Good job! You covered most of the key ideas about {topic}."
        suggestions = [f"Try to also mention: {', '.join(missing)}."] if missing else []
    elif score == 1:
        feedback = f"You are on the right track with {topic}, but the answer needs more detail."
        suggestions = [
            f"Include these key ideas: {', '.join(missing)}.",
            "Try to explain it in your own words with an example.",
        ]
    else:
        feedback = f"Let's try again. Think about what you learned about {topic}."
        suggestions = [
            f"Key ideas to include: {', '.join(expected)}.",
            "Re-read the module explanation and try again.",
        ]

    return {
        "score": score,
        "max_score": 3,
        "percentage": round((score / 3) * 100),
        "feedback": feedback,
        "suggestions": suggestions,
        "keywords_found": found,
        "keywords_missing": missing,
    }
