import csv
import time
import sys
sys.path.append(".")
from backend.pipeline.chain import process_query

test_cases = [
    ("Hello!", "GREETING"),
    ("Good morning 😊", "GREETING"),
    ("Are you still online?", "META"),
    ("Anyone there?", "META"),
    ("Thanks a lot!", "THANKS"),
    ("Really appreciate your help.", "THANKS"),
    ("Okay, got it.", "ACKNOWLEDGMENT"),
    ("Makes sense now.", "ACKNOWLEDGMENT"),
    ("Bye!", "GOODBYE"),
    ("See you later!", "GOODBYE"),
    ("Explain binary search.", "TASK"),
    ("Write Python code for merge sort.", "TASK"),
    ("Explain quantum computing simply.", "TASK"),
    ("Generate SQL query for employee table.", "TASK"),
    ("Design REST API for an e-commerce app.", "TASK"),
    ("Compare TCP and UDP.", "TASK"),
    ("Optimize this C++ code for speed.", "TASK"),
    ("Explain Docker Compose with example.", "TASK"),
    ("Create a React login page.", "TASK"),
    ("What is prompt engineering?", "TASK"),
    ("Hello, What is Gemma Model?", "TASK"),
    ("Okay that's fine. Now explain Gemma 3 1B.", "TASK"),
]

correct = 0
task_count = 0
non_task_count = 0

task_time = 0
non_task_time = 0

agent1_success = 0
agent2_success = 0
base_success = 0
csv_rows = []
print("PROMPTFLOW END-TO-END PIPELINE TEST\n\n")

for i, (query, expected_intent) in enumerate(test_cases, start=1):
    print(f"Test Case {i}/{len(test_cases)}\n")

    start = time.time()
    result = process_query(query)
    elapsed = time.time() - start

    predicted = result["intent"]
    confidence = result["confidence"]
    pipeline = result["pipeline"]

    if predicted == expected_intent:
        correct += 1
        status = "PASS"
    else:
        status = "FAIL"

    if pipeline == "PromptFlow":
        task_count += 1
        task_time += elapsed

        agent1 = "YES"
        agent2 = "YES"
        base = "NO"

        if result.get("refined_prompt"):
            agent1_success += 1

        if result.get("response"):
            agent2_success += 1

    else:
        non_task_count += 1
        non_task_time += elapsed

        agent1 = "NO"
        agent2 = "NO"
        base = "YES"

        if result.get("response"):
            base_success += 1

    print(f"Input               : {query}")
    print(f"Expected Intent     : {expected_intent}")
    print(f"Predicted Intent    : {predicted}")
    print(f"Confidence          : {confidence:.4f}")
    print(f"Pipeline Used       : {pipeline}")
    print(f"Agent 1 Used        : {agent1}")
    print(f"Agent 2 Used        : {agent2}")
    print(f"Base Assistant Used : {base}")
    print(f"Execution Time      : {elapsed:.2f} sec")
    print(f"Result              : {status}")

    print("\nResponse Preview\n")
    print(result.get("response", ""),"\n\n")

    csv_rows.append([
        i,
        query,
        expected_intent,
        predicted,
        f"{confidence:.4f}",
        pipeline,
        agent1,
        agent2,
        base,
        result.get("refined_prompt", ""),
        result.get("response", ""),
        f"{elapsed:.2f}",
        status
    ])

accuracy = (correct / len(test_cases)) * 100

avg_task_time = (
    task_time / task_count
    if task_count else 0
)

avg_non_task_time = (
    non_task_time / non_task_count
    if non_task_count else 0
)

with open(
    "pipeline_test_report.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Test No",
        "Input",
        "Expected Intent",
        "Predicted Intent",
        "Confidence",
        "Pipeline Used",
        "Agent 1 Used",
        "Agent 2 Used",
        "Base Assistant Used",
        "Refined Prompt",
        "Final Response",
        "Execution Time (sec)",
        "Result"
    ])

    writer.writerows(csv_rows)

    writer.writerow([])
    writer.writerow(["Total Test Cases", len(test_cases)])
    writer.writerow(["Correct Routing", correct])
    writer.writerow(["Routing Accuracy", f"{accuracy:.2f}%"])
    writer.writerow(["PromptFlow Invocations", task_count])
    writer.writerow(["Base Assistant Calls", non_task_count])
    writer.writerow(["Agent 1 Success", f"{agent1_success}/{task_count}"])
    writer.writerow(["Agent 2 Success", f"{agent2_success}/{task_count}"])
    writer.writerow(["Base Assistant Success", f"{base_success}/{non_task_count}"])
    writer.writerow(["Average TASK Time", f"{avg_task_time:.2f} sec"])
    writer.writerow(["Average NON-TASK Time", f"{avg_non_task_time:.2f} sec"])

print("\n")
print("FINAL PIPELINE EVALUATION\n\n")

print(f"Total Test Cases        : {len(test_cases)}")
print(f"Correct Routing         : {correct}")
print(f"Routing Accuracy        : {accuracy:.2f}%")
print()

print(f"PromptFlow Invocations  : {task_count}")
print(f"Base Assistant Calls    : {non_task_count}")
print()

print(f"Agent 1 Success         : {agent1_success}/{task_count}")
print(f"Agent 2 Success         : {agent2_success}/{task_count}")
print(f"Base Assistant Success  : {base_success}/{non_task_count}")
print()

print(f"Average TASK Time       : {avg_task_time:.2f} sec")
print(f"Average NON-TASK Time   : {avg_non_task_time:.2f} sec")

print("\nDetailed report saved as:")
print("pipeline_test_report.csv")
