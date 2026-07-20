import sys
sys.path.append(".")
from backend.agents.agent1_gemma import run_agent1
from backend.agents.agent2_main import run_agent2
from backend.services.session_manager import session_manager

MAX_TURNS = 2
REWRITE_KEYWORDS = [
    "rewrite",
    "simplify",
    "rephrase",
    "reword",
    "improve",
    "shorten",
    "elaborate",
    "in simple words",
    "for beginner",
    "for a beginner",
    "explain again",
    "make it simpler",
    "make it shorter",
    "in easier words",
    "in plain english"
]

def _is_rewrite_request(query: str) -> bool:
    return any(
        keyword in query.lower()
        for keyword in REWRITE_KEYWORDS
    )


def _trim_history(history: list,max_turns: int) -> list:
    max_entries = max_turns * 2
    if len(history) > max_entries:
        return history[-max_entries:]
    return history


def process_query(session_id: str,user_input: str) -> dict:
    history = (session_manager.get_history(session_id))
    last_response = (session_manager.get_last_response(session_id))

    refined_prompt = run_agent1(user_input,history)

    if (_is_rewrite_request(user_input) and last_response):
        agent2_input = (
            f"{refined_prompt}\n\n"
            f"[Previous Response To Rewrite]:\n"
            f"{last_response}"
        )
    else:
        agent2_input = refined_prompt

    response = run_agent2(agent2_input)

    history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    history.append(
        {
            "role": "model",
            "content": refined_prompt
        }
    )

    history = _trim_history(history,MAX_TURNS)
    session_manager.set_history(session_id,history)
    session_manager.set_last_response(session_id,response)

    return {
        "refined_prompt": refined_prompt,
        "response": response
    }


def clear_history(session_id: str):
    session_manager.clear_session(
        session_id
    )