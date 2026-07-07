import sys
sys.path.append(".")
from backend.agents.agent1_gemma import run_agent1
from backend.agents.agent2_main import run_agent2

# Conversation history for Agent 1
_history: list[dict] = []
MAX_TURNS = 3

def _trim_history(history: list[dict], max_turns: int) -> list[dict]:
    """
    Keep only the last N complete turns.
    Each turn is 2 entries: user + model.
    """
    max_entries = max_turns * 2
    if len(history) > max_entries:
        return history[-max_entries:]
    return history


def process_query(user_input: str) -> dict:
    """
    PromptFlow Pipeline: User -> Agent 1 -> Agent 2

    Agent 1 receives full conversation history.
    Agent 2 receives only the current RISE prompt — no history.
    """
    global _history

    # Agent 1: refine with full history
    refined_prompt = run_agent1(user_input, _history)
    response = run_agent2(refined_prompt)

    # Update history with this turn
    _history.append({"role": "user",  "content": user_input})
    _history.append({"role": "model",  "content": refined_prompt})  
    #_history.append({"role": "model", "content": response})
    #_history.append({"role": "user", "content": f"[Agent 2 Response]: {response}"})
        
    _history = _trim_history(_history, MAX_TURNS)
    return {
        "refined_prompt": refined_prompt,
        "response": response
    }


def clear_history():
    """Call this when user starts a new conversation."""
    global _history
    _history = []