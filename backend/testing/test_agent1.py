import sys,time,csv,re
sys.path.append(".")
from backend.agents.agent1_gemma import run_agent1

TEST_QUERIES = [
    {
        "id": 1,
        "category": "General",
        "input": "explain quantum physics simply",
        "expected": "RISE"
    },
    {
        "id": 2,
        "category": "General",
        "input": "what is blockchain not just crypto",
        "expected": "RISE"
    },
    {
        "id": 3,
        "category": "General",
        "input": "how does gps work technically",
        "expected": "RISE"
    },
    {
        "id": 4,
        "category": "Professional",
        "input": "write email boss asking for raise",
        "expected": "RISE"
    },
    {
        "id": 5,
        "category": "Professional",
        "input": "help me make resume for software job",
        "expected": "RISE"
    },
    {
        "id": 6,
        "category": "Professional",
        "input": "business proposal for mobile app startup",
        "expected": "RISE"
    },
    {
        "id": 7,
        "category": "Technical",
        "input": "python list comprehension not working",
        "expected": "RISE"
    },
    {
        "id": 8,
        "category": "Technical",
        "input": "difference between sql and nosql database",
        "expected": "RISE"
    },
    {
        "id": 9,
        "category": "Technical",
        "input": "explain neural networks for beginner",
        "expected": "RISE"
    },
    {
        "id": 10,
        "category": "Ethical",
        "input": "is it okay to steal food if family starving",
        "expected": "RISE"
    },
    {
        "id": 11,
        "category": "Ethical",
        "input": "should you report friend to police for crime",
        "expected": "RISE"
    },
    {
        "id": 12,
        "category": "Ethical",
        "input": "trolley problem what is right choice",
        "expected": "RISE"
    },
    {
        "id": 13,
        "category": "Critical Analysis",
        "input": "is social media more harm than good analyse",
        "expected": "RISE"
    },
    {
        "id": 14,
        "category": "Critical Analysis",
        "input": "capitalism good or bad critically",
        "expected": "RISE"
    },
    {
        "id": 15,
        "category": "Creative",
        "input": "short story about two strangers on train",
        "expected": "RISE"
    },
    {
        "id": 16,
        "category": "Creative",
        "input": "motivational quote about never giving up",
        "expected": "RISE"
    },
    {
        "id": 17,
        "category": "Maths",
        "input": "solve quadratic equation step by step",
        "expected": "RISE"
    },
    {
        "id": 18,
        "category": "Maths",
        "input": "plane 100 seats 1st guy lost ticket sits random. others take their seat if open else random what chance last guy gets his actual seat??",
        "expected": "RISE"
    },
    {
        "id": 19,
        "category": "Summarization",
        "input": "summarize long contract highlight important parts",
        "expected": "RISE"
    },
    {
        "id": 20,
        "category": "Summarization",
        "input": "research paper summary make it simple",
        "expected": "RISE"
    },
    {
        "id": 21,
        "category": "Greeting",
        "input": "Hello",
        "expected": "RAW"
    },
    {
        "id": 22,
        "category": "Greeting + Task",
        "input": "Hi, explain Linux in simple terms",
        "expected": "RISE"
    },
    {
        "id": 23,
        "category": "Messy Input",
        "input": "resume google software engineer",
        "expected": "RISE"
    },
    {
        "id": 24,
        "category": "Ambiguous Technical",
        "input": "python bug help",
        "expected": "RISE"
    },
    {
        "id": 25,
        "category": "Multi-Task",
        "input": "Explain Docker and compare it with Kubernetes",
        "expected": "RISE"
    }
]

LEAK_PATTERNS=["You are PromptFlow Agent 1","CRITICAL COMPLIANCE REQUIREMENT","OUTPUT REQUIREMENTS","RISE FORMAT"]

def validate(out,expected):
    wc=len(out.split())
    leak=any(x.lower() in out.lower() for x in LEAK_PATTERNS)
    code="```" in out
    if expected=="RAW":
        ok=not ("Role:" in out and "Instruction:" in out)
        return {"pass":ok,"wc":wc,"leak":leak,"role":False,"instruction":False,"expectation":False}
    role="Role:" in out
    inst="Instruction:" in out
    exp="Expectation:" in out
    steps=("Steps:" in out) or bool(re.search(r"\n1\.",out))
    ok=role and inst and exp and not leak and not code
    return {"pass":ok,"wc":wc,"leak":leak,"role":role,"instruction":inst,"expectation":exp,"steps":steps}

rows=[]
passed=0
times=[]
print("="*70)
print("PROMPTFLOW AGENT 1 VALIDATION")
print("="*70)
for t in TEST_QUERIES:
    st=time.time()
    try:
        out=run_agent1(t["input"])
    except Exception as e:
        out=f"ERROR: {e}"
    dt=time.time()-st
    times.append(dt)
    v=validate(out,t["expected"])
    passed+=1 if v["pass"] else 0
    print(f"\n[{t['id']:02}] {t['category']}")
    print("Input :",t["input"])
    print("Output:\n",out)
    print(f"Pass: {'YES' if v['pass'] else 'NO'} | Time: {dt:.2f}s | Words:{v['wc']} | Leak:{v['leak']}")
    rows.append([t["id"],t["category"],t["input"],t["expected"],v["pass"],dt,v["wc"],v["leak"],out])

with open("agent1_validation_report.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["ID","Category","Input","Expected","Pass","Latency","Words","Leak","Output"])
    w.writerows(rows)

print(f"Passed : {passed}/{len(TEST_QUERIES)}")
print(f"Success: {passed/len(TEST_QUERIES)*100:.2f}%")
print(f"Average Latency: {sum(times)/len(times):.2f}s")
print("CSV Report: agent1_validation_report.csv")