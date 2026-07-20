from llama_cpp import Llama
import sys
sys.path.append(".")
from backend.prompts.raw_system import RAW_SYSTEM_PROMPT
from backend.config.settings import AGENT2_INFERENCE_PARAMS
from backend.services.shared_gemma4 import get_shared_model


class RawAgent:
    def __init__(self):
        print("Initializing Raw Assistant...")
        self.model = get_shared_model()
        print("Raw Assistant ready ✓")

    def _build_prompt(self, user_input: str) -> str:
        return (
            f"<start_of_turn>system\n"
            f"{RAW_SYSTEM_PROMPT}<end_of_turn>\n"
            f"<start_of_turn>user\n"
            f"{user_input}<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )

    def _clean_output(self, raw: str) -> str:
        output = raw.replace("<end_of_turn>", "").strip()

        output = output.replace("<start_of_turn>", "").strip()
        return output

    def respond(self, user_input: str) -> str:
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty.")

        prompt = self._build_prompt(user_input.strip())
        response = self.model(
            prompt,
            **AGENT2_INFERENCE_PARAMS
        )

        raw = response["choices"][0]["text"]
        return self._clean_output(raw)

raw_agent_instance = RawAgent()

def run_raw_agent(user_input: str) -> str:
    return raw_agent_instance.respond(user_input)