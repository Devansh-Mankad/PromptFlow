from llama_cpp import Llama
from backend.prompts.agent1_system import AGENT1_SYSTEM_PROMPT
from backend.config.settings import (
    AGENT1_MODEL_PATH,
    AGENT1_LOADING_PARAMS,
    AGENT1_INFERENCE_PARAMS
)

class Agent1:
    """
    PromptFlow Agent 1 — Prompt Refiner
    Loads fine-tuned Gemma 3 1B GGUF model
    Converts messy user input to RISE format
    """

    def __init__(self):
        print("Loading Agent 1 — Gemma 3 1B...")
        print(f"Model path: {AGENT1_MODEL_PATH}")

        # Initialize llama-cpp-python with model
        self.model = Llama(
            model_path=AGENT1_MODEL_PATH,
            **AGENT1_LOADING_PARAMS
        )
        print("Agent 1 loaded successfully ✓")

    def _build_prompt(self, user_input: str) -> str:
        """
        Build Gemma chat template format prompt.
        Must match EXACTLY the format used during
        fine tuning in Google Colab.
        Wrong format = wrong output guaranteed.
        """
        return (
            f"<start_of_turn>system\n"
            f"{AGENT1_SYSTEM_PROMPT}<end_of_turn>\n"
            f"<start_of_turn>user\n"
            f"{user_input}<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )

    def _clean_output(self, raw_output: str) -> str:
        """
        Clean the raw model output.
        Remove any leftover special tokens.
        Strip extra whitespace.
        """
        # Remove end of turn token if present
        output = raw_output.replace(
            "<end_of_turn>", ""
        ).strip()

        # Remove any start of turn tokens
        output = output.replace(
            "<start_of_turn>", ""
        ).strip()

        return output

    def refine(self, user_input: str) -> str:
        """
        Main refinement function.
        Takes raw messy user input.
        Returns RISE formatted refined prompt.
        """
        # Validate input
        if not user_input or not user_input.strip():
            raise ValueError("Input cannot be empty")

        if len(user_input) > 1000:
            raise ValueError("Input too long (max 1000 chars)")

        # Build formatted prompt
        prompt = self._build_prompt(user_input.strip())

        # Run inference with all parameters
        response = self.model(
            prompt,
            **AGENT1_INFERENCE_PARAMS
        )

        # Extract generated text
        raw_output = response["choices"][0]["text"]

        # Clean and return
        refined_prompt = self._clean_output(raw_output)
        return refined_prompt

agent1_instance = Agent1()

def run_agent1(user_input: str) -> str:
    return agent1_instance.refine(user_input)