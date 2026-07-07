from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import aiofiles
import asyncio
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Day 17 - File Upload and Streaming"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    content = await file.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    return {
        "filename": file.filename,
        "size": len(content),
        "message": "Uploaded successfully"
    }


async def generate_tokens():

    tokens = [
        "Hello",
        "this",
        "is",
        "a",
        "streaming",
        "response",
        "from",
        "FastAPI"
    ]

    for token in tokens:
        yield f"data: {token}\n\n"
        await asyncio.sleep(1)

    yield "data: DONE\n\n"


@app.get("/stream")
async def stream():

    return StreamingResponse(
        generate_tokens(),
        media_type="text/event-stream"
    )