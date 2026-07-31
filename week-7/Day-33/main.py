from embedding_service import EmbeddingService
from chroma_store import ChromaVectorStore
from qdrant_store import QdrantVectorStore
from models import Document


embedder = EmbeddingService()

USE_CHROMA = True

if USE_CHROMA:
    store = ChromaVectorStore()
else:
    store = QdrantVectorStore()


documents = [
    {
        "id": "doc1",
        "content": "Employees are entitled to 12 casual leaves every year.",
        "metadata": {
            "doc_type": "policy",
            "department": "HR"
        }
    },
    {
        "id": "doc2",
        "content": "The engineering team follows Agile Scrum methodology.",
        "metadata": {
            "doc_type": "handbook",
            "department": "Engineering"
        }
    },
    {
        "id": "doc3",
        "content": "Work from home is allowed for two days each week.",
        "metadata": {
            "doc_type": "policy",
            "department": "HR"
        }
    }
]
vector_documents = []

for item in documents:

    embedding = embedder.embed(
        item["content"]
    )

    vector_documents.append(

        Document(
            id=item["id"],
            content=item["content"],
            embedding=embedding,
            metadata=item["metadata"]
        )

    )
print("=" * 60)
print("Adding documents...")
store.add_documents(vector_documents)
print("Documents added successfully.")
print("\n" + "=" * 60)
print("Semantic Search")

query = "How many casual leaves are allowed?"

query_embedding = embedder.embed(query)

results = store.search(
    query_embedding=query_embedding,
    top_k=2
)

for document in results:

    print("-" * 40)
    print("ID:", document.id)
    print("Content:", document.content)
    print("Metadata:", document.metadata)
print("\n" + "=" * 60)
print("Metadata Filter Search")

filtered_results = store.search(
    query_embedding=query_embedding,
    top_k=5,
    metadata_filter={
        "department": "HR"
    }
)

for document in filtered_results:

    print("-" * 40)
    print("ID:", document.id)
    print("Content:", document.content)
    print("Metadata:", document.metadata)
print("\n" + "=" * 60)
print("Deleting document: doc3")

store.delete_document("doc3")

print("Document deleted successfully.")
print("\n" + "=" * 60)
print("Searching Again After Delete")

results = store.search(
    query_embedding=query_embedding,
    top_k=5
)

for document in results:

    print("-" * 40)
    print("ID:", document.id)
    print("Content:", document.content)
print("\n" + "=" * 60)
print("Day-33 Vector Store Demo Completed Successfully")
                