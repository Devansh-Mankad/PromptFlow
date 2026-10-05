import json
from openai import OpenAI

from backend.prompts.judge_system import JUDGE_SYSTEM_PROMPT
from backend.config.ollama_settings import (
    OLLAMA_BASE_URL,
    JUDGE_MODEL,
    REQUEST_TIMEOUT,
    TEMPERATURE,
    TOP_P,
)

# Ollama OpenAI-compatible client
client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama"
)

class JudgeAgent:
    def __init__(self):
        print("Judge Agent Ready ✓")
        print(f"Judge Provider: Ollama Cloud")
        print(f"Judge Model: {JUDGE_MODEL}")

    def evaluate(self,query: str,direct_response: str,pipeline_response: str,query_index: int = 0) -> dict:

        user_prompt = f"""
User Query:
{query}

Direct Response:
{direct_response}

PromptFlow Response:
{pipeline_response}
"""

        print("\n\nJudge Prompt:", user_prompt, "\n")
        print("Judge using Ollama Cloud...")
        print(f"Model: {JUDGE_MODEL}")

        try:

            response = client.chat.completions.create(
                model=JUDGE_MODEL,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                messages=[
                    {
                        "role": "system",
                        "content": JUDGE_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                timeout=REQUEST_TIMEOUT
            )
            actual_model = getattr(response,"model",JUDGE_MODEL)
            print(f"Requested model: {JUDGE_MODEL}")
            print(f"Actual model used: {actual_model}")


            if not response.choices:
                raise RuntimeError("Ollama returned no response choices.")

            raw = response.choices[0].message.content
            if not raw:
                raise RuntimeError("Ollama returned empty judge content.")

            raw = raw.strip()
            if raw.startswith("```json"):
                raw = raw[7:]
            elif raw.startswith("```"):
                raw = raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()

            try:
                result = json.loads(raw)
            except json.JSONDecodeError as e:
                raise RuntimeError(
                    f"Ollama returned invalid JSON: {e}\n"
                    f"Raw response:\n{raw}"
                )

            if "left" not in result:
                raise RuntimeError("Ollama response missing 'left' metrics.")

            if "right" not in result:
                raise RuntimeError("Ollama response missing 'right' metrics.")

            left = result["left"]
            right = result["right"]
            required_metrics = [
                "relevance",
                "clarity",
                "completeness",
                "actionability",
                "structure",
                "depth"
            ]

            for metric in required_metrics:
                if metric not in left:
                    raise RuntimeError(
                        f"Ollama response missing "
                        f"left metric: {metric}"
                    )

                if metric not in right:
                    raise RuntimeError(
                        f"Ollama response missing "
                        f"right metric: {metric}"
                    )

            left_total = sum(
                left[metric]
                for metric in required_metrics
            )

            right_total = sum(
                right[metric]
                for metric in required_metrics
            )

            if right_total > left_total:
                winner = "PromptFlow Pipeline"
            elif left_total > right_total:
                winner = "Direct Response"
            else:
                winner = "Equivalent Performance"


            if left_total == 0:
                improvement = 0
            else:
                improvement = round(((right_total - left_total) / left_total) * 100,2)

            return {
                "left_metrics": left,
                "right_metrics": right,
                "winner": winner,
                "overall_improvement": improvement,
                "reason": result.get("reason",""),
                "judge_api": "Ollama Cloud",
                "requested_model": JUDGE_MODEL,
                "actual_model": actual_model
            }

        except Exception as e:
            error_message = str(e)
            print(
                f"Judge Error [Ollama Cloud]: "
                f"{error_message}"
            )

            return {
                "left_metrics": {},
                "right_metrics": {},
                "winner": "Judge Failed",
                "overall_improvement": 0,
                "reason": error_message,
                "judge_api": "Ollama Cloud",
                "requested_model": JUDGE_MODEL
            }

judge_agent = JudgeAgent()

def evaluate_responses(
    query: str,
    direct_response: str,
    pipeline_response: str,
    query_index: int = 0
) -> dict:
    return judge_agent.evaluate(
        query=query,
        direct_response=direct_response,
        pipeline_response=pipeline_response,
        query_index=query_index
    )