import asyncio

from fastapi.responses import StreamingResponse

from app.gemini_client import GeminiClient


class StreamService:

    def __init__(self):

        self.client = GeminiClient()

    async def stream_generator(
        self,
        prompt: str
    ):

        response = self.client.generate(prompt)

        words = response.split()

        for word in words:

            yield word + " "

            await asyncio.sleep(0.05)

    def stream(
        self,
        prompt: str
    ):

        return StreamingResponse(
            self.stream_generator(prompt),
            media_type="text/plain"
        )