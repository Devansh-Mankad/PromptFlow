from sklearn.metrics import confusion_matrix, classification_report,ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import sys
sys.path.append(".")
from backend.pipeline.intent_classifier import IntentClassifier
import csv
import statistics

classifier = IntentClassifier()

test_cases = [
    ("Hey! Could you explain what recursion is in simple words?", "TASK"),
    ("Thanks buddy, now show me a Java implementation of BFS.", "TASK"),
    ("Bye... actually wait, explain binary trees first.", "TASK"),
    ("Yo bro, are you still online?", "META"),
    ("Good evening! Can you generate an SQL query to join two tables?", "TASK"),
    ("thx 😊", "THANKS"),
    ("See ya later!", "GOODBYE"),
    ("Cool, got it.", "ACKNOWLEDGMENT"),
    ("Hello there 👋", "GREETING"),
    ("Can u explain OOP in Python?", "TASK"),
    ("hiiiii", "GREETING"),
    ("Yo!! Explain transformers like I'm five.", "TASK"),
    ("Is anyone listening?", "META"),
    ("Much appreciated, that's exactly what I needed.", "THANKS"),
    ("Alright then.", "ACKNOWLEDGMENT"),
    ("Need a C++ program for Dijkstra's algorithm.", "TASK"),
    ("Bro can u help me understand pointers?", "TASK"),
    ("Namaste! How's it going?", "GREETING"),
    ("Still awake?", "META"),
    ("Thanks! You're amazing.", "THANKS"),
    ("Catch you tomorrow.", "GOODBYE"),
    ("Makes perfect sense now.", "ACKNOWLEDGMENT"),
    ("Explain JWT authentication with an example.", "TASK"),
    ("Write regex to validate an email address.", "TASK"),
    ("Can you hear me now?", "META"),
    ("Good night, talk tomorrow.", "GOODBYE"),
    ("👍", "ACKNOWLEDGMENT"),
    ("🙏 Thanks a million!", "THANKS"),
    ("Hello! Are you free?", "META"),
    ("Hey! Thanks for helping yesterday. I need help with CNNs today.", "TASK"),
    ("Okay cool, explain REST API next.", "TASK"),
    ("Fine, I understand.", "ACKNOWLEDGMENT"),
    ("bye bye 👋", "GOODBYE"),
    ("Kem cho?", "GREETING"),
    ("Pls explain difference between stack and queue.", "TASK"),
    ("Can u generate a login page using React?", "TASK"),
    ("Hello... anyone here??", "META"),
    ("tysm ❤️", "THANKS"),
    ("Roger that!", "ACKNOWLEDGMENT"),
    ("Morning!", "GREETING"),
    ("Before I leave, explain what RAG is.", "TASK"),
    ("Ping...", "META"),
    ("Can you optimize this Python code for speed?", "TASK"),
    ("Alright bro 👍", "ACKNOWLEDGMENT"),
    ("Have a wonderful evening!", "GOODBYE"),
    ("Appreciate your support 🙏", "THANKS"),
    ("Sup?", "GREETING"),
    ("Explain why TinyBERT is suitable for CPU inference.", "TASK"),
    ("Hello 😊 Thanks! Now explain prompt engineering in detail.", "TASK"),
    ("Wait... are you still responding?", "META"),
    ("Hey!! Explain memoization with a simple Python example.", "TASK"),
    ("Thanks! Now show me BFS implementation in C++.", "TASK"),
    ("Bye... wait, explain polymorphism first.", "TASK"),
    ("Hey, are you available right now?", "META"),
    ("Good morning! Can you write an SQL query to find the second highest salary?", "TASK"),
    ("thnx 😊", "THANKS"),
    ("See you soon!", "GOODBYE"),
    ("Okay, understood.", "ACKNOWLEDGMENT"),
    ("Hello buddy 👋", "GREETING"),
    ("Can you explain multithreading in Java?", "TASK"),
    ("heyyyy", "GREETING"),
    ("Bro! Explain CNNs in simple language.", "TASK"),
    ("Anybody there?", "META"),
    ("Thanks a lot for explaining that.", "THANKS"),
    ("Alright, got your point.", "ACKNOWLEDGMENT"),
    ("Need a Python program for topological sorting.", "TASK"),
    ("Can u explain linked lists?", "TASK"),
    ("Good evening 😊", "GREETING"),
    ("Still there bro?", "META"),
    ("Thank you so much!", "THANKS"),
    ("Catch you later 👋", "GOODBYE"),
    ("Makes sense, thanks.", "ACKNOWLEDGMENT"),
    ("Explain OAuth 2.0 with an example.", "TASK"),
    ("Generate regex for validating phone numbers.", "TASK"),
    ("Can you see my message?", "META"),
    ("Goodbye! Have a nice day.", "GOODBYE"),
    ("👌", "ACKNOWLEDGMENT"),
    ("🙏 Really appreciate it!", "THANKS"),
    ("Hi! Are you online?", "META"),
    ("Hello! I need help understanding transformers.", "TASK"),
    ("Okay then, explain Kubernetes.", "TASK"),
    ("Yes, I understand now.", "ACKNOWLEDGMENT"),
    ("bye 👋", "GOODBYE"),
    ("Hello!!", "GREETING"),
    ("Explain stack vs heap memory.", "TASK"),
    ("Write a React component for user login.", "TASK"),
    ("Hello... anyone available?", "META"),
    ("Thanks ❤️", "THANKS"),
    ("Exactly!", "ACKNOWLEDGMENT"),
    ("Hi there!", "GREETING"),
    ("Explain microservices architecture.", "TASK"),
    ("Ping!", "META"),
    ("Optimize this Java code for performance.", "TASK"),
    ("Perfect 👍", "ACKNOWLEDGMENT"),
    ("Have a great day!", "GOODBYE"),
    ("Many thanks 🙏", "THANKS"),
    ("Yo!", "GREETING"),
    ("Explain the difference between REST and GraphQL.", "TASK"),
    ("Hi 😊 Thanks! Can you explain reinforcement learning?", "TASK"),
    ("Are you still here?", "META"),
    ("Hey!! Before we start, explain dependency injection in Spring Boot.", "TASK"),
    ("Yo, u still there or what?", "META"),
    ("Thanks mate 🙌", "THANKS"),
    ("Yep, that's crystal clear.", "ACKNOWLEDGMENT"),
    ("Later bro 👋", "GOODBYE"),
    ("Good morning! Can you explain deadlock with a real example?", "TASK"),
    ("heyyyyyyy 😄", "GREETING"),
    ("Anybody online??", "META"),
    ("Really appreciate your help ❤️", "THANKS"),
    ("Okay, let's continue.", "ACKNOWLEDGMENT"),
    ("Write a Python program to detect cycles in a graph.", "TASK"),
    ("Hola 👋", "GREETING"),
    ("Take care, see ya!", "GOODBYE"),
    ("Need help understanding AVL trees.", "TASK"),
    ("thxxxx 😊", "THANKS"),
    ("Gotcha 👍", "ACKNOWLEDGMENT"),
    ("Can anyone hear me over here?", "META"),
    ("Explain CAP theorem in distributed systems.", "TASK"),
    ("Ram Ram 🙏", "GREETING"),
    ("Logging off now, bye!", "GOODBYE"),
    ("Thank you so much, you're awesome!", "THANKS"),
    ("Everything makes sense now.", "ACKNOWLEDGMENT"),
    ("Generate a responsive dashboard using Tailwind CSS.", "TASK"),
    ("Still connected??", "META"),
    ("Yo wassup!", "GREETING"),
    ("Write a C++ implementation of Prim's Algorithm.", "TASK"),
    ("Cheers! Thanks again.", "THANKS"),
    ("Roger, moving on.", "ACKNOWLEDGMENT"),
    ("See you around!", "GOODBYE"),
    ("Explain how Redis caching works.", "TASK"),
    ("Hellooo buddy!", "GREETING"),
    ("Server alive?", "META"),
    ("ty buddy ❤️", "THANKS"),
    ("Makes total sense.", "ACKNOWLEDGMENT"),
    ("Explain virtual memory in operating systems.", "TASK"),
    ("Good to see you again!", "GREETING"),
    ("Bye! Have a safe trip.", "GOODBYE"),
    ("Design a normalized database schema for an online store.", "TASK"),
    ("Much obliged 🙏", "THANKS"),
    ("Understood completely.", "ACKNOWLEDGMENT"),
    ("Echo... anybody there?", "META"),
    ("Explain optimistic vs pessimistic locking.", "TASK"),
    ("Sup bro 😎", "GREETING"),
    ("I'm leaving, catch you later.", "GOODBYE"),
    ("Thanks for clearing my doubts!", "THANKS"),
    ("Perfect, I got the idea.", "ACKNOWLEDGMENT"),
    ("Can you implement Merge Sort in Java?", "TASK"),
    ("Hello... is this thing working?", "META"),
    ("Good afternoon 😊", "GREETING"),
    ("Before we end, explain message queues like RabbitMQ.", "TASK"),
    ("Hey bro 😄 before anything else explain heaps.", "TASK"),
    ("thx... btw explain gradient descent.", "TASK"),
    ("Bye for now, but first tell me what Docker Compose is.", "TASK"),
    ("yoooo 👋", "GREETING"),
    ("u alive?", "META"),
    ("tysm bro ❤️", "THANKS"),
    ("Aight 👍", "ACKNOWLEDGMENT"),
    ("I'm out, cya!", "GOODBYE"),
    ("Could you explain Bloom Filters with examples?", "TASK"),
    ("Kem cho dost?", "GREETING"),
    ("Still responding or crashed?", "META"),
    ("Appreciate it man 🙏", "THANKS"),
    ("Yep, everything's clear.", "ACKNOWLEDGMENT"),
    ("See ya next time!", "GOODBYE"),
    ("Write a Java program to implement Kruskal's algorithm.", "TASK"),
    ("Hellooooooo", "GREETING"),
    ("Can anyone read this message?", "META"),
    ("Thanks again for the detailed explanation!", "THANKS"),
    ("Roger 👍 understood.", "ACKNOWLEDGMENT"),
    ("Before leaving, explain indexing in databases.", "TASK"),
    ("Morning bro!", "GREETING"),
    ("Logging off 👋", "GOODBYE"),
    ("Could you build a REST API using Node.js and Express?", "TASK"),
    ("Yo... are you listening??", "META"),
    ("Many many thanks 😊", "THANKS"),
    ("Exactly what I was looking for.", "ACKNOWLEDGMENT"),
    ("Explain producer-consumer synchronization.", "TASK"),
    ("Namaskar 🙏", "GREETING"),
    ("Still online mate?", "META"),
    ("thnqqqq ❤️", "THANKS"),
    ("Makes total sense now 👍", "ACKNOWLEDGMENT"),
    ("Goodbye, have a productive day!", "GOODBYE"),
    ("Generate a binary search tree implementation in C.", "TASK"),
    ("Sup dude?", "GREETING"),
    ("Echo... anyone responding??", "META"),
    ("Really grateful for your help!", "THANKS"),
    ("Yep, moving ahead.", "ACKNOWLEDGMENT"),
    ("Explain CAP theorem with practical examples.", "TASK"),
    ("Heya 👋", "GREETING"),
    ("Can you hear this ping?", "META"),
    ("Thanks boss 😄", "THANKS"),
    ("Fair enough.", "ACKNOWLEDGMENT"),
    ("Catch you later bro!", "GOODBYE"),
    ("Explain why B-Trees are used in databases.", "TASK"),
    ("Good afternoon everyone!", "GREETING"),
    ("Write a responsive navbar using Bootstrap.", "TASK"),
    ("Still waiting...", "META"),
    ("ty ❤️ appreciate it", "THANKS"),
    ("Perfect explanation 👍", "ACKNOWLEDGMENT"),
    ("Before I go, explain Kafka message brokers.", "TASK"),
    ("Hey... before anything else, explain thread synchronization.", "TASK"),
    ("Thanks! One last thing—how does memoization work?", "TASK"),
    ("Bye... actually can you explain binary heaps first?", "TASK"),
    ("Helloooo 👋", "GREETING"),
    ("Are you actually responding?", "META"),
    ("Thanks a bunch 😊", "THANKS"),
    ("Understood perfectly.", "ACKNOWLEDGMENT"),
    ("See you next time!", "GOODBYE"),
    ("Explain how hash tables handle collisions.", "TASK"),
    ("Good morning everyone!", "GREETING"),
    ("Can you still read my messages?", "META"),
    ("Really appreciate your help!", "THANKS"),
    ("Everything's clear now.", "ACKNOWLEDGMENT"),
    ("Take care, bye!", "GOODBYE"),
    ("Generate a Python implementation of A* Search.", "TASK"),
    ("Hi there 😄", "GREETING"),
    ("Just checking if you're online.", "META"),
    ("Thank you for explaining that so well.", "THANKS"),
    ("That answers my question.", "ACKNOWLEDGMENT"),
    ("Explain optimistic concurrency control.", "TASK"),
    ("Hey friend!", "GREETING"),
    ("Still connected?", "META"),
    ("Much appreciated!", "THANKS"),
    ("Exactly what I needed.", "ACKNOWLEDGMENT"),
    ("Goodbye and have a wonderful day.", "GOODBYE"),
    ("Can you explain ACID properties with examples?", "TASK"),
    ("Morning! 👋", "GREETING"),
    ("Is this conversation still active?", "META"),
    ("Thanks for your patience.", "THANKS"),
    ("Crystal clear explanation.", "ACKNOWLEDGMENT"),
    ("Explain the Observer Design Pattern.", "TASK"),
    ("Hello there!", "GREETING"),
    ("Can you receive this message?", "META"),
    ("Thanks again for all the help.", "THANKS"),
    ("I completely understand now.", "ACKNOWLEDGMENT"),
    ("See you around!", "GOODBYE"),
    ("Write a Java program for Huffman Coding.", "TASK"),
    ("Hey buddy!", "GREETING"),
    ("Anyone there?", "META"),
    ("I appreciate your assistance.", "THANKS"),
    ("Makes complete sense.", "ACKNOWLEDGMENT"),
    ("Before we finish, explain Apache Spark.", "TASK"),
    ("Greetings!", "GREETING"),
    ("Just making sure you're still available.", "META"),
    ("Thanks, that solved my confusion.", "THANKS"),
    ("Perfect, let's continue.", "ACKNOWLEDGMENT"),
    ("Goodbye for now.", "GOODBYE"),
    ("Explain consistent hashing in distributed systems.", "TASK"),
    ("Hello 😊 Before we start, explain reinforcement learning.", "TASK"),
        ("Alright, sounds good.", "ACKNOWLEDGMENT"),
    ("Yep, continue please.", "ACKNOWLEDGMENT"),
    ("Okay then 👍", "ACKNOWLEDGMENT"),
    ("Looks good to me.", "ACKNOWLEDGMENT"),
    ("That makes sense.", "ACKNOWLEDGMENT"),
    ("Understood, go ahead.", "ACKNOWLEDGMENT"),
    ("Awesome, continue.", "ACKNOWLEDGMENT"),
    ("Works for me.", "ACKNOWLEDGMENT"),
    ("Exactly, that's what I meant.", "ACKNOWLEDGMENT"),
    ("Perfect, carry on.", "ACKNOWLEDGMENT"),

    ("Thanks, now explain binary search trees.", "TASK"),
    ("Goodbye... actually tell me about Docker first.", "TASK"),
    ("Hi there! Can you explain Kubernetes networking?", "TASK"),
    ("Morning! I need help with JWT authentication.", "TASK"),
    ("Hey 😊 explain reinforcement learning.", "TASK"),
    ("Before I leave, explain database indexing.", "TASK"),
    ("Thanks again! One last question about Redis.", "TASK"),
    ("Can you quickly explain mutex vs semaphore?", "TASK"),
    ("Hello! Show me a Python implementation of DFS.", "TASK"),
    ("Bye... before that explain heaps.", "TASK"),

    ("Still with me?", "META"),
    ("Can you read this?", "META"),
    ("Everything working?", "META"),
    ("Am I connected?", "META"),
    ("Is the chat alive?", "META"),
    ("Can you still see my messages?", "META"),
    ("Testing... are you responding?", "META"),
    ("Anyone on the other side?", "META"),
    ("You there?", "META"),
    ("Still available?", "META"),

    ("Thanks a ton!", "THANKS"),
    ("Really appreciate everything.", "THANKS"),
    ("You're a lifesaver.", "THANKS"),
    ("Couldn't have done it without you.", "THANKS"),
    ("Many thanks!", "THANKS"),
    ("Thanks again 😊", "THANKS"),
    ("Huge thanks!", "THANKS"),
    ("That helped a lot, thanks.", "THANKS"),

    ("See you!", "GOODBYE"),
    ("I'm heading out now.", "GOODBYE"),
    ("Take it easy!", "GOODBYE"),
    ("Talk later!", "GOODBYE"),
    ("Until next time!", "GOODBYE"),
    ("Have a nice one!", "GOODBYE"),
    ("Signing off.", "GOODBYE"),
    ("See you tomorrow.", "GOODBYE"),

    ("Good evening!", "GREETING"),
    ("Hello my friend!", "GREETING"),
    ("Hey there!", "GREETING"),
    ("Nice to see you!", "GREETING"),
    ("Hope you're doing well!", "GREETING"),
    ("Howdy!", "GREETING"),
    ("Greetings, assistant!", "GREETING"),
    ("Hi again 👋", "GREETING"),
    ("Welcome back!", "GREETING"),
    ("Hey, good to see you!", "GREETING"),
    ("Good afternoon!", "GREETING")
]

