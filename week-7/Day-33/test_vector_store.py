from embedding_service import EmbeddingService
from chroma_store import ChromaVectorStore
from models import Document


def test_vector_store():

    embedder = EmbeddingService()

    store = ChromaVectorStore()

    try:
        store.clear()
    except Exception:
        pass

    document = Document(
        id="test1",
        content="Artificial Intelligence is transforming education.",
        embedding=embedder.embed(
            "Artificial Intelligence is transforming education."
        ),
        metadata={
            "doc_type": "article"
        }
    )

    store.add_documents([document])

    results = store.search(
        embedder.embed("AI in education"),
        top_k=1
    )

    assert len(results) == 1

    assert results[0].id == "test1"

    store.delete_document("test1")

    print("All tests passed.")


if __name__ == "__main__":
    test_vector_store()