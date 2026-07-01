import sys
sys.path.append(".")
from backend.pipeline.intent_classifier import IntentClassifier
from backend.agents.agent1_gemma import run_agent1
from backend.agents.agent2_main import run_agent2
from backend.agents.raw_agent import run_raw_agent


classifier = IntentClassifier()


def process_query(user_input: str) -> dict:
    """
    PromptFlow Pipeline
    TASK:
        User -> Intent Classifier -> Agent 1 -> Agent 2

    NON-TASK:
        User -> Intent Classifier -> Base Assistant
    """

    result = classifier.predict(user_input)
    intent = result["intent"]
    confidence = result["confidence"]

    if intent == "TASK":
        refined_prompt = run_agent1(user_input)
        response = run_agent2(refined_prompt)
        return {
            "intent": intent,
            "confidence": confidence,
            "pipeline": "PromptFlow",
            "refined_prompt": refined_prompt,
            "response": response
        }

    response = run_raw_agent(user_input)
    return {
        "intent": intent,
        "confidence": confidence,
        "pipeline": "Base Assistant",
        "refined_prompt": None,
        "response": response
    }