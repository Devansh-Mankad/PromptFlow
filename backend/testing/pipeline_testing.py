import sys
sys.path.append(".")
from backend.pipeline.chain import process_query, clear_history

# ANSI colors for readable output
GREEN  = "\033[92m"
BLUE   = "\033[94m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RED    = "\033[91m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def divider(title: str = ""):
    line = "─" * 60
    if title:
        print(f"\n{BOLD}{line}{RESET}")
        print(f"{BOLD}  {title}{RESET}")
        print(f"{BOLD}{line}{RESET}")
    else:
        print(f"{line}")

def run_turn(turn_number: int, query: str) -> dict:
    print(f"\n{BLUE}{BOLD}[Turn {turn_number}] User:{RESET} {query}")
    result = process_query(query)

    print(f"\n{YELLOW}{BOLD}  → Refined RISE Prompt:{RESET}")
    for line in result["refined_prompt"].splitlines():
        print(f"    {line}")

    print(f"\n{GREEN}{BOLD}  → Agent 2 Response:{RESET}")
    # Print first 300 chars to keep output readable
    preview = result["response"][:300]
    if len(result["response"]) > 300:
        preview += "..."
    for line in preview.splitlines():
        print(f"    {line}")

    return result

def check_context(rise_prompt: str, expected_keyword: str) -> bool:
    """Check if the RISE prompt contains the expected topic keyword."""
    return expected_keyword.lower() in rise_prompt.lower()


# TEST SUITE 1 — Linux follow-up chain
divider("TEST SUITE 1 — Follow-up pronoun resolution (Linux)")
clear_history()
r1 = run_turn(1, "Explain Linux")
divider()

r2 = run_turn(2, "What are its applications?")
t2_pass = check_context(r2["refined_prompt"], "linux")
print(f"\n  {GREEN}✓ PASS{RESET}" if t2_pass else f"\n  {RED}✗ FAIL — 'linux' not found in RISE prompt{RESET}")
divider()

r3 = run_turn(3, "Compare it with Windows")
t3_pass = check_context(r3["refined_prompt"], "linux")
print(f"\n  {GREEN}✓ PASS{RESET}" if t3_pass else f"\n  {RED}✗ FAIL — 'linux' not found in RISE prompt{RESET}")
divider()

r4 = run_turn(4, "Give me some examples")
t4_pass = check_context(r4["refined_prompt"], "linux")
print(f"\n  {GREEN}✓ PASS{RESET}" if t4_pass else f"\n  {RED}✗ FAIL — 'linux' not found in RISE prompt{RESET}")
divider()

r5 = run_turn(5, "Explain it in more detail")
t5_pass = check_context(r5["refined_prompt"], "linux")
print(f"\n  {GREEN}✓ PASS{RESET}" if t5_pass else f"\n  {RED}✗ FAIL — 'linux' not found in RISE prompt{RESET}")

# TEST SUITE 2 — Topic switch (Docker after Linux)
divider("TEST SUITE 2 — Topic switch detection")
clear_history()

run_turn(1, "Explain Linux")
divider()

r2 = run_turn(2, "Now explain Docker")
t2_pass = check_context(r2["refined_prompt"], "docker")
print(f"\n  {GREEN}✓ PASS{RESET}" if t2_pass else f"\n  {RED}✗ FAIL — 'docker' not found in RISE prompt{RESET}")
divider()

r3 = run_turn(3, "How does it work internally?")
t3_pass = check_context(r3["refined_prompt"], "docker")
print(f"\n  {GREEN}✓ PASS{RESET}" if t3_pass else f"\n  {RED}✗ FAIL — expected 'docker', not 'linux'{RESET}")

# TEST SUITE 3 — Independent query (no history needed)
divider("TEST SUITE 3 — Independent query (fresh history)")
clear_history()

r1 = run_turn(1, "What is machine learning?")
t1_pass = check_context(r1["refined_prompt"], "machine learning")
print(f"\n  {GREEN}✓ PASS{RESET}" if t1_pass else f"\n  {RED}✗ FAIL — 'machine learning' not in RISE prompt{RESET}")


# TEST SUITE 4 — History trim (more than MAX_TURNS)
divider("TEST SUITE 4 — History trimming (6 turns, MAX=5)")
clear_history()

topics = [
    "Explain Python",
    "Explain JavaScript",
    "Explain Rust",
    "Explain Go",
    "Explain TypeScript",
    "Explain Kotlin",        # 6th turn — oldest (Python) should be trimmed
]

for i, topic in enumerate(topics, 1):
    run_turn(i, topic)
    divider()

r7 = run_turn(7, "What are its main use cases?")
t7_pass = check_context(r7["refined_prompt"], "kotlin")
print(f"\n  {GREEN}✓ PASS — references Kotlin (last topic){RESET}"
      if t7_pass
      else f"\n  {RED}✗ FAIL — should reference 'kotlin', got: {r7['refined_prompt'][:100]}{RESET}")


# SUMMARY
divider("RESULTS SUMMARY")

results = {
    "Suite 1 — Turn 2 (its applications)":     t2_pass,
    "Suite 1 — Turn 3 (compare it)":           t3_pass,
    "Suite 1 — Turn 4 (give examples)":        t4_pass,
    "Suite 1 — Turn 5 (more detail)":          t5_pass,
    "Suite 2 — Topic switch to Docker":         t2_pass,
    "Suite 2 — Follow-up after switch":         t3_pass,
    "Suite 3 — Independent query":              t1_pass,
    "Suite 4 — History trim (Kotlin)":          t7_pass,
}

passed = sum(results.values())
total  = len(results)
for name, passed_flag in results.items():
    icon = f"{GREEN}✓{RESET}" if passed_flag else f"{RED}✗{RESET}"
    print(f"  {icon}  {name}")

print(f"\n{BOLD}  Score: {passed}/{total}{RESET}")

if passed == total:
    print(f"\n{GREEN}{BOLD}  All tests passed. Conversation history is working correctly.{RESET}\n")
else:
    print(f"\n{RED}{BOLD}  {total - passed} test(s) failed. Agent 1 is not resolving context reliably.{RESET}\n")
    print(f"{YELLOW}  Tip: Check your AGENT1_SYSTEM_PROMPT — it should instruct Agent 1 to")
    print(f"  resolve pronouns like 'it', 'its', 'this' using conversation history.{RESET}\n")