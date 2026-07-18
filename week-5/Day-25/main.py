import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from gemini_client import GeminiClient

app = FastAPI()

client = GeminiClient()


async def stream_generator(prompt):

    try:

        for chunk in client.stream(prompt):

            if chunk.text:

                data = {
                    "token": chunk.text
                }

                yield f"data: {json.dumps(data)}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:

        error = {
            "error": str(e)
        }

        yield f"data: {json.dumps(error)}\n\n"


@app.get("/stream")
async def stream(prompt: str):

    return StreamingResponse(
        stream_generator(prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )