import json

INPUT_FILE = "C:/Users/devan/AllProjects/PromptFlow/Dataset/intent_dataset.json"
OUTPUT_FILE = "C:/Users/devan/AllProjects/PromptFlow/Dataset/intent_dataset_cleaned.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    dataset = json.load(f)

print(f"Original samples : {len(dataset)}")
seen = set()
cleaned_dataset = []

for sample in dataset:
    key = (
        sample["text"].strip().lower(),
        sample["label"]
    )
    if key not in seen:
        seen.add(key)
        cleaned_dataset.append(sample)

print(f"Unique samples   : {len(cleaned_dataset)}")
print(f"Duplicates removed: {len(dataset) - len(cleaned_dataset)}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_dataset, f, indent=2, ensure_ascii=False)

print(f"\n✅ Clean dataset saved to:\n{OUTPUT_FILE}")