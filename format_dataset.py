import json

# ────────────────────────────────────────
# Why this formatting is needed:
#
# Your current dataset.json has:
# {"input": "...", "output": "..."}
#
# Unsloth SFTTrainer needs:
# {"text": "<start_of_turn>user\n...<end_of_turn>\n..."}
#
# The special tokens tell Gemma exactly
# who is speaking in the conversation
# MUST match how Gemma 3 1B was pretrained
# Wrong format = model learns nothing ✗
# ────────────────────────────────────────

INPUT_FILE = "Dataset/training.json"
OUTPUT_FILE = "Dataset/formatted_training.json"

def format_pair(example):
    """
    Convert single input/output pair
    into Gemma chat template format

    <start_of_turn>user → Marks user message start
    <end_of_turn>       → Marks user message end
    <start_of_turn>model → Marks model turn start
    <end_of_turn>        → Marks model turn end
    """
    return {
        "text": (
            f"<start_of_turn>user\n"
            f"{example['input']}<end_of_turn>\n"
            f"<start_of_turn>model\n"
            f"{example['output']}<end_of_turn>"
        )
    }

def validate_pair(example, index):
    """Check each pair for common issues"""
    issues = []
    if not example.get("input", "").strip():
        issues.append(f"Empty input at index {index}")
    if not example.get("output", "").strip():
        issues.append(f"Empty output at index {index}")
    output_words = len(
        example.get("output", "").split()
    )
    if output_words < 30:
        issues.append(
            f"Very short output at {index}: "
            f"{output_words} words"
        )

    if output_words > 200:
        issues.append(
            f"Very long output at {index}: "
            f"{output_words} words"
        )
    return issues

print("Loading dataset...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_data = json.load(f)
print(f"Loaded {len(raw_data)} pairs ✓")

# Pair Validation
print("\nValidating dataset...")
all_issues = []
duplicate_inputs = {}

for i, item in enumerate(raw_data):
    issues = validate_pair(item, i)
    all_issues.extend(issues)

    # Check for duplicate inputs
    input_text = item.get("input", "").strip().lower()
    if input_text in duplicate_inputs:
        all_issues.append(
            f"Duplicate input at index {i} "
            f"and {duplicate_inputs[input_text]}"
        )
    else:
        duplicate_inputs[input_text] = i

if all_issues:
    print(f"\nFound {len(all_issues)} issues:")
    for issue in all_issues[:10]:
        print(f"  → {issue}")
    if len(all_issues) > 10:
        print(f"  ... and {len(all_issues)-10} more")
    print("\nFix these before training")
    print("Or proceed anyway if issues are minor")
else:
    print("Validation passed — no issues found")

# Format all pairs
print("\nFormatting pairs...")
formatted_data = []

for i, item in enumerate(raw_data):
    try:
        formatted = format_pair(item)
        formatted_data.append(formatted)
    except Exception as e:
        print(f"Error formatting pair {i}: {e}")
        continue
print(f"Formatted {len(formatted_data)} pairs")

# Save dataset
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(formatted_data, f,
              indent=2, ensure_ascii=False)
print(f"\nSaved to: {OUTPUT_FILE} ✓")

# Show sample to verify format
print("\nSample formatted pair:")
print(formatted_data[0]["text"])

# Final stats
print(f"\nFinal Statistics:")
print(f"  Total pairs:     {len(formatted_data)}")
print(f"  Input file:      {INPUT_FILE}")
print(f"  Output file:     {OUTPUT_FILE}")

avg_length = sum(len(item["text"].split())
    for item in formatted_data
) / len(formatted_data)
print(f"  Avg text length: {avg_length:.0f} words")