from fastapi import FastAPI, HTTPException, Query
from typing import List

from schemas import Student, Message

app = FastAPI(
    title="Student Management API",
    description="A simple CRUD API built using FastAPI",
    version="1.0"
)

students: List[Student] = []


@app.get("/", response_model=Message)
def home():
    return {"message": "Welcome to Student Management API"}


@app.post("/students", response_model=Student)
def add_student(student: Student):

    for s in students:
        if s.id == student.id:
            raise HTTPException(
                status_code=400,
                detail="Student ID already exists"
            )

    students.append(student)
    return student


@app.get("/students", response_model=List[Student])
def get_students(course: str | None = Query(default=None)):

    if course:
        return [student for student in students if student.course.lower() == course.lower()]

    return students


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):

    for student in students:
        if student.id == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):

    for index, student in enumerate(students):

        if student.id == student_id:
            students[index] = updated_student
            return updated_student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


@app.delete("/students/{student_id}", response_model=Message)
def delete_student(student_id: int):

    for student in students:

        if student.id == student_id:
            students.remove(student)
            return {"message": "Student deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )