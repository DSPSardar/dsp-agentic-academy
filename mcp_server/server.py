"""
Local MCP-style server for DSP Agentic Academy.
Exposes tools via HTTP so agents can discover and call them
following the Model Context Protocol pattern.

Run with: python -m mcp_server.server
Serves on: http://localhost:8765
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tools.explain_concept import explain_concept
from tools.quiz_tools import generate_quiz
from tools.progress_tools import get_progress
from tools.security_check import security_check

app = FastAPI(
    title="DSP Agentic Academy MCP Server",
    description="Local MCP-style tool server for educational agent tools.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── MCP Tool Discovery Endpoint ──────────────────────────────────────────────

@app.get("/mcp/tools")
def list_tools():
    """MCP tool discovery — returns all available tools and their schemas."""
    return {
        "protocol": "mcp",
        "version": "1.0",
        "server": "dsp-agentic-academy",
        "tools": [
            {
                "name": "explain_concept",
                "description": "Explain an AI agent concept in beginner-friendly language.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "The concept to explain (e.g. MCP, agent loop, memory)"},
                        "level": {"type": "string", "default": "beginner", "description": "Explanation level"},
                    },
                    "required": ["topic"],
                },
            },
            {
                "name": "generate_quiz",
                "description": "Generate quiz questions for a learning module.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "module_name": {"type": "string", "description": "Module name or id (e.g. module_1, mcp, memory)"},
                    },
                    "required": ["module_name"],
                },
            },
            {
                "name": "get_progress",
                "description": "Get a student's learning progress summary.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "student_id": {"type": "string", "description": "The student identifier"},
                    },
                    "required": ["student_id"],
                },
            },
            {
                "name": "security_check",
                "description": "Check a message for secrets, billing risks, or personal data.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "user_message": {"type": "string", "description": "The message to check"},
                    },
                    "required": ["user_message"],
                },
            },
        ],
    }


# ── MCP Tool Call Endpoint ────────────────────────────────────────────────────

class ToolCallRequest(BaseModel):
    tool: str
    inputs: dict


@app.post("/mcp/call")
def call_tool(request: ToolCallRequest):
    """MCP tool call endpoint — executes the named tool with given inputs."""
    tool = request.tool
    inputs = request.inputs

    if tool == "explain_concept":
        topic = inputs.get("topic", "")
        level = inputs.get("level", "beginner")
        if not topic:
            raise HTTPException(status_code=400, detail="'topic' is required")
        result = explain_concept(topic, level)
        return {"tool": tool, "result": result}

    elif tool == "generate_quiz":
        module_name = inputs.get("module_name", "")
        if not module_name:
            raise HTTPException(status_code=400, detail="'module_name' is required")
        result = generate_quiz(module_name)
        return {"tool": tool, "result": result}

    elif tool == "get_progress":
        student_id = inputs.get("student_id", "")
        if not student_id:
            raise HTTPException(status_code=400, detail="'student_id' is required")
        result = get_progress(student_id)
        return {"tool": tool, "result": result}

    elif tool == "security_check":
        user_message = inputs.get("user_message", "")
        if not user_message:
            raise HTTPException(status_code=400, detail="'user_message' is required")
        result = security_check(user_message)
        return {"tool": tool, "result": result}

    else:
        raise HTTPException(status_code=404, detail=f"Unknown tool: {tool}")


@app.get("/health")
def health():
    return {"status": "ok", "server": "DSP Agentic Academy MCP Server"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
