from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
import time

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Too many requests. Please try again later."}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_request_time(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()

    print(
        f"{request.method} {request.url.path} completed in "
        f"{end_time - start_time:.4f} seconds"
    )

    return response


@app.get("/")
@limiter.limit("5/minute")
async def home(request: Request):

    return {
        "message": "Welcome to Day 18 FastAPI Middleware Project"
    }


@app.get("/student")
@limiter.limit("3/minute")
async def student(request: Request):

    return {
        "name": "Anurag",
        "course": "AI Engineering"
    }