from config import RRF_K


class HybridRetriever:

    def __init__(
        self,
        dense_retriever,
        bm25_retriever
    ):

        self.dense_retriever = dense_retriever
        self.bm25_retriever = bm25_retriever

    def search(
        self,
        query,
        query_embedding,
        top_k=5
    ):

        dense_results = self.dense_retriever.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        bm25_results = self.bm25_retriever.search(
            query=query,
            top_k=top_k
        )

        scores = {}

        for rank, document in enumerate(dense_results):

            scores[document.id] = scores.get(
                document.id,
                0
            ) + 1 / (RRF_K + rank + 1)

        for rank, document in enumerate(bm25_results):

            scores[document.id] = scores.get(
                document.id,
                0
            ) + 1 / (RRF_K + rank + 1)

        merged_documents = {}

        for document in dense_results:
            merged_documents[document.id] = document

        for document in bm25_results:
            merged_documents[document.id] = document

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        results = []

        for document_id, _ in ranked[:top_k]:

            results.append(
                merged_documents[document_id]
            )

        return results