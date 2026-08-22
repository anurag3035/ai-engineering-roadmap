from embedding_service import EmbeddingService
from dense_retriever import DenseRetriever
from bm25_retriever import BM25Retriever
from hybrid_retriever import HybridRetriever
from rag_generator import RAGGenerator
from models import Document


documents = [

    Document(
        id="1",
        content="Employees receive 12 casual leaves every year.",
        metadata={
            "source": "HR Policy",
            "page": 5
        }
    ),

    Document(
        id="2",
        content="Work from home is allowed for two days every week.",
        metadata={
            "source": "HR Policy",
            "page": 8
        }
    ),

    Document(
        id="3",
        content="Python is used for AI application development.",
        metadata={
            "source": "Engineering Guide",
            "page": 2
        }
    )

]

embedder = EmbeddingService()

for document in documents:

    document.embedding = embedder.embed(
        document.content
    )

dense = DenseRetriever()

dense.clear()

dense.add_documents(
    documents
)

bm25 = BM25Retriever()

bm25.add_documents(
    documents
)

hybrid = HybridRetriever(
    dense,
    bm25
)

generator = RAGGenerator()

query = input("Ask your question : ")

results = hybrid.search(
    query=query,
    query_embedding=embedder.embed(query),
    top_k=3
)

answer = generator.generate(
    query=query,
    documents=results
)

print("\nAnswer\n")

print(answer)