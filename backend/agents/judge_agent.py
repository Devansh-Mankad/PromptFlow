import json

from openai import OpenAI

from backend.prompts.judge_system import (
    JUDGE_SYSTEM_PROMPT
)

from backend.config.judge_settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    JUDGE_MODEL,
    REQUEST_TIMEOUT,
)

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found."
    )

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
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
    ) -> dict:

        user_prompt = f"""
User Query:
{query}

Direct Response:
{direct_response}

PromptForge Response:
{pipeline_response}
"""

        try:
            response = (
                client.chat.completions.create(
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
            )

            raw = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            raw = (
                raw.replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

            result = json.loads(raw)

            left = result["left"]
            right = result["right"]

            left_total = sum(
                left.values()
            )

            right_total = sum(
                right.values()
            )

            if right_total > left_total:
                winner = (
                    "PromptForge Pipeline"
                )

            elif left_total > right_total:
                winner = (
                    "Direct Response"
                )

            else:
                winner = (
                    "PromptForge Pipeline"
                )

            if left_total == 0:
                improvement = 0

            else:
                improvement = round(
                    (
                        (
                            right_total
                            - left_total
                        )
                        / left_total
                    )
                    * 100,
                    2
                )

            return {
                "left_metrics": left,
                "right_metrics": right,
                "winner": winner,
                "overall_improvement": improvement,
                "reason": result.get(
                    "reason",
                    ""
                )
            }

        except Exception as e:
            print(
                f"Judge Error: {e}"
            )

            return {
                "left_metrics": {},
                "right_metrics": {},
                "winner": "Judge Failed",
                "overall_improvement": 0,
                "reason": str(e)
            }


judge_agent = JudgeAgent()


def evaluate_responses(
    query: str,
    direct_response: str,
    pipeline_response: str
) -> dict:

    return judge_agent.evaluate(
        query,
        direct_response,
        pipeline_response
    )