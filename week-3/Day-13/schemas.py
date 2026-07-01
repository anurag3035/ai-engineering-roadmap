from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str


class StudentCreate(BaseModel):
    name: str
    age: int
    course: str