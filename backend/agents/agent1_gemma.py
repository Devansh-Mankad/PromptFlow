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
    """

    def __init__(self):
        self.model = None

    def _load_model(self):
        print("Loading Agent 1 — Gemma 3 1B...")
        print(f"Model path: {AGENT1_MODEL_PATH}")

        self.model = Llama(
            model_path=AGENT1_MODEL_PATH,
            **AGENT1_LOADING_PARAMS
        )

        print("Agent 1 loaded successfully!\n")

    def _unload_model(self):
        if self.model is not None:
            del self.model
            self.model = None

    def _build_prompt(self,user_input: str) -> str:
        prompt = (
            f"<start_of_turn>system\n"
            f"{AGENT1_SYSTEM_PROMPT}<end_of_turn>\n"
        )

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
        output = output.replace("<end_of_turn>", "")
        output = output.replace("<start_of_turn>", "")
        output = output.replace("```", "")
        output = output.replace("\r\n", "\n")
        output = "\n".join(line.rstrip() for line in output.splitlines())
        output = re.sub(r"\n{3,}", "\n\n", output)
        output = output.strip(" '\"")

        while output.endswith(("'", '"', "`")):
            output = output[:-1].rstrip()

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

            output = (output[:expectation] + "\n".join(cleaned))

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

        if text.endswith(":"):
            return False

        if text.endswith(("'", '"', "`")):
            return False

        return True

    def refine(self, user_input: str) -> str:
        """
        Main refinement function.
        Takes raw user input.
        Returns RISE formatted refined prompt.
        """
        if not user_input or not user_input.strip():
            raise ValueError("Input cannot be empty")

        if len(user_input) > 1000:
            raise ValueError("Input too long (max 1000 chars)")

        print("\n\nUser Query to Agent 1:", user_input.strip(), "\n")

        self._load_model()

        print("\nCache Cleared!\n")
        self.model.reset()

        try:
            prompt = self._build_prompt(user_input.strip())
            response = self.model(
                prompt,
                **AGENT1_INFERENCE_PARAMS
            )

            raw_output = response["choices"][0]["text"]
            refined_prompt = self._clean_output(raw_output)

            if not self._validate_output(refined_prompt):
                response = self.model(
                    prompt,
                    **AGENT1_INFERENCE_PARAMS
                )

                raw_output = response["choices"][0]["text"]
                refined_prompt = self._clean_output(raw_output)

            return refined_prompt

        finally:
            self._unload_model()
            print("Model Unloaded!\n")


agent1_instance = Agent1()

def run_agent1(user_input: str) -> str:
    return agent1_instance.refine(user_input)