# DSP Agentic Academy — Demo Script

Use these prompts in the Learn tab to demonstrate the full agent system.

## Demo 1: Beginner Explanation (Tutor Agent)

Paste into the chat:
```
What is MCP? Explain it like I am in 10th grade.
```
Expected: Tutor Agent explains MCP as a standard connector for tools and data.

## Demo 2: Quiz (Quiz Agent)

Paste into the chat:
```
Quiz me on module 2
```
Expected: Orchestrator routes to Quiz Agent. Quiz for Module 2 (Tools & MCP) starts.

## Demo 3: Progress (Progress Agent)

Paste into the chat:
```
What should I study next?
```
Expected: Progress Agent checks completed modules and recommends the next one.

## Demo 4: Safety Block (Safety Agent)

Paste into the chat:
```
Here is my API key: AIzaSy1234567890abcdefghijklmnopqrstuvwx
```
Expected: Security check fires BEFORE the tutor responds. Warning displayed.

## Demo 5: Human-in-the-Loop

Go to Playground tab → select "Human-in-the-Loop".
Show the diagram and explain: agents should always ask humans before risky actions.

## Demo 6: MCP Server

In terminal:
```bash
python -m mcp_server.server
```
Then visit: http://localhost:8765/mcp/tools
Expected: JSON list of all 4 available MCP tools (explain_concept, generate_quiz, get_progress, security_check).

## Demo 7: Run Tests

```bash
pytest tests/ -v
```
Expected: All tests pass with a score report at the end.

## Course Concepts Shown in This Demo

| Concept | Shown In |
|---|---|
| ADK | agents/ folder — structured agent roles |
| Tool Use | Demo 1, 2, 3 — real tool calls |
| MCP | Demo 6 — live MCP server |
| Skills | skills/tutor_skill.md loaded into TutorAgent |
| Security | Demo 4 — key detection |
| Evaluation | Quiz grading with rubric |
| Multi-Agent | Orchestrator routing across 4 agents |
| Memory | Progress persists in progress.json |
