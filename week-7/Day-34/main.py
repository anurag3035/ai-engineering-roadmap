from embedding_service import EmbeddingService
from dense_retriever import DenseRetriever
from bm25_retriever import BM25Retriever
from hybrid_retriever import HybridRetriever
from models import Document


def print_results(title, results):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    for i, document in enumerate(results, start=1):

        print(f"{i}. {document.content}")
        print(f"   Metadata: {document.metadata}")
        print()


embedder = EmbeddingService()

dense = DenseRetriever()
dense.clear()

documents = [

    Document(
        id="1",
        content="Employees are entitled to 12 casual leaves every year.",
        metadata={
            "department": "HR"
        }
    ),

    Document(
        id="2",
        content="Python is widely used for Artificial Intelligence projects.",
        metadata={
            "department": "Engineering"
        }
    ),

    Document(
        id="3",
        content="Machine learning improves search quality in modern applications.",
        metadata={
            "department": "Engineering"
        }
    ),

    Document(
        id="4",
        content="Work from home is allowed for two days every week.",
        metadata={
            "department": "HR"
        }
    )

]

for document in documents:

    document.embedding = embedder.embed(
        document.content
    )

dense.add_documents(documents)

bm25 = BM25Retriever()
bm25.add_documents(documents)

hybrid = HybridRetriever(
    dense,
    bm25
)

query = "Artificial Intelligence search"

query_embedding = embedder.embed(query)

dense_results = dense.search(
    query_embedding=query_embedding,
    top_k=3
)

hybrid_results = hybrid.search(
    query=query,
    query_embedding=query_embedding,
    top_k=3
)

print_results(
    "Dense Retrieval Results",
    dense_results
)

print_results(
    "Hybrid Retrieval Results",
    hybrid_results
)