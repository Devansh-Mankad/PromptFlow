import sys
sys.path.append(".")
from backend.pipeline.chain import process_query, clear_history
from backend.agents.raw_agent import run_raw_agent

def run_turn(query: str) -> dict:
    result = process_query(query)

    print(f"\nRefined RISE Prompt:")
    print(result["refined_prompt"])

    print(f"\nAgent 2 Response:")
    print(result["response"])

    return result


print("PromptFlow Pipeline — Interactive Mode")
print("Type 'clear' to reset conversation history.")
print("Type 'exit' to quit.")

turn = 1
while True:
    user_input = input(f"\n[Turn {turn}] You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        print("Exiting.")
        break

    if user_input.lower() == "clear":
        clear_history()
        turn = 1
        print("History cleared. Starting fresh.")
        continue

    run_turn(user_input)
    turn += 1

# print(run_raw_agent("I am feeling col, tell me what remedies i should take for the same. I have runny nose, fever. Also my friend had cold yesterday so am i infected?"))