from google import genai

from config import (
    GEMINI_API_KEY,
    MODEL_NAME
)


class EmbeddingService:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )
    def embed(
        self,
        text
    ):

        response = self.client.models.embed_content(
            model=MODEL_NAME,
            contents=text
        )

        return response.embeddings[0].values
    def embed_documents(
        self,
        documents
    ):

        embeddings = []

        for document in documents:

            embeddings.append(
                self.embed(
                    document.content
                )
            )

        return embeddings
                