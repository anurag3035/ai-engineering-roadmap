from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue
)

from config import (
    QDRANT_PATH,
    COLLECTION_NAME
)

from models import Document


class QdrantVectorStore:

    def __init__(self):

        self.client = QdrantClient(
            path=QDRANT_PATH
        )

        collections = [
            collection.name
            for collection in self.client.get_collections().collections
        ]

        if COLLECTION_NAME not in collections:

            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=3072,
                    distance=Distance.COSINE
                )
            )
    def add_documents(
        self,
        documents
    ):

        points = []

        for document in documents:

            points.append(

                PointStruct(
                    id=document.id,
                    vector=document.embedding,
                    payload={
                        "content": document.content,
                        **document.metadata
                    }
                )

            )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        ) 
    def search(
        self,
        query_embedding,
        top_k=5,
        metadata_filter=None
    ):

        query_filter = None

        if metadata_filter:

            conditions = []

            for key, value in metadata_filter.items():

                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )

            query_filter = Filter(
                must=conditions
            )

        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=query_filter
        )

        documents = []

        for result in results:

            payload = result.payload

            documents.append(

                Document(
                    id=str(result.id),
                    content=payload["content"],
                    embedding=[],
                    metadata={
                        key: value
                        for key, value in payload.items()
                        if key != "content"
                    }
                )

            )

            return documents
    def delete_document(
        self,
        document_id
    ):

        self.client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=[
                document_id
            ]
        ) 
    def clear(self):

        collections = self.client.get_collections()

        if any(
            collection.name == COLLECTION_NAME
            for collection in collections.collections
        ):

            self.client.delete_collection(
                collection_name=COLLECTION_NAME
            )

            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=3072,
                    distance=Distance.COSINE
                )
            )  
                                            