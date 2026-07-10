from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

students = [
    {
        "id": 1,
        "name": "Anurag",
        "course": "Chemical Engineering"
    },
    {
        "id": 2,
        "name": "Rahul",
        "course": "Computer Science"
    }
]


def verify_api_key(api_key: str):

    if api_key != "fastapi123":
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return api_key


@app.get("/")
def home():

    return {
        "message": "Day 20 - Dependency Injection"
    }


@app.get("/students")
def get_students(
    api_key: str = Depends(verify_api_key)
):

    return students


@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    api_key: str = Depends(verify_api_key)
):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )