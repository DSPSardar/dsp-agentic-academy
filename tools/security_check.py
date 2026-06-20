import re

# Patterns that indicate secrets or unsafe content
SECRET_PATTERNS = [
    (r"AIza[0-9A-Za-z\-_]{35}", "Google API key"),
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI-style secret key"),
    (r"Bearer\s+[a-zA-Z0-9\-._~+/]{20,}", "Bearer token"),
    (r"[a-f0-9]{32,64}", "hex secret (possible token or hash)"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"xox[baprs]-[0-9A-Za-z\-]+", "Slack token"),
    (r"-----BEGIN (RSA |EC )?PRIVATE KEY-----", "private key"),
    (r"password\s*[:=]\s*\S+", "password in plaintext"),
    (r"[A-Za-z0-9]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", "JWT or API token"),
    (r"[A-Z0-9]{20,}", "possible secret token (long uppercase string)"),
    (r"AQ\.[A-Za-z0-9_\-]{10,}", "Gemini API key"),
]

BILLING_KEYWORDS = [
    "deploy to cloud", "enable billing", "google cloud billing",
    "aws billing", "azure billing", "enable api", "production deploy",
    "gcp billing", "credit card", "payment method",
]

CREDENTIAL_KEYWORDS = [
    "my password is", "my username is", "my email is",
    "my phone number is", "my address is", "my ssn",
    "social security", "passport number",
]


def security_check(user_message: str) -> dict:
    """
    Scan a user message for secrets, billing triggers, or personal data.
    Returns a warning dict if risky content is found, else safe=True.
    """
    msg = user_message.strip()
    msg_lower = msg.lower()

    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, msg, re.IGNORECASE):
            return {
                "safe": False,
                "risk_type": "secret_detected",
                "label": label,
                "warning": (
                    f"Warning: It looks like your message contains a {label}. "
                    "Please do NOT share API keys, tokens, or secrets in this chat. "
                    "Store secrets in a .env file and never paste them in a chat or notebook. "
                    "I have not stored your message."
                ),
            }

    for kw in BILLING_KEYWORDS:
        if kw in msg_lower:
            return {
                "safe": False,
                "risk_type": "billing_warning",
                "label": kw,
                "warning": (
                    "Billing Warning: You are asking about cloud deployment or billing. "
                    "Before enabling any paid cloud service, always: "
                    "(1) Check the pricing page. "
                    "(2) Set a spending limit or budget alert. "
                    "(3) Start with the free tier. "
                    "Keep your first version local by default."
                ),
            }

    for kw in CREDENTIAL_KEYWORDS:
        if kw in msg_lower:
            return {
                "safe": False,
                "risk_type": "personal_data",
                "label": kw,
                "warning": (
                    "Privacy Warning: Please do not share personal information like passwords, "
                    "phone numbers, email addresses, or identity documents in this learning tool. "
                    "This is an educational platform — keep your personal data private."
                ),
            }

    return {"safe": True, "risk_type": None, "warning": None}
