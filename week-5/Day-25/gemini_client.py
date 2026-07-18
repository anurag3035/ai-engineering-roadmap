from google import genai

from config import GEMINI_API_KEY, MODEL_NAME


class GeminiClient:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def stream(self, prompt):

        return self.client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=prompt,
        )