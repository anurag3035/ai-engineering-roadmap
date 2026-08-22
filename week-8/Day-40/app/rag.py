from google import genai
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from app.config import GEMINI_API_KEY, MODEL_NAME, EMBEDDING_MODEL


class RAGService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.documents = []

        self.prompt = ChatPromptTemplate.from_template("""
You are a helpful RAG assistant.

Answer the question using only the context below.
If the context does not contain the answer, say:
"I could not find that information in the available documents."

Include citations in this format:
[Source: filename]

Context:
{context}

Question:
{question}

Answer:
""")

    def embed(self, text):
        response = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )
        return response.embeddings[0].values

    def add_documents(self, documents):
        for document in documents:
            if isinstance(document, Document):
                self.documents.append(document)
            else:
                self.documents.append(
                    Document(
                        page_content=document["content"],
                        metadata={"filename": document["filename"]}
                    )
                )

    def search(self, query, top_k=3):
        if not self.documents:
            return []

        query_vector = self.embed(query)
        scored = []

        for document in self.documents:
            vector = self.embed(document.page_content)

            dot = sum(a * b for a, b in zip(query_vector, vector))
            q_norm = sum(a * a for a in query_vector) ** 0.5
            d_norm = sum(a * a for a in vector) ** 0.5

            score = dot / (q_norm * d_norm) if q_norm and d_norm else 0
            scored.append((score, document))

        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[:top_k]

    def generate(self, query):
        results = self.search(query)

        if not results:
            return "I could not find that information in the available documents.", []

        context_parts = []
        sources = []

        for score, document in results:
            filename = document.metadata.get("filename", "unknown")
            context_parts.append(
                f"[Source: {filename}]\n{document.page_content}"
            )
            sources.append({
                "filename": filename,
                "score": round(score, 4)
            })

        context = "\n\n---\n\n".join(context_parts)
        prompt = self.prompt.format_messages(
            context=context,
            question=query
        )

        prompt_text = "\n".join(message.content for message in prompt)

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_text
        )

        return response.text, sources