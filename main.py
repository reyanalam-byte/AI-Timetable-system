from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scheduler import assign_replacement

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
def home():

    return {
        "message": "Backend Running"
    }

# Teacher Absent Route
@app.post("/teacher/absent/{teacher_name}")
def mark_absent(teacher_name: str):

    replacements = assign_replacement(teacher_name)

    return {
        "absentTeacher": teacher_name,
        "totalReplacements": len(replacements),
        "replacements": replacements
    }