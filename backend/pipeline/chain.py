import sys
sys.path.append(".")
from backend.agents.agent1_gemma import run_agent1
from backend.agents.agent2_main import run_agent2

# Conversation history for Agent 1
_history: list[dict] = []
_last_response: str = ""
MAX_TURNS = 2

# Keywords that indicate a rewrite request
REWRITE_KEYWORDS = [
    "rewrite", "simplify", "rephrase", "reword",
    "improve", "shorten", "elaborate",
    "in simple words", "for beginner", "for a beginner",
    "explain again", "make it simpler", "make it shorter",
    "in easier words", "in plain english"
]

def _is_rewrite_request(query: str) -> bool:
    return any(keyword in query.lower() for keyword in REWRITE_KEYWORDS)

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
    Agent 2 receives only the current RISE prompt.
    On rewrite requests, Agent 2 also receives 
    the previous response appended to the RISE prompt.
    """
    global _history, _last_response

    refined_prompt = run_agent1(user_input, _history)
    if _is_rewrite_request(user_input) and _last_response:
        agent2_input = (
            f"{refined_prompt}\n\n"
            f"[Previous Response To Rewrite]:\n{_last_response}"
        )
    else:
        agent2_input = refined_prompt

    response = run_agent2(agent2_input)

    _history.append({"role": "user",  "content": user_input})
    _history.append({"role": "model", "content": refined_prompt})
    _history = _trim_history(_history, MAX_TURNS)
    _last_response = response

    return {
        "refined_prompt": refined_prompt,
        "response": response
    }


def clear_history():
    """Call this when user starts a new conversation."""
    global _history, _last_response
    _history = []
    _last_response = ""