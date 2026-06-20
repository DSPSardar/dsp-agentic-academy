# DSP Agentic Academy Capstone Project Plan

## 1. Project Goal

Build an interactive AI learning companion that helps DSP students understand AI agents from beginner level to production-ready thinking. The project should demonstrate real agent design, tool use, safety, evaluation, memory, and multi-agent workflows.

## 2. Recommended Kaggle Track

**Agents for Good**

Reason: The project improves education and makes advanced AI agent concepts accessible to students.

## 3. Main User Story

As a DSP student, I want a friendly AI companion that explains AI agent concepts in simple language, lets me practice with visual examples, quizzes me, remembers my progress, and teaches me safe agent design so I can confidently build useful AI agents.

## 4. Core Features

### Feature 1: Simple Concept Explainer

The Tutor Agent explains topics like:

- AI agents
- Tools
- MCP
- Memory
- Evaluation
- ADK
- Multi-agent systems
- A2A
- Deployment readiness

Output should be simple enough for a 10th-grade student.

### Feature 2: Live Visual Playground

Students can view small simulations:

- Agent thinking loop
- Tool calling flow
- MCP connector flow
- Memory/session flow
- Evaluation flow
- Human-in-the-loop approval flow

### Feature 3: Quiz and Feedback

The Quiz Agent creates short quizzes for each module. The Evaluator Agent checks answers and explains mistakes kindly.

### Feature 4: Progress Tracking

The Progress Agent tracks:

- Completed modules
- Quiz scores
- Weak topics
- Recommended next lesson

### Feature 5: Safety Coach

The Safety Coach teaches:

- Do not share API keys
- Avoid unsafe tool calls
- Use human approval for risky actions
- Test agents before real deployment
- Watch for cloud billing

## 5. Agent Architecture

### Main Orchestrator Agent

Routes student requests to the right helper agent.

### Tutor Agent

Explains course concepts in simple language.

### Quiz Agent

Generates and grades short quizzes.

### Progress Agent

Stores and retrieves student learning progress.

### Safety and Evaluation Agent

Checks whether answers are safe, accurate, and beginner-friendly.

## 6. Tools

Suggested local tools:

- `explain_concept(topic, level)`
- `generate_quiz(module_name)`
- `grade_quiz(student_answers)`
- `save_progress(student_id, module, score)`
- `get_progress(student_id)`
- `security_check(user_message)`
- `evaluate_answer(answer, rubric)`

## 7. Course Concepts Demonstrated

| Course Concept | How DSP Agentic Academy Demonstrates It |
|---|---|
| ADK | Uses structured agents, instructions, and tools. |
| Tool Calling | Uses local functions for quizzes, progress, and safety checks. |
| MCP | Explains and can optionally search official developer docs through an MCP-style connector. |
| Skills | Uses reusable instructions for simple explanations and answer evaluation. |
| Security | Blocks secrets and risky deployment guidance. |
| Evaluation | Uses rubrics and test cases to check quality. |
| Multi-Agent Systems | Uses separate tutor, quiz, progress, and safety agents. |

## 8. Minimum Viable Product

The first version should include:

- One web or notebook interface.
- Five learning modules.
- Tutor explanations.
- Quiz generation.
- Progress tracking in local storage or a JSON file.
- Safety warnings for API keys and billing.
- Basic tests for tools.
- A README and demo script.

## 9. Demo Script

### Demo 1: Beginner Explanation

User asks:

```text
What is MCP? Explain it like I am in 10th grade.
```

Expected:

The Tutor Agent explains MCP as a standard connector that lets AI agents use tools and data sources.

### Demo 2: Quiz

User asks:

```text
Quiz me on Agent Tools.
```

Expected:

The Quiz Agent creates 3 short questions and gives feedback.

### Demo 3: Progress

User asks:

```text
What should I study next?
```

Expected:

The Progress Agent checks completed modules and recommends the next module.

### Demo 4: Safety

User says:

```text
Here is my API key: AIza...
```

Expected:

The Safety Agent warns the user not to share secrets and explains how to store keys safely.

## 10. Evaluation Rubric

| Area | Success Criteria |
|---|---|
| Accuracy | Explanations are technically correct. |
| Simplicity | Answers are understandable for beginners. |
| Safety | Secrets and risky actions are blocked or warned. |
| Tool Use | Correct tool is called for quiz, progress, or safety tasks. |
| Memory | Progress is remembered across the session. |
| Usefulness | Student knows what to study next. |

## 11. Security Checklist

- Do not hardcode API keys.
- Store secrets in `.env` or platform secrets.
- Add `.env` to `.gitignore`.
- Warn before any cloud deployment or billing step.
- Keep demo data fake.
- Avoid real student private data in the demo.
- Add tests for unsafe messages.

## 12. Build Timeline

### Phase 1: Planning

- Finalize project name and track.
- Write README and project plan.
- Decide core modules.

### Phase 2: Prototype

- Build local interface.
- Add tutor explanations.
- Add quiz and progress tools.

### Phase 3: Agent Design

- Add orchestrator agent.
- Add tutor, quiz, progress, and safety roles.
- Add skill instructions.

### Phase 4: Evaluation

- Add test cases.
- Add safety tests.
- Add example outputs.

### Phase 5: Submission

- Prepare screenshots.
- Record demo if allowed.
- Finalize README.
- Submit before July 6, 2026 at 11:59 PM PT.

## 13. Submission Deadline

Kaggle deadline:

```text
July 6, 2026 at 11:59 PM PT
```

Islamabad time:

```text
July 7, 2026 at 11:59 AM PKT
```

Safe target:

```text
Submit before July 7, 2026 at 10:00 AM PKT
```

## 14. Final Recommendation

Build DSP Agentic Academy as a local-first educational agent system. Keep the first version simple, safe, and easy to demo. Focus on showing strong agent design rather than complex cloud deployment.

