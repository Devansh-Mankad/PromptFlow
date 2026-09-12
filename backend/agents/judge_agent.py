import json
from openai import OpenAI
from backend.prompts.judge_system import JUDGE_SYSTEM_PROMPT
from backend.config.judge_settings import (
    OPENROUTER_API_KEY_A,
    OPENROUTER_API_KEY_B,
    OPENROUTER_BASE_URL,
    JUDGE_MODEL,
    REQUEST_TIMEOUT,
)

if not OPENROUTER_API_KEY_A:
    raise ValueError("OPENROUTER_API_KEY_A not found.")
if not OPENROUTER_API_KEY_B:
    raise ValueError("OPENROUTER_API_KEY_B not found.")

# Two independent OpenRouter clients
client_a = OpenAI(
    api_key=OPENROUTER_API_KEY_A,
    base_url=OPENROUTER_BASE_URL
)

client_b = OpenAI(
    api_key=OPENROUTER_API_KEY_B,
    base_url=OPENROUTER_BASE_URL
)


class JudgeAgent:
    def __init__(self):
        print("Judge Agent Ready ✓")

    def evaluate(
        self,
        query: str,
        direct_response: str,
        pipeline_response: str,
        query_index: int = 0
    ) -> dict:

        user_prompt = f"""
User Query:
{query}

Direct Response:
{direct_response}

PromptFlow Response:
{pipeline_response}
"""

        print("\n\nJudge Prompt:", user_prompt, "\n")
        if query_index % 2 == 0:
            client = client_a
            api_name = "API A"
        else:
            client = client_b
            api_name = "API B"

        print(f"Judge using {api_name}...")

        try:

            response = client.chat.completions.create(
                model=JUDGE_MODEL,
                temperature=0,
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

            # Check provider error "NoneType" Object Error"
            if getattr(response, "error", None):
                error_info = response.error
                error_message = (
                    error_info.get("message", "Unknown provider error")
                    if isinstance(error_info, dict)
                    else str(error_info)
                )

                error_code = (
                    error_info.get("code", "unknown")
                    if isinstance(error_info, dict)
                    else "unknown"
                )

                raise RuntimeError(
                    f"{api_name} provider error "
                    f"(code {error_code}): {error_message}"
                )

            if not response.choices:
                raise RuntimeError(f"{api_name} returned no response choices.")

            raw = response.choices[0].message.content
            if not raw:
                raise RuntimeError(f"{api_name} returned empty judge content.")

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
                raise RuntimeError(f"{api_name} returned invalid JSON: {e}")

            if "left" not in result:
                raise RuntimeError(f"{api_name} response missing 'left' metrics.")
            if "right" not in result:
                raise RuntimeError(f"{api_name} response missing 'right' metrics.")

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
                        f"{api_name} response missing "
                        f"left metric: {metric}"
                    )

                if metric not in right:
                    raise RuntimeError(
                        f"{api_name} response missing "
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
                "reason": result.get("reason", ""),
                "judge_api": api_name
            }

        except Exception as e:
            error_message = str(e)
            print(f"Judge Error [{api_name}]: " f"{error_message}")

            return {
                "left_metrics": {},
                "right_metrics": {},
                "winner": "Judge Failed",
                "overall_improvement": 0,
                "reason": error_message,
                "judge_api": api_name
            }

judge_agent = JudgeAgent()
def evaluate_responses(query: str,direct_response: str,pipeline_response: str,query_index: int = 0) -> dict:
    return judge_agent.evaluate(query=query,direct_response=direct_response,pipeline_response=pipeline_response,query_index=query_index)