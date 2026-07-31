from typing import Protocol

from models import Document


class VectorStore(Protocol):

    def add_documents(
        self,
        documents: list[Document]
    ) -> None:
        ...

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        metadata_filter: dict | None = None
    ) -> list[Document]:
        ...

    def delete_document(
        self,
        document_id: str
    ) -> None:
        ...