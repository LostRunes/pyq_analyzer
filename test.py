import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ================= CONFIG =================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUBJECT_ID = "607ad3fc-3336-4a4e-bd03-d313f84faa78"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"  
}

# ==========================================

def insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.post(url, headers=HEADERS, json=data)

    print(f"[{table}] Status:", res.status_code)

    if res.status_code not in (200, 201):
        print("ERROR:", res.text)
        exit()

    if not res.text:
        print("⚠️ Empty response (missing Prefer header?)")
        return None

    return res.json()

def select(table, query=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{query}"
    res = requests.get(url, headers=HEADERS)
    return res.json()

# ================= LOAD JSON =================
with open("pe10002_pyq_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

topics = data["topics"]
questions = data["questions"]

# ================= INSERT TOPICS =================
print("Inserting topics...")

topic_map = {}  # name → id

for t in topics:
    res = insert("topics", {
        "subject_id": SUBJECT_ID,
        "name": t["topic_name"],
        "summary": t["summary"]
    })
    topic_map[t["topic_name"]] = res[0]["id"]

print("Topics done")

# ================= INSERT QUESTIONS =================
print("Inserting questions...")

question_map = {}  # text → id

for q in questions:
    res = insert("questions", {
        "question_text": q["question_text"],
        "difficulty": q["difficulty"]
    })
    q_id = res[0]["id"]
    question_map[q["question_text"]] = q_id

    # ---- LINK QUESTION ↔ TOPICS ----
    for topic_name in q["topics"]:
        insert("question_topics", {
            "question_id": q_id,
            "topic_id": topic_map[topic_name]
        })

    # ---- PYQ SOURCES ----
    for src in q["pyq_sources"]:
        # check if already exists
        existing = select(
            "pyq_sources",
            f"year=eq.{src['year']}&exam_type=eq.{src['exam_type']}&season=eq.{src['season']}&question_number=eq.{src['question_number']}&subject_id=eq.{SUBJECT_ID}"
        )

        if existing:
            pyq_id = existing[0]["id"]
        else:
            res2 = insert("pyq_sources", {**src, "subject_id": SUBJECT_ID})
            pyq_id = res2[0]["id"]

        # map question ↔ pyq
        insert("question_pyq_map", {
            "question_id": q_id,
            "pyq_source_id": pyq_id
        })

print("Questions + mappings done")

print("ALL DATA INSERTED SUCCESSFULLY")