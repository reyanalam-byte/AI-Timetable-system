from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scheduler import assign_replacement

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.post("/teacher/absent/{teacher_name}")
def teacher_absent(teacher_name: str):

    result = assign_replacement(teacher_name)

    return {
        "absentTeacher": teacher_name,
        "replacements": result
    }