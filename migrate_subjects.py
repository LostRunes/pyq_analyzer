import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# =========================================
# YOUR MASTER DATABASE
# =========================================

YOUR_SUPABASE_URL = os.getenv("YOUR_SUPABASE_URL")
YOUR_SUPABASE_KEY = os.getenv("YOUR_SUPABASE_KEY")

your_db = create_client(
    YOUR_SUPABASE_URL,
    YOUR_SUPABASE_KEY
)

# =========================================
# STUDENT DATABASE
# =========================================

STUDENT_SUPABASE_URL = os.getenv("STUDENT_SUPABASE_URL")
STUDENT_SUPABASE_KEY = os.getenv("STUDENT_SUPABASE_KEY")

student_db = create_client(
    STUDENT_SUPABASE_URL,
    STUDENT_SUPABASE_KEY
)

# =========================================
# CONFIG
# =========================================

SUBJECT_CODES = [
    "CS30011", 
    "CS21002"
    
]

# =========================================
# ALIASES
# =========================================

BRANCH_ALIASES = {

    # ECS variations
    "ecsc": "ecs",
    "electronics and computer science": "ecs",
    "electronics & computer science": "ecs",

    # CSE variations
    "computer science": "cse",
    "computer science engineering": "cse",
}

YEAR_ALIASES = {

    # 1st year
    "1": "1st year",
    "1st": "1st year",
    "first": "1st year",

    # 2nd year
    "2": "2nd year",
    "2nd": "2nd year",
    "second": "2nd year",

    # 3rd year
    "3": "3rd year",
    "3rd": "3rd year",
    "third": "3rd year",

    # 4th year
    "4": "4th year",
    "4th": "4th year",
    "fourth": "4th year",
}

# =========================================
# HELPERS
# =========================================

def normalize(text):
    return text.strip().lower()

def fetch_table(table_name, filters=None):

    query = student_db.table(table_name).select("*")

    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)

    response = query.execute()

    return response.data

def upsert_data(table_name, data):

    if not data:
        print(f"No data for {table_name}")
        return

    your_db.table(table_name).upsert(data).execute()

    print(f"Inserted/Updated {len(data)} rows into {table_name}")

# =========================================
# FETCH BRANCHES + YEARS
# =========================================

student_branches = fetch_table("branches")

your_branches = (
    your_db
    .table("branches")
    .select("*")
    .execute()
    .data
)

student_years = fetch_table("years")

your_years = (
    your_db
    .table("years")
    .select("*")
    .execute()
    .data
)

# =========================================
# BUILD BRANCH MAP
# =========================================

BRANCH_MAP = {}

for sb in student_branches:

    student_name = normalize(sb["name"])

    student_name = BRANCH_ALIASES.get(
        student_name,
        student_name
    )

    for yb in your_branches:

        your_name = normalize(yb["name"])

        your_name = BRANCH_ALIASES.get(
            your_name,
            your_name
        )

        if student_name == your_name:

            BRANCH_MAP[sb["id"]] = yb["id"]

print("\n===================================")
print("BRANCH MAP")
print("===================================")

for k, v in BRANCH_MAP.items():
    print(f"{k} -> {v}")

# =========================================
# BUILD YEAR MAP
# =========================================

YEAR_MAP = {}

for sy in student_years:

    student_name = normalize(sy["name"])

    student_name = YEAR_ALIASES.get(
        student_name,
        student_name
    )

    for yy in your_years:

        your_name = normalize(yy["name"])

        your_name = YEAR_ALIASES.get(
            your_name,
            your_name
        )

        if student_name == your_name:

            YEAR_MAP[sy["id"]] = yy["id"]

print("\n===================================")
print("YEAR MAP")
print("===================================")

for k, v in YEAR_MAP.items():
    print(f"{k} -> {v}")

# =========================================
# FETCH SUBJECTS
# =========================================

subjects = []

for code in SUBJECT_CODES:

    result = fetch_table(
        "subjects",
        {"code": code}
    )

    if not result:
        print(f"Subject {code} not found")
        continue

    subjects.extend(result)

if not subjects:
    print("No subjects found.")
    exit()

subject_ids = [s["id"] for s in subjects]

print("\n===================================")
print("SUBJECTS FOUND")
print("===================================")

