import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from agents.agent2_main import run_agent2
import time

test_rise_prompt = """explain quantum physics simply"""

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