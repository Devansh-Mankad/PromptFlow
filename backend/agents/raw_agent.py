import requests

from backend.prompts.raw_system import RAW_SYSTEM_PROMPT
from backend.config.settings import AGENT2_OLLAMA_MODEL


class RawAgent:
    """
    PromptFlow Raw Agent

    Sends the original user query directly to
    Gemma 4 E2B through Ollama.

    This is the baseline path used for comparison
    against the Agent 1 → Agent 2 pipeline.

    System prompt and inference parameters are
    controlled by the Ollama Modelfile.
    """

    OLLAMA_URL = "http://localhost:11434/api/chat"
    REQUEST_TIMEOUT = 300

    def __init__(self):
        print("Initializing Raw Assistant...")
        print(f"Ollama model: {AGENT2_OLLAMA_MODEL}")
        print("Raw Assistant ready ✓")

    def _clean_output(self, raw: str) -> str:
        output = raw.strip()

        output = output.replace(
            "<end_of_turn>",
            ""
        )

        output = output.replace(
            "<start_of_turn>",
            ""
        )

        return output.strip()

    def respond(self, user_input: str) -> str:
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty.")

        user_input = user_input.strip()

        print("\n\nLeft Panel Query:", user_input, "\n")

        payload = {
            "model": AGENT2_OLLAMA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": RAW_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "stream": False,
            "think": False,
            "keep_alive": 0
        }

        response = requests.post(
            self.OLLAMA_URL,
            json=payload,
            timeout=self.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        try:
            raw = data["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise RuntimeError(
                "Invalid response received from Ollama."
            ) from exc

        return self._clean_output(raw)


raw_agent_instance = RawAgent()


def run_raw_agent(user_input: str) -> str:
    return raw_agent_instance.respond(user_input)