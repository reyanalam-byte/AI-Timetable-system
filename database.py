import json

TEACHERS_FILE = "data/teachers.json"
ASSIGNMENTS_FILE = "data/assignments.json"


def load_teachers():
    with open(TEACHERS_FILE, "r") as file:
        return json.load(file)


def load_assignments():
    with open(ASSIGNMENTS_FILE, "r") as file:
        return json.load(file)


def save_assignments(assignments):
    with open(ASSIGNMENTS_FILE, "w") as file:
        json.dump(assignments, file, indent=4)