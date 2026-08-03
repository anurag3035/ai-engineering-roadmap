import chromadb

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    TOP_K
)

from models import Document


class DenseRetriever:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    def add_documents(
        self,
        documents
    ):

        for document in documents:

            self.collection.add(
                ids=[
                    document.id
                ],
                documents=[
                    document.content
                ],
                embeddings=[
                    document.embedding
                ],
                metadatas=[
                    document.metadata
                ]
            )

    def search(
        self,
        query_embedding,
        top_k=TOP_K
    ):

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k
        )

        documents = []

        ids = results["ids"][0]
        texts = results["documents"][0]
        metadata = results["metadatas"][0]

        for i in range(len(ids)):

            documents.append(

                Document(
                    id=ids[i],
                    content=texts[i],
                    metadata=metadata[i]
                )

            )

        return documents

    def clear(self):

        ids = self.collection.get()["ids"]

        if ids:

            self.collection.delete(ids=ids)