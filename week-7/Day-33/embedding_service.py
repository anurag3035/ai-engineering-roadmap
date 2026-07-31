from google import genai

from config import GEMINI_API_KEY, MODEL_NAME


class EmbeddingService:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def embed(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model=MODEL_NAME,
            contents=text
        )

        return response.embeddings[0].values

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = []

        for text in texts:
            embeddings.append(self.embed(text))

        return embeddings