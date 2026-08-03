from rank_bm25 import BM25Okapi

from models import Document


class BM25Retriever:

    def __init__(self):

        self.documents = []
        self.tokenized_documents = []
        self.bm25 = None

    def add_documents(self, documents):

        self.documents = documents
        self.tokenized_documents = []

        for document in documents:

            tokens = document.content.lower().split()
            self.tokenized_documents.append(tokens)

        self.bm25 = BM25Okapi(self.tokenized_documents)

    def search(self, query, top_k=5):

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            zip(scores, self.documents),
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        for _, document in ranked[:top_k]:
            results.append(document)

        return results