labels = [
    "TASK",
    "GREETING",
    "THANKS",
    "GOODBYE",
    "ACKNOWLEDGMENT",
    "META",
]

y_true = []
y_pred = []
correct = 0
results = []
failed_confidences = []

for i, (text, expected) in enumerate(test_cases, 1):
    result = classifier.predict(text)
    intent = result["intent"]
    confidence = result["confidence"]

    y_true.append(expected)
    y_pred.append(intent)

    passed = intent == expected
    results.append({
        "Input": text,
        "Expected": expected,
        "Predicted": intent,
        "Confidence": confidence,
        "Result": "PASS" if passed else "FAIL"
    })

    if not passed:
        failed_confidences.append(confidence)

    if passed:
        correct += 1

    print("-" * 70)
    print(f"Test       : {i}/{len(test_cases)}")
    print(f"Input      : {text}")
    print(f"Expected   : {expected}")
    print(f"Predicted  : {intent}")
    print(f"Confidence : {confidence:.4f}")
    print(f"Result     : {'PASS' if intent == expected else 'FAIL'}")

# Save CSV
with open("classifier_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Input",
            "Expected",
            "Predicted",
            "Confidence",
            "Result"
        ]
    )
    writer.writeheader()
    writer.writerows(results)
print("\nResults saved to classifier_results.csv")

accuracy = correct / len(test_cases) * 100
print(f"\n\n\nOverall Accuracy : {correct}/{len(test_cases)} ({accuracy:.2f}%)\n\n")

cm = confusion_matrix(y_true, y_pred, labels=labels)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

disp.plot(cmap="Blues", values_format="d")
plt.title("Intent Classifier - Confusion Matrix")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\nClassification Report\n")
print(classification_report(y_true, y_pred, labels=labels, digits=4))

if failed_confidences:
    avg_conf = sum(failed_confidences) / len(failed_confidences)
    print("\n========== Failed Prediction Statistics ==========")
    print(f"Failed Samples           : {len(failed_confidences)}")
    print(f"Average Confidence       : {avg_conf:.4f}")
    print(f"Median Confidence        : {statistics.median(failed_confidences):.4f}")
    print(f"Minimum Confidence       : {min(failed_confidences):.4f}")
    print(f"Maximum Confidence       : {max(failed_confidences):.4f}")

else:
    print("\nNo failed predictions found.")