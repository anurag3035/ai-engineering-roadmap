from fastapi import FastAPI
from schemas import Student

app = FastAPI()

students = []


@app.get("/")
def home():
    return {
        "message": "Student API"
    }


@app.post("/students")
def create_student(student: Student):
    students.append(student)

    return {
        "message": "Student added successfully",
        "student": student
    }


@app.get("/students")
def get_students():
    return students