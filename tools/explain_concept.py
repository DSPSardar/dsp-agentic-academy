import json
import os

MODULES_DIR = os.path.join(os.path.dirname(__file__), "..", "modules")

CONCEPT_MAP = {
    "agent": "module_1_intro",
    "agents": "module_1_intro",
    "agent loop": "module_1_intro",
    "adk": "module_1_intro",
    "tools": "module_2_tools_mcp",
    "tool": "module_2_tools_mcp",
    "mcp": "module_2_tools_mcp",
    "model context protocol": "module_2_tools_mcp",
    "memory": "module_3_memory",
    "session": "module_3_memory",
    "context": "module_3_memory",
    "evaluation": "module_4_evaluation",
    "logging": "module_4_evaluation",
    "tracing": "module_4_evaluation",
    "eval": "module_4_evaluation",
    "deployment": "module_5_production",
    "production": "module_5_production",
    "a2a": "module_5_production",
    "human in the loop": "module_5_production",
    "human-in-the-loop": "module_5_production",
    "hitl": "module_5_production",
    "safety": "module_5_production",
    "billing": "module_5_production",
    "multi-agent": "module_5_production",
}


def explain_concept(topic: str, level: str = "beginner") -> dict:
    """
    Return a beginner-friendly explanation for a given topic.
    Looks up the relevant module and returns matching concept text.
    """
    topic_lower = topic.lower().strip()

    module_file = None
    for keyword, filename in CONCEPT_MAP.items():
        if keyword in topic_lower:
            module_file = filename
            break

    if module_file is None:
        return {
            "topic": topic,
            "level": level,
            "explanation": (
                f"Great question about '{topic}'! "
                "AI agents are programs that can think and act to reach a goal. "
                "They use tools, remember context, and work in loops. "
                "Pick a module from the Learn tab to go deeper on this topic."
            ),
            "module": None,
        }

    path = os.path.join(MODULES_DIR, f"{module_file}.json")
    with open(path, "r") as f:
        module = json.load(f)

    matched = []
    for concept in module["concepts"]:
        if any(kw in concept["name"].lower() for kw in topic_lower.split()):
            matched.append(concept)

    if not matched:
        matched = module["concepts"][:2]

    explanation_parts = []
    for c in matched[:2]:
        explanation_parts.append(f"**{c['name']}**\n{c['explanation']}")

    return {
        "topic": topic,
        "level": level,
        "explanation": "\n\n".join(explanation_parts),
        "module": module["title"],
        "module_id": module["id"],
    }
