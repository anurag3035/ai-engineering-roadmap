from embedding_service import EmbeddingService
from dense_retriever import DenseRetriever
from bm25_retriever import BM25Retriever
from hybrid_retriever import HybridRetriever
from models import Document


embedder = EmbeddingService()

dense = DenseRetriever()

dense.clear()

documents = [

    Document(
        id="1",
        content="Artificial Intelligence is transforming education.",
        metadata={"type": "article"}
    ),

    Document(
        id="2",
        content="Python is a popular programming language.",
        metadata={"type": "tutorial"}
    ),

    Document(
        id="3",
        content="Machine learning is a subset of Artificial Intelligence.",
        metadata={"type": "article"}
    )

]

for document in documents:
    document.embedding = embedder.embed(document.content)

dense.add_documents(documents)

bm25 = BM25Retriever()
bm25.add_documents(documents)

hybrid = HybridRetriever(
    dense,
    bm25
)

query = "Artificial Intelligence in education"

results = hybrid.search(
    query=query,
    query_embedding=embedder.embed(query),
    top_k=2
)

print("\nHybrid Search Results\n")

for document in results:

    print(f"ID: {document.id}")
    print(f"Content: {document.content}")
    print("-" * 40)