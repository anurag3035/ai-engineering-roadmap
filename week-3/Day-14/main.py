from fastapi import FastAPI, HTTPException
from schemas import Student

app = FastAPI()

students = []


@app.get("/")
def home():
    return {"message": "Student Management API"}


@app.get("/students")
def get_students():
    return students


@app.post("/students")
def add_student(student: Student):
    students.append(student)
    return {
        "message": "Student added successfully",
        "student": student
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student.id == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")


@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    for index, student in enumerate(students):

        if student.id == student_id:
            students[index] = updated_student
            return {
                "message": "Student updated successfully",
                "student": updated_student
            }

    raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:

        if student.id == student_id:
            students.remove(student)
            return {"message": "Student deleted successfully"}

    raise HTTPException(status_code=404, detail="Student not found")