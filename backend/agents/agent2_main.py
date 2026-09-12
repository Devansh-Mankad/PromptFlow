import requests

from backend.prompts.agent2_system import AGENT2_SYSTEM_PROMPT
from backend.config.settings import (
    AGENT2_OLLAMA_MODEL,
    OLLAMA_HOST
)


class Agent2:
    """
    PromptFlow Agent 2 — Response Generator

    Uses Gemma 4 E2B through Ollama.
    Receives the refined RISE prompt from Agent 1
    and generates the final response.

    Inference parameters are configured
    in the Ollama Modelfile.
    """

    def __init__(self):
        print("Initializing Agent 2...")
        print(f"Ollama model: {AGENT2_OLLAMA_MODEL}")
        print("Agent 2 ready ✓")

    def respond(self, refined_prompt: str) -> str:
        if not refined_prompt or not refined_prompt.strip():
            raise ValueError("Refined prompt cannot be empty")

        refined_prompt = refined_prompt.strip()

        print("\n\nAgent 1 Prompt:", refined_prompt, "\n")

        payload = {
            "model": AGENT2_OLLAMA_MODEL,

            "messages": [
                {
                    "role": "system",
                    "content": AGENT2_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": refined_prompt
                }
            ],

            "stream": False,
            "think": False
        }

        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        raw = data["message"]["content"]

        return self._clean_output(raw)

    def _clean_output(self, raw: str) -> str:
        output = raw.replace(
            "<end_of_turn>",
            ""
        ).strip()

        output = output.replace(
            "<start_of_turn>",
            ""
        ).strip()

        return output


agent2_instance = Agent2()

def run_agent2(refined_prompt: str) -> str:
    return agent2_instance.respond(refined_prompt)