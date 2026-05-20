from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scheduler import assign_replacement
from teacher_data import teachers, timetable
from ollama_ai import ask_ollama

app = FastAPI()

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# HOME ROUTE
# =========================================

@app.get("/")
def home():

    return {
        "message": "AI Timetable Backend Running"
    }

# =========================================
# API 1 -> ALL TEACHERS DATABASE
# =========================================

@app.get("/teachers")
def get_teachers():

    return {

        "totalTeachers": len(teachers),
        "teachers": teachers

    }

# =========================================
# API 2 -> GENERATIVE AI QUERY
# =========================================

@app.post("/ai-query")
def ai_query(data: dict):

    prompt = data["prompt"]

    improved_prompt = f"""
    You are an AI timetable assistant.

    Teachers:
    {teachers}

    Timetable:
    {timetable}

    USER QUESTION:
    {prompt}

    STRICT RULES:
    - Keep answer under 3 lines
    - Be direct
    - Professional tone only
    """

    response = ask_ollama(improved_prompt)

    return {

        "query": prompt,
        "aiResponse": response

    }

# =========================================
# API 3 -> SMART CHATBOT
# =========================================

@app.post("/chatbot")
def chatbot(data: dict):

    query = data["query"].lower()

    # =====================================
    # AVAILABLE TEACHERS
    # =====================================

    if "available at" in query:

        time = query.split("available at")[-1]

        time = (
            time.replace(".", "")
                .replace(" ", "")
                .upper()
        )

        available_teachers = []

        for teacher in teachers:

            if time in teacher["freeSlots"]:

                available_teachers.append(
                    teacher["name"]
                )

        if available_teachers:

            response = (
                f"Available teachers at {time}: "
                f"{', '.join(available_teachers)}"
            )

        else:

            response = f"No teachers available at {time}"

        return {

            "query": query,
            "response": response

        }

    # =====================================
    # LOWEST WORKLOAD
    # =====================================

    elif "lowest workload" in query:

        lowest = min(
            teachers,
            key=lambda x: x["currentLoad"]
        )

        return {

            "query": query,
            "response": (
                f"{lowest['name']} has the lowest workload "
                f"with load {lowest['currentLoad']}."
            )

        }

    # =====================================
    # OVERLOADED TEACHERS
    # =====================================

    elif "overloaded" in query:

        overloaded = []

        for teacher in teachers:

            if teacher["currentLoad"] >= teacher["maxLoad"]:

                overloaded.append(
                    teacher["name"]
                )

        if overloaded:

            response = (
                "Overloaded teachers: "
                + ", ".join(overloaded)
            )

        else:

            response = "No teachers are overloaded."

        return {

            "query": query,
            "response": response

        }

    # =====================================
    # REPLACEMENT QUERY
    # =====================================

    elif "replace" in query:

        for cls in timetable:

            absent_teacher = cls["teacher"].lower()

            if absent_teacher in query:

                replacements = assign_replacement(
                    cls["teacher"]
                )

                if replacements:

                    replacement_names = []

                    for r in replacements:

                        replacement_names.append(
                            r["replacementTeacher"]
                        )

                    return {

                        "query": query,
                        "response": (
                            "Possible replacements: "
                            + ", ".join(replacement_names)
                        )

                    }

        return {

            "query": query,
            "response": "No replacement teacher found."

        }

    # =====================================
    # AI FALLBACK
    # =====================================

    else:

        prompt = f"""
        You are an AI timetable assistant.

        Teachers:
        {teachers}

        Timetable:
        {timetable}

        USER QUESTION:
        {query}

        STRICT RULES:
        - Keep answer under 3 lines
        - Be direct
        - No fake forms
        - No greetings
        """

        response = ask_ollama(prompt)

        return {

            "query": query,
            "response": response

        }

# =========================================
# API 4 -> FULL AI TIMETABLE GENERATOR
# =========================================

@app.post("/generate-timetable")
def generate_timetable():

    sections = [
        {"section": "A", "class": 9},
        {"section": "B", "class": 8},
        {"section": "C", "class": 7},
        {"section": "D", "class": 10}
    ]

    periods = [
        "9AM",
        "10AM",
        "11AM",
        "1PM"
    ]

    subjects = [
        "Maths",
        "Science",
        "English"
    ]

    generated = []

    teacher_busy = {}

    for period in periods:

        teacher_busy[period] = []

        for sec in sections:

            assigned = False

            for subject in subjects:

                best_teacher = None

                for teacher in teachers:

                    if teacher["subject"] != subject:
                        continue

                    if period not in teacher["freeSlots"]:
                        continue

                    if teacher["currentLoad"] >= teacher["maxLoad"]:
                        continue

                    if teacher["name"] in teacher_busy[period]:
                        continue

                    best_teacher = teacher
                    break

                if best_teacher:

                    generated.append({

                        "section": sec["section"],
                        "class": sec["class"],
                        "subject": subject,
                        "teacher": best_teacher["name"],
                        "period": period

                    })

                    teacher_busy[period].append(
                        best_teacher["name"]
                    )

                    best_teacher["currentLoad"] += 1

                    assigned = True
                    break

            if not assigned:

                generated.append({

                    "section": sec["section"],
                    "class": sec["class"],
                    "subject": "Free Period",
                    "teacher": "No Teacher Available",
                    "period": period

                })

    ai_prompt = f"""
    Analyze this generated school timetable.

    Timetable:
    {generated}

    Give short professional insights about:
    - workload balancing
    - scheduling quality
    - teacher utilization

    Keep response under 4 lines.
    """

    ai_response = ask_ollama(ai_prompt)

    return {

        "generatedTimetable": generated,
        "aiInsights": ai_response

    }

# =========================================
# EXISTING AI REPLACEMENT SYSTEM
# =========================================

@app.post("/teacher/absent/{teacher_name}")
def mark_absent(teacher_name: str):

    replacements = assign_replacement(teacher_name)

    return {

        "absentTeacher": teacher_name,
        "totalReplacements": len(replacements),
        "replacements": replacements

    }