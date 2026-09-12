import re
import requests

from backend.config.settings import (
    OLLAMA_HOST,
    AGENT1_OLLAMA_MODEL
)


class Agent1:
    """
    PromptFlow Agent 1 — Prompt Refiner

    Uses Ollama to run the fine-tuned Gemma 3 1B GGUF model.

    System prompt and inference parameters
    are configured entirely in the Ollama Modelfile.
    """

    def __init__(self):
        self.ollama_url = f"{OLLAMA_HOST}/api/chat"

    def _clean_output(self, raw_output: str) -> str:
        """
        Remove only unwanted model artifacts.
        Do not modify the actual RISE content.
        """

        output = raw_output.strip()

        # Remove model special tokens
        output = output.replace("<start_of_turn>", "")
        output = output.replace("<end_of_turn>", "")
        output = output.replace("<eos>", "")

        # Remove markdown fences only
        output = output.replace("```text", "")
        output = output.replace("```", "")

        # Normalize line endings
        output = output.replace("\r\n", "\n")

        # Remove trailing spaces
        output = "\n".join(
            line.rstrip()
            for line in output.splitlines()
        )

        # Collapse excessive blank lines
        output = re.sub(r"\n{3,}", "\n\n", output)

        # If model added text before Role:
        role_match = re.search(
            r"(?m)^Role:\s*",
            output
        )

        if role_match:
            output = output[role_match.start():]

        return output.strip()

    def _validate_output(self, text: str) -> bool:
        """
        Strict validation of RISE structure.
        """

        if not text:
            return False

        # Required sections
        pattern = re.compile(
            r"^Role:\s*.+?"
            r"\nInstruction:\s*.+?"
            r"\nSteps:\s*.+?"
            r"\nExpectation:\s*.+$",
            re.DOTALL
        )

        if not pattern.match(text):
            return False

        # Count sections exactly once
        sections = [
            "Role:",
            "Instruction:",
            "Steps:",
            "Expectation:"
        ]

        for section in sections:
            if text.count(section) != 1:
                return False

        # Make sure correct order is preserved
        positions = [
            text.find("Role:"),
            text.find("Instruction:"),
            text.find("Steps:"),
            text.find("Expectation:")
        ]

        if positions != sorted(positions):
            return False

        # Must start with Role:
        if not text.startswith("Role:"):
            return False

        # Must not end with a section heading
        if text.rstrip().endswith(
            ("Role:", "Instruction:", "Steps:", "Expectation:")
        ):
            return False

        # Avoid obvious unfinished output
        if text.rstrip().endswith(("'", '"', "`")):
            return False

        return True

    def _generate(
        self,
        user_input: str,
        retry: bool = False
    ) -> str:
        """
        Send request to Ollama.

        System prompt and inference parameters
        are handled entirely by the Modelfile.
        """

        if retry:
            content = (
                f"{user_input}\n\n"
                "Rewrite this as a valid RISE prompt. "
                "Return only Role, Instruction, Steps, and Expectation. "
                "Do not answer the query or add information."
            )
        else:
            content = user_input

        payload = {
            "model": AGENT1_OLLAMA_MODEL,

            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],

            "stream": False,
            "think": False,

            # Unload model after generation
            "keep_alive": 0
        }

        response = requests.post(
            self.ollama_url,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]

    def refine(self, user_input: str) -> str:
        """
        Main refinement function.

        Takes raw user input and returns
        a validated RISE prompt.
        """

        if not user_input or not user_input.strip():
            raise ValueError("Input cannot be empty")

        if len(user_input) > 1000:
            raise ValueError(
                "Input too long (max 1000 chars)"
            )

        user_input = user_input.strip()

        print(
            "\n\nUser Query to Agent 1:",
            user_input,
            "\n"
        )

        print("Sending request to Ollama...")

        try:
            # -------------------------
            # ATTEMPT 1
            # -------------------------

            raw_output = self._generate(
                user_input,
                retry=False
            )

            refined_prompt = self._clean_output(
                raw_output
            )

            if self._validate_output(refined_prompt):
                return refined_prompt

            print("Agent 1 output invalid.")
            print("Retrying with format correction...")

            # -------------------------
            # ATTEMPT 2
            # -------------------------

            raw_output = self._generate(
                user_input,
                retry=True
            )

            refined_prompt = self._clean_output(
                raw_output
            )

            if self._validate_output(refined_prompt):
                return refined_prompt

            raise ValueError(
                "Agent 1 produced an invalid RISE prompt "
                "after retry."
            )

        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"Ollama request failed: {e}"
            ) from e


agent1_instance = Agent1()

def run_agent1(user_input: str) -> str:
    return agent1_instance.refine(user_input)