"""Agent smoke tests — verify orchestrator routing and agent responses."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from agents.orchestrator import orchestrate, detect_intent
from agents.quiz import run_quiz, quiz_feedback_message, submit_quiz
from agents.progress import get_student_summary, format_progress_report


class TestIntentDetection:
    def test_quiz_intent(self):
        assert detect_intent("Quiz me on MCP") == "quiz"
        assert detect_intent("test me on memory") == "quiz"

    def test_progress_intent(self):
        assert detect_intent("What should I study next?") == "progress"
        assert detect_intent("Show my progress") == "progress"

    def test_tutor_intent_default(self):
        assert detect_intent("What is an AI agent?") == "tutor"
        assert detect_intent("Explain MCP") == "tutor"

    def test_safety_demo_intent(self):
        assert detect_intent("Show safety tips") == "safety_demo"


class TestOrchestratorSafety:
    def test_api_key_blocked(self):
        result = orchestrate("My key is AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz12345678")
        assert result["safe"] is False
        assert result["intent"] == "safety_block"
        assert "Warning" in result["response"]

    def test_billing_blocked(self):
        result = orchestrate("I want to deploy to cloud now")
        assert result["safe"] is False
        assert result["intent"] == "safety_block"

    def test_safe_message_passes(self):
        result = orchestrate("What is an agent?")
        assert result["safe"] is True


class TestOrchestratorRouting:
    def test_quiz_route_returns_quiz_data(self):
        result = orchestrate("Quiz me on module 1")
        assert result["intent"] == "quiz"
        assert "quiz_data" in result
        assert result["quiz_data"]["total"] == 3

    def test_progress_route_returns_report(self):
        result = orchestrate("What should I study next?", student_id="test_user")
        assert result["intent"] == "progress"
        assert result["response"] is not None
        assert "Progress Dashboard" in result["response"]

    def test_tutor_route_returns_response(self):
        result = orchestrate("What is MCP?")
        assert result["intent"] == "tutor"
        assert result["response"] is not None
        assert len(result["response"]) > 10


class TestQuizAgent:
    def test_run_quiz_returns_questions(self):
        result = run_quiz("module_2")
        assert result["total"] == 3
        assert len(result["questions"]) == 3

    def test_submit_quiz_and_format(self):
        grade = submit_quiz("module_1", {"q1": "B", "q2": "C", "q3": "B"})
        message = quiz_feedback_message(grade)
        assert "Quiz Results" in message
        assert "Score" in message


class TestProgressAgent:
    def test_format_empty_progress(self, tmp_path, monkeypatch):
        import tools.progress_tools as pt
        monkeypatch.setattr(pt, "PROGRESS_FILE", str(tmp_path / "progress.json"))

        progress = get_student_summary("new_student")
        report = format_progress_report(progress)
        assert "Progress Dashboard" in report
        assert "not started" in report or "⬜" in report
