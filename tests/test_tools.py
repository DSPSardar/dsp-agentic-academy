"""Unit tests for all tool functions."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from tools.explain_concept import explain_concept
from tools.quiz_tools import generate_quiz, grade_quiz
from tools.progress_tools import save_progress, get_progress
from tools.evaluate_answer import evaluate_answer


class TestExplainConcept:
    def test_known_topic_returns_explanation(self):
        result = explain_concept("MCP")
        assert result["explanation"]
        assert len(result["explanation"]) > 20

    def test_agent_topic(self):
        result = explain_concept("agent")
        assert result["module"] is not None

    def test_unknown_topic_returns_fallback(self):
        result = explain_concept("quantum computing")
        assert "explanation" in result
        assert result["module"] is None

    def test_memory_topic(self):
        result = explain_concept("memory")
        assert "memory" in result["explanation"].lower() or "session" in result["explanation"].lower()

    def test_returns_module_id_when_known(self):
        result = explain_concept("evaluation")
        assert result.get("module_id") == "module_4"


class TestQuizTools:
    def test_generate_quiz_module1(self):
        result = generate_quiz("module_1")
        assert result["total"] == 3
        assert len(result["questions"]) == 3

    def test_generate_quiz_by_keyword(self):
        result = generate_quiz("mcp")
        assert "error" not in result
        assert result["total"] == 3

    def test_generate_quiz_unknown_returns_error(self):
        result = generate_quiz("xyz_unknown_module")
        assert "error" in result

    def test_grade_all_correct(self):
        result = grade_quiz("module_1", {"q1": "B", "q2": "C", "q3": "B"})
        assert result["score"] == 3
        assert result["passed"] is True
        assert result["percentage"] == 100

    def test_grade_all_wrong(self):
        result = grade_quiz("module_1", {"q1": "A", "q2": "A", "q3": "A"})
        assert result["score"] == 0
        assert result["passed"] is False

    def test_grade_partial(self):
        result = grade_quiz("module_1", {"q1": "B", "q2": "C", "q3": "A"})
        assert result["score"] == 2
        assert result["passed"] is True

    def test_grade_feedback_length(self):
        result = grade_quiz("module_2", {"q1": "B", "q2": "C", "q3": "B"})
        assert len(result["feedback"]) == 3


class TestProgressTools:
    def test_save_and_retrieve_progress(self, tmp_path, monkeypatch):
        import tools.progress_tools as pt
        monkeypatch.setattr(pt, "PROGRESS_FILE", str(tmp_path / "progress.json"))

        save_result = save_progress("test_student", "module_1", 3, 3)
        assert save_result["saved"] is True
        assert save_result["passed"] is True

        progress = get_progress("test_student")
        assert progress["completed_count"] == 1
        assert progress["overall_percentage"] == 20

    def test_progress_empty_student(self, tmp_path, monkeypatch):
        import tools.progress_tools as pt
        monkeypatch.setattr(pt, "PROGRESS_FILE", str(tmp_path / "progress.json"))

        progress = get_progress("nobody")
        assert progress["completed_count"] == 0
        assert progress["overall_percentage"] == 0
        assert progress["next_module_id"] == "module_1"

    def test_all_modules_complete(self, tmp_path, monkeypatch):
        import tools.progress_tools as pt
        monkeypatch.setattr(pt, "PROGRESS_FILE", str(tmp_path / "progress.json"))

        for i in range(1, 6):
            save_progress("top_student", f"module_{i}", 3, 3)

        progress = get_progress("top_student")
        assert progress["completed_count"] == 5
        assert progress["overall_percentage"] == 100


class TestEvaluateAnswer:
    def test_full_score(self):
        result = evaluate_answer(
            "An AI agent uses tools in a loop to reach its goal",
            {"expected_keywords": ["agent", "tools", "loop", "goal"], "min_keywords": 3, "topic": "agents"},
        )
        assert result["score"] >= 3

    def test_empty_answer_zero_score(self):
        result = evaluate_answer(
            "",
            {"expected_keywords": ["agent", "loop"], "min_keywords": 1, "topic": "agents"},
        )
        assert result["score"] == 0

    def test_partial_keywords(self):
        result = evaluate_answer(
            "agents are tools",
            {"expected_keywords": ["agent", "tools", "loop", "goal"], "min_keywords": 2, "topic": "agents"},
        )
        assert 1 <= result["score"] <= 2
