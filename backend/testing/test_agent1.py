import json
import time
import sys
sys.path.append(".")
from backend.agents.agent1_gemma import run_agent1

def count_tokens(text):
    return len(text.split())

VALIDATION_FILE = "C:/Users/devan/AllProjects/PromptFlow/Dataset/agent1_validation.json"
OUTPUT_FILE = "C:/Users/devan/AllProjects/PromptFlow/Dataset/agent1_validation_output.json"

with open(VALIDATION_FILE, "r", encoding="utf-8") as f:
    test_queries = json.load(f)

results = []
print("PROMPTFLOW AGENT 1 VALIDATION")
print(f"Loaded {len(test_queries)} samples")
print()

for item in test_queries:
    sample_id = item["id"]
    category = item["category"]
    print(f"[{sample_id:03}] {category}")
    start_time = time.time()

    try:
        if "conversation" in item:
            history = []
            turns = []
            for message in item["conversation"]:
                refined_prompt = run_agent1(message,history)

                turns.append({
                    "user_input": message,
                    "refined_prompt": refined_prompt
                })

                history.append({
                    "role": "user",
                    "content": message
                })

                history.append({
                    "role": "model",
                    "content": refined_prompt
                })

            latency = round(time.time() - start_time,2)
            total_input_tokens = sum(count_tokens(t["user_input"]) for t in turns)
            total_output_tokens = sum(count_tokens(t["refined_prompt"]) for t in turns)

            result = {
                "id": sample_id,
                "category": category,
                "conversation": turns,
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "expansion_ratio": round(
                    total_output_tokens /
                    max(total_input_tokens, 1),
                    2
                ),
                "latency_seconds": latency
            }

        else:
            user_query = item["query"]
            refined_prompt = run_agent1(user_query,[])

            latency = round(time.time() - start_time,2)
            input_tokens = count_tokens(user_query)
            output_tokens = count_tokens(refined_prompt)

            result = {
                "id": sample_id,
                "category": category,
                "user_input": user_query,
                "refined_prompt": refined_prompt,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "expansion_ratio": round(
                    output_tokens /
                    max(input_tokens, 1),
                    2
                ),
                "latency_seconds": latency
            }

        results.append(result)
        print(f"✓ Time:{result['latency_seconds']}s")

    except Exception as e:
        print(f"✗ Error: {e}")
        results.append({
            "id": sample_id,
            "category": category,
            "error": str(e)
        })

    with open(OUTPUT_FILE,"w",encoding="utf-8") as f:
        json.dump(results,f,indent=2,ensure_ascii=False)

print()
print("VALIDATION COMPLETE")

successful = [r for r in results if "error" not in r]
failed = [r for r in results if "error" in r]
total_input_tokens = sum(r.get("input_tokens", 0) for r in successful)
total_output_tokens = sum(r.get("output_tokens", 0) for r in successful)
avg_latency = round(sum(r.get("latency_seconds", 0) for r in successful) / max(len(successful), 1),2)
avg_ratio = round(sum(r.get("expansion_ratio", 0) for r in successful) / max(len(successful), 1),2)

print(f"Total Samples: {len(results)}")
print(f"Successful: {len(successful)}")
print(f"Failed: {len(failed)}")
print(f"Input Tokens: {total_input_tokens}")
print(f"Output Tokens: {total_output_tokens}")
print(f"Average Expansion: {avg_ratio}x")
print(f"Average Latency: {avg_latency}s")
print()
print(f"Saved Results -> {OUTPUT_FILE}")