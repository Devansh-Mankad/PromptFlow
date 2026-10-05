import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from agents.agent2_main import run_agent2
import time

test_rise_prompt = """Role: Economics Professor
Instruction: Explain inflation to a first-year economics student without prior eco-background, covering its definition, causes, and impact on savings and wages.
Steps:
1. Define inflation and explain why prices go up.
2. Compare cost-push inflation and demand-pull inflation using a table.
3. Provide everyday examples and analyze how inflation affects savings and wages.
4. Debunk common economic misconceptions and conclude with a short summary.
Expectation: A clear, accessible economic explanation of inflation tailored to the specified audience without prior eco-background."""

print("="*50)
print("AGENT 2 — SOLO TEST")
print("="*50)
print("\nInput RISE Prompt:")
print("─"*50)
print(test_rise_prompt)
print("─"*50)

start = time.time()
response = run_agent2(test_rise_prompt)
elapsed = time.time() - start

print(f"\nAgent 2 Response ({elapsed:.1f}s):")
print("─"*50)
print(response)
print("─"*50)
print(f"\nWord count: {len(response.split())} words")
print("\nAgent 2 working ✓")