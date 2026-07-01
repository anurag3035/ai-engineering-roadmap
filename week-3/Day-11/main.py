from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to my first FastAPI application!"
    }


@app.get("/about")
def about():
    return {
        "name": "Anurag",
        "internship": "AI Engineering Roadmap",
        "day": 11
    }


@app.get("/hello/{name}")
def say_hello(name: str):
    return {
        "message": f"Hello {name}"
    }


@app.get("/square/{number}")
def find_square(number: int):
    return {
        "number": number,
        "square": number * number
    }


@app.get("/add")
def add_numbers(a: int, b: int):
    return {
        "first_number": a,
        "second_number": b,
        "sum": a + b
    }