for s in subjects:
    print(f"{s['name']} ({s['code']})")

# =========================================
# INSERT SUBJECTS
# =========================================

upsert_data("subjects", subjects)

# =========================================
# FETCH TOPICS
# =========================================

topics = []

for subject_id in subject_ids:

    topics.extend(
        fetch_table(
            "topics",
            {"subject_id": subject_id}
        )
    )

topic_ids = [t["id"] for t in topics]

upsert_data("topics", topics)

# =========================================
# FETCH PYQ SOURCES
# =========================================

pyq_sources = []

for subject_id in subject_ids:

    pyq_sources.extend(
        fetch_table(
            "pyq_sources",
            {"subject_id": subject_id}
        )
    )

pyq_source_ids = [p["id"] for p in pyq_sources]

upsert_data("pyq_sources", pyq_sources)

# =========================================
# FETCH QUESTION_TOPICS
# =========================================

question_topics = []

for topic_id in topic_ids:

    question_topics.extend(
        fetch_table(
            "question_topics",
            {"topic_id": topic_id}
        )
    )

question_ids = list(set([
    qt["question_id"]
    for qt in question_topics
]))

# =========================================
# FETCH QUESTIONS
# =========================================

questions = []

for question_id in question_ids:

    result = fetch_table(
        "questions",
        {"id": question_id}
    )

    if result:
        questions.extend(result)

upsert_data("questions", questions)

# =========================================
# INSERT QUESTION_TOPICS
# =========================================

upsert_data(
    "question_topics",
    question_topics
)

# =========================================
# FETCH QUESTION_PYQ_MAP
# =========================================

question_pyq_map = []

for pyq_id in pyq_source_ids:

    question_pyq_map.extend(
        fetch_table(
            "question_pyq_map",
            {"pyq_source_id": pyq_id}
        )
    )
# =========================================
# ENSURE ALL QUESTIONS EXIST
# =========================================

# extra_question_ids = list(set([
#     qpm["question_id"]
#     for qpm in question_pyq_map
# ]))

# existing_question_ids = set([
#     q["id"]
#     for q in questions
# ])

# missing_question_ids = [
#     qid
#     for qid in extra_question_ids
#     if qid not in existing_question_ids
# ]

# print("\nMissing Questions:", len(missing_question_ids))

# extra_questions = []

# for question_id in missing_question_ids:

#     result = fetch_table(
#         "questions",
#         {"id": question_id}
#     )

#     if result:
#         extra_questions.extend(result)

# if extra_questions:

#     questions.extend(extra_questions)

#     upsert_data(
#         "questions",
#         extra_questions
#     )
upsert_data(
    "question_pyq_map",
    question_pyq_map
)

# =========================================
# FETCH IMAGES
# =========================================

images = []

for question_id in question_ids:

    images.extend(
        fetch_table(
            "images",
            {"question_id": question_id}
        )
    )

upsert_data("images", images)

# =========================================
# FETCH BRANCH_SUBJECTS
# =========================================

branch_subjects = []

for subject_id in subject_ids:

    branch_subjects.extend(
        fetch_table(
            "branch_subjects",
            {"subject_id": subject_id}
        )
    )

# =========================================
# REMAP BRANCH + YEAR IDS
# =========================================

for row in branch_subjects:

    old_branch_id = row["branch_id"]
    old_year_id = row["year_id"]

    # =====================
    # BRANCH REMAP
    # =====================

    if old_branch_id in BRANCH_MAP:

        row["branch_id"] = BRANCH_MAP[
            old_branch_id
        ]

    else:

        print(
            f"WARNING: Missing branch mapping for "
            f"{old_branch_id}"
        )

    # =====================
    # YEAR REMAP
    # =====================

    if old_year_id in YEAR_MAP:

        row["year_id"] = YEAR_MAP[
            old_year_id
        ]

    else:

        print(
            f"WARNING: Missing year mapping for "
            f"{old_year_id}"
        )

# =========================================
# INSERT BRANCH_SUBJECTS
# =========================================

upsert_data(
    "branch_subjects",
    branch_subjects
)

# =========================================
# DONE
# =========================================

print("\n===================================")
print("MIGRATION COMPLETED SUCCESSFULLY")
print("===================================")