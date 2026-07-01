from fastapi import FastAPI, HTTPException
from schemas import Student, StudentCreate

app = FastAPI()

students = []


@app.get("/")
def home():
    return {
        "message": "Student CRUD API"
    }


@app.post("/students")
def create_student(student: StudentCreate):

    new_student = Student(
        id=len(students) + 1,
        name=student.name,
        age=student.age,
        course=student.course
    )

    students.append(new_student)

    return new_student


@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student.id == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: StudentCreate):

    for student in students:

        if student.id == student_id:

            student.name = updated_student.name
            student.age = updated_student.age
            student.course = updated_student.course

            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:

        if student.id == student_id:

            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )