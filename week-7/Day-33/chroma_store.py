import chromadb

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME
)

from models import Document


class ChromaVectorStore:

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
        top_k=5,
        metadata_filter=None
    ):

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k,
            where=metadata_filter
        )

        documents = []

        for index in range(
            len(results["ids"][0])
        ):

            documents.append(

                Document(
                    id=results["ids"][0][index],
                    content=results["documents"][0][index],
                    embedding=[],
                    metadata=results["metadatas"][0][index]
                )

            )

        return documents 
    def delete_document(
        self,
        document_id
    ):

        self.collection.delete(
            ids=[
                document_id
            ]
        )
    def clear(self):

        ids = self.collection.get()["ids"]

        if ids:

            self.collection.delete(
                ids=ids
            ) 
                                  
