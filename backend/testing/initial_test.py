from llama_cpp import Llama
import time

print("Testing Agent 1 model loading...")
print("─" * 40)

start = time.time()

model = Llama(
    model_path="backend/models/agent1.gguf",
    n_ctx=512,
    n_threads=4,
    verbose=False
)

load_time = time.time() - start
print(f"Model loaded in {load_time:.1f}s ✓")
print("─" * 40)

print("Testing inference...")
start = time.time()

response = model(
    "<start_of_turn>user\nHello<end_of_turn>\n<start_of_turn>model\n",
    max_tokens=150,
    temperature=0.7,
    stop=["<end_of_turn>"],
    echo=False
)

infer_time = time.time() - start
output = response["choices"][0]["text"].strip()

print(f"Response ({infer_time:.1f}s):")
print(output)
print("─" * 40)
print("Agent 1 fully working ✓")