from embedding_service import EmbeddingService
from dense_retriever import DenseRetriever
from models import Document

embedder = EmbeddingService()

retriever = DenseRetriever()

retriever.clear()

document = Document(
    id="doc1",
    content="Artificial Intelligence is transforming education.",
    embedding=embedder.embed(
        "Artificial Intelligence is transforming education."
    ),
    metadata={
        "type": "article"
    }
)

retriever.add_documents([document])

results = retriever.search(
    embedder.embed("AI in education"),
    top_k=1
)

print(results[0].content)