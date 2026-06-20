"""Safety tests — verify the security_check tool catches all risky patterns."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from tools.security_check import security_check


class TestSecretDetection:
    def test_google_api_key_detected(self):
        result = security_check("My key is AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz12345678")
        assert result["safe"] is False
        assert result["risk_type"] == "secret_detected"
        assert "Google API key" in result["label"]

    def test_openai_key_detected(self):
        result = security_check("sk-abcdefghijklmnopqrstuvwxyz123456789012")
        assert result["safe"] is False
        assert result["risk_type"] == "secret_detected"

    def test_github_token_detected(self):
        result = security_check("ghp_ABCDefghijklmnopqrstuvwxyz1234567890ab")
        assert result["safe"] is False
        assert result["risk_type"] == "secret_detected"

    def test_private_key_detected(self):
        result = security_check("-----BEGIN RSA PRIVATE KEY----- MIIE...")
        assert result["safe"] is False
        assert result["risk_type"] == "secret_detected"

    def test_bearer_token_detected(self):
        result = security_check("Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9abc")
        assert result["safe"] is False
        assert result["risk_type"] == "secret_detected"


class TestBillingWarning:
    def test_deploy_to_cloud_warning(self):
        result = security_check("How do I deploy to cloud right now?")
        assert result["safe"] is False
        assert result["risk_type"] == "billing_warning"

    def test_enable_billing_warning(self):
        result = security_check("Enable billing for my GCP project")
        assert result["safe"] is False
        assert result["risk_type"] == "billing_warning"

    def test_gcp_billing_detected(self):
        result = security_check("How do I set up gcp billing?")
        assert result["safe"] is False
        assert result["risk_type"] == "billing_warning"


class TestPersonalData:
    def test_password_warning(self):
        result = security_check("my password is abc123")
        assert result["safe"] is False
        assert result["risk_type"] == "personal_data"

    def test_ssn_warning(self):
        result = security_check("my ssn is 123-45-6789")
        assert result["safe"] is False
        assert result["risk_type"] == "personal_data"


class TestSafeMessages:
    def test_normal_question_is_safe(self):
        result = security_check("What is an AI agent?")
        assert result["safe"] is True
        assert result["warning"] is None

    def test_mcp_question_is_safe(self):
        result = security_check("Explain MCP to me")
        assert result["safe"] is True

    def test_quiz_request_is_safe(self):
        result = security_check("Quiz me on Module 2")
        assert result["safe"] is True

    def test_progress_request_is_safe(self):
        result = security_check("What should I study next?")
        assert result["safe"] is True

    def test_empty_message_is_safe(self):
        result = security_check("")
        assert result["safe"] is True
