from llama_cpp import Llama
from prompts.agent2_system import AGENT2_SYSTEM_PROMPT
from config.settings import (
    AGENT2_MODEL_PATH,
    AGENT2_LOADING_PARAMS,
    AGENT2_INFERENCE_PARAMS
)

class Agent2:
    """
    PromptForge Agent 2 — Response Generator
    Loads Gemma 4 E2B QAT GGUF model
    Receives RISE refined prompt from Agent 1
    Generates high quality final response
    """

    def __init__(self):
        print("Loading Agent 2 — Gemma 4 E2B...")
        print(f"Model path: {AGENT2_MODEL_PATH}")

        self.model = Llama(
            model_path=AGENT2_MODEL_PATH,
            **AGENT2_LOADING_PARAMS
        )
        print("Agent 2 loaded successfully ✓")

    def _build_prompt(
        self, refined_prompt: str
    ) -> str:
        """
        Build Gemma 4 chat template prompt.
        System prompt sets Agent 2 behavior.
        Refined RISE prompt is user turn.
        Model generates final response.
        """
        return (
            f"<start_of_turn>system\n"
            f"{AGENT2_SYSTEM_PROMPT}<end_of_turn>\n"
            f"<start_of_turn>user\n"
            f"{refined_prompt}<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )

    def _clean_output(self, raw: str) -> str:
        """Clean special tokens from output"""
        output = raw.replace(
            "<end_of_turn>", ""
        ).strip()
        output = output.replace(
            "<start_of_turn>", ""
        ).strip()
        return output

    def respond(self, refined_prompt: str) -> str:
        """
        Generate final response.
        Takes RISE format prompt from Agent 1.
        Returns complete high quality answer.
        """
        if not refined_prompt or \
           not refined_prompt.strip():
            raise ValueError(
                "Refined prompt cannot be empty"
            )

        prompt = self._build_prompt(
            refined_prompt.strip()
        )

        response = self.model(
            prompt,
            **AGENT2_INFERENCE_PARAMS
        )

        raw = response["choices"][0]["text"]
        return self._clean_output(raw)


# Load once at startup
print("Initializing Agent 2...")
agent2_instance = Agent2()


def run_agent2(refined_prompt: str) -> str:
    """Public function for pipeline to call"""
    return agent2_instance.respond(refined_prompt)