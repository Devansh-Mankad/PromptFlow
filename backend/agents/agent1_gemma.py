from llama_cpp import Llama
from backend.prompts.agent1_system import AGENT1_SYSTEM_PROMPT
from backend.config.settings import (
    AGENT1_MODEL_PATH,
    AGENT1_LOADING_PARAMS,
    AGENT1_INFERENCE_PARAMS
)
import re

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
        """
        Clean Gemma output before sending to Agent 2.
        """
        output = raw_output
        # Remove Gemma chat tokens
        output = output.replace("<end_of_turn>", "")
        output = output.replace("<start_of_turn>", "")
        # Remove markdown code fences
        output = output.replace("```", "")
        # Normalize line endings
        output = output.replace("\r\n", "\n")
        # Remove trailing whitespace
        output = "\n".join(line.rstrip() for line in output.splitlines())
        # Collapse excessive blank lines
        output = re.sub(r"\n{3,}", "\n\n", output)
        # Remove unmatched quotes at beginning/end
        output = output.strip(" '\"")
        # Remove trailing punctuation that often breaks Agent 2
        while output.endswith(("'", '"', "`")):
            output = output[:-1].rstrip()
        # Ensure output starts with Role:
        role_index = output.find("Role:")
        if role_index != -1:
            output = output[role_index:]

        expectation = output.find("Expectation:")
        if expectation != -1:
            lines = output[expectation:].split("\n")
            cleaned = []
            for line in lines:
                cleaned.append(line)

                if len(cleaned) > 2 and line.strip() == "":
                    break

            output = (output[:expectation]+ "\n".join(cleaned))
        return output.strip()

    def _validate_output(self, text: str) -> bool:
        """
        Basic validation that the RISE prompt is usable.
        """

        required = [
            "Role:",
            "Instruction:",
            "Expectation:"
        ]

        for field in required:
            if field not in text:
                return False

        # Prevent unfinished outputs
        if text.endswith(":"):
            return False

        # Prevent unmatched quote
        if text.endswith(("'", '"', "`")):
            return False

        return True

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
        
        print("\n\nUser Query to Agent 1:" , user_input.strip(),history , "\n")

        # Build multi-turn prompt
        prompt = self._build_prompt(user_input.strip(), history)
        self.model.reset()
        response = self.model(
            prompt,
            **AGENT1_INFERENCE_PARAMS
        )

        raw_output = response["choices"][0]["text"]
        refined_prompt = self._clean_output(raw_output)
        if not self._validate_output(refined_prompt):
            self.model.reset()
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