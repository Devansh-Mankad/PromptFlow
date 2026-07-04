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
    Supports multi-turn conversation history
    """

    def __init__(self):
        print("Loading Agent 1 — Gemma 3 1B...")
        print(f"Model path: {AGENT1_MODEL_PATH}")
        self.model = Llama(
            model_path=AGENT1_MODEL_PATH,
            **AGENT1_LOADING_PARAMS
        )
        print("Agent 1 loaded successfully ✓")

    def _build_prompt(self,user_input: str,history: list[dict]) -> str:
        """
        Build multi-turn Gemma chat template.

        history format:
        [
            {"role": "user",  "content": "Explain Linux"},
            {"role": "model", "content": "Role: Linux Expert..."},
            {"role": "user",  "content": "What are its uses?"},
            {"role": "model", "content": "Role: Linux Expert..."},
        ]

        Each "model" turn is Agent 1's previous RISE output.
        This gives Agent 1 full context to resolve follow-ups.
        """
        prompt = (
            f"<start_of_turn>system\n"
            f"{AGENT1_SYSTEM_PROMPT}<end_of_turn>\n"
        )

        # Inject previous turns
        for turn in history:
            role = turn["role"]   # "user" or "model"
            content = turn["content"]
            prompt += (
                f"<start_of_turn>{role}\n"
                f"{content}<end_of_turn>\n"
            )

        # Append current user message
        prompt += (
            f"<start_of_turn>user\n"
            f"{user_input}<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )

        return prompt

    def _clean_output(self, raw_output: str) -> str:
        output = raw_output.replace("<end_of_turn>", "").strip()
        output = output.replace("<start_of_turn>", "").strip()
        return output

    def refine(self, user_input: str, history: list[dict]) -> str:
        """
        Main refinement function.
        Takes raw user input + conversation history.
        Returns RISE formatted refined prompt.
        """
        if not user_input or not user_input.strip():
            raise ValueError("Input cannot be empty")

        if len(user_input) > 1000:
            raise ValueError("Input too long (max 1000 chars)")

        # Build multi-turn prompt
        prompt = self._build_prompt(user_input.strip(), history)

        response = self.model(
            prompt,
            **AGENT1_INFERENCE_PARAMS
        )

        raw_output = response["choices"][0]["text"]
        refined_prompt = self._clean_output(raw_output)
        return refined_prompt


agent1_instance = Agent1()

def run_agent1(user_input: str, history: list[dict]) -> str:
    return agent1_instance.refine(user_input, history)