import json
import re

INPUT_FILE = "C:/Users/devan/Downloads/dataset_final.txt"
OUTPUT_FILE = "C:/Users/devan/AllProjects/PromptFlow/Dataset/training/Final Dataset/dataset_cleaned.json"


def extract_user_query(text):
    """Extract only the content between the user turn markers."""
    match = re.search(
        r"<start_of_turn>user\s*(.*?)\s*<end_of_turn>",
        text,
        re.DOTALL
    )

    if not match:
        return None

    return match.group(1).strip()


# Load dataset
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

seen_queries = set()
cleaned_data = []

duplicate_count = 0

for item in data:
    text = item.get("text", "")

    user_query = extract_user_query(text)

    if user_query is None:
        # Keep malformed records instead of silently deleting them
        cleaned_data.append(item)
        continue

    # Normalize only for duplicate detection
    # Original query remains unchanged in the dataset.
    normalized_query = re.sub(r"\s+", " ", user_query).strip().lower()

    if normalized_query in seen_queries:
        duplicate_count += 1
        continue

    seen_queries.add(normalized_query)
    cleaned_data.append(item)


# Save cleaned dataset
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)


print("========== DATASET CLEANING ==========")
print(f"Original records : {len(data)}")
print(f"Duplicate records: {duplicate_count}")
print(f"Final records    : {len(cleaned_data)}")
print(f"Removed          : {len(data) - len(cleaned_data)}")
print(f"Output file      : {OUTPUT_FILE}")
print("======================================")