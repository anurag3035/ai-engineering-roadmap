from fastapi import FastAPI, HTTPException
from auth import hash_password, verify_password, create_access_token
from schemas import UserRegister, UserLogin

app = FastAPI()

users = {}


@app.get("/")
def home():
    return {"message": "Day 16 - Authentication API"}


# Register User
@app.post("/register")
def register(user: UserRegister):

    if user.username in users:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    users[user.username] = hash_password(user.password)

    return {
        "message": "Registration Successful"
    }


# Login User
@app.post("/login")
def login(user: UserLogin):

    if user.username not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    hashed_password = users[user.username]

    if not verify_password(
        user.password,
        hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Wrong Password"
        )

    token = create_access_token(
        {
            "username": user.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }