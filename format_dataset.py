# import json
# INPUT_FILE = "Dataset/training.json"
# OUTPUT_FILE = "Dataset/formatted_training.json"

# def format_pair(example):
#     """
#     Convert single input/output pair
#     into Gemma chat template format

#     <start_of_turn>user → Marks user message start
#     <end_of_turn>       → Marks user message end
#     <start_of_turn>model → Marks model turn start
#     <end_of_turn>        → Marks model turn end
#     """
#     return {
#         "text": (
#             f"<start_of_turn>user\n"
#             f"{example['input']}<end_of_turn>\n"
#             f"<start_of_turn>model\n"
#             f"{example['output']}<end_of_turn>"
#         )
#     }

# def validate_pair(example, index):
#     """Check each pair for common issues"""
#     issues = []
#     if not example.get("input", "").strip():
#         issues.append(f"Empty input at index {index}")
#     if not example.get("output", "").strip():
#         issues.append(f"Empty output at index {index}")
#     output_words = len(
#         example.get("output", "").split()
#     )
#     if output_words < 30:
#         issues.append(
#             f"Very short output at {index}: "
#             f"{output_words} words"
#         )

#     if output_words > 200:
#         issues.append(
#             f"Very long output at {index}: "
#             f"{output_words} words"
#         )
#     return issues

# print("Loading dataset...")
# with open(INPUT_FILE, "r", encoding="utf-8") as f:
#     raw_data = json.load(f)
# print(f"Loaded {len(raw_data)} pairs ✓")

# # Pair Validation
# print("\nValidating dataset...")
# all_issues = []
# duplicate_inputs = {}

# for i, item in enumerate(raw_data):
#     issues = validate_pair(item, i)
#     all_issues.extend(issues)

#     # Check for duplicate inputs
#     input_text = item.get("input", "").strip().lower()
#     if input_text in duplicate_inputs:
#         all_issues.append(
#             f"Duplicate input at index {i} "
#             f"and {duplicate_inputs[input_text]}"
#         )
#     else:
#         duplicate_inputs[input_text] = i

# if all_issues:
#     print(f"\nFound {len(all_issues)} issues:")
#     for issue in all_issues[:10]:
#         print(f"  → {issue}")
#     if len(all_issues) > 10:
#         print(f"  ... and {len(all_issues)-10} more")
#     print("\nFix these before training")
#     print("Or proceed anyway if issues are minor")
# else:
#     print("Validation passed — no issues found")

# # Format all pairs
# print("\nFormatting pairs...")
# formatted_data = []

# for i, item in enumerate(raw_data):
#     try:
#         formatted = format_pair(item)
#         formatted_data.append(formatted)
#     except Exception as e:
#         print(f"Error formatting pair {i}: {e}")
#         continue
# print(f"Formatted {len(formatted_data)} pairs")

# # Save dataset
# with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#     json.dump(formatted_data, f,
#               indent=2, ensure_ascii=False)
# print(f"\nSaved to: {OUTPUT_FILE} ✓")

# # Show sample to verify format
# print("\nSample formatted pair:")
# print(formatted_data[0]["text"])

# # Final stats
# print(f"\nFinal Statistics:")
# print(f"  Total pairs:     {len(formatted_data)}")
# print(f"  Input file:      {INPUT_FILE}")
# print(f"  Output file:     {OUTPUT_FILE}")

# avg_length = sum(len(item["text"].split())
#     for item in formatted_data
# ) / len(formatted_data)
# print(f"  Avg text length: {avg_length:.0f} words")/

# import json

# INPUT_FILE = "Dataset/training.json"
# OUTPUT_FILE = "Dataset/formatted_training2.json"

# with open(INPUT_FILE, "r", encoding="utf-8") as f:
#     data = json.load(f)

# seen = set()
# clean_data = []

# for item in data:
#     text = item["text"].strip()

#     if text not in seen:
#         seen.add(text)
#         clean_data.append(item)

# with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#     json.dump(clean_data, f, indent=2, ensure_ascii=False)

# print(f"Original: {len(data)}")
# print(f"Unique: {len(clean_data)}")
# print(f"Removed: {len(data) - len(clean_data)}")

import json
import re
from pathlib import Path

INPUT_FILE = "C:/Users/devan/AllProjects/PromptFlow/Dataset/formatted_training1.json"      # Your current dataset
OUTPUT_FILE = "C:/Users/devan/AllProjects/PromptFlow/Dataset/qwen_chat_dataset.json"

def extract_messages(text):
    user_pattern = (
        r"<start_of_turn>user\s*"
        r"(.*?)"
        r"\s*<end_of_turn>"
    )

    assistant_pattern = (
        r"<start_of_turn>model\s*"
        r"(.*?)"
        r"\s*<end_of_turn>"
    )

    user_match = re.search(user_pattern, text, re.DOTALL)
    assistant_match = re.search(assistant_pattern, text, re.DOTALL)

    if not user_match or not assistant_match:
        return None

    user = user_match.group(1).strip()
    assistant = assistant_match.group(1).strip()

    return {
        "messages": [
            {
                "role": "user",
                "content": user
            },
            {
                "role": "assistant",
                "content": assistant
            }
        ]
    }


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

converted = []

failed = 0

for sample in data:

    text = sample.get("text", "")

    result = extract_messages(text)

    if result:
        converted.append(result)
    else:
        failed += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(converted, f, indent=2, ensure_ascii=False)

print("=" * 50)
print("Conversion Complete")
print("=" * 50)
print(f"Converted : {len(converted)}")
print(f"Failed    : {failed}")
print(f"Saved To  : {OUTPUT_FILE}")