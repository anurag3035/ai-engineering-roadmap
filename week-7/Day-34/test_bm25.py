from bm25_retriever import BM25Retriever
from models import Document


documents = [

    Document(
        id="1",
        content="Artificial Intelligence is transforming education."
    ),

    Document(
        id="2",
        content="Python is a popular programming language."
    ),

    Document(
        id="3",
        content="Machine learning is a subset of Artificial Intelligence."
    )

]

retriever = BM25Retriever()

retriever.add_documents(documents)

results = retriever.search(
    "Artificial Intelligence education",
    top_k=2
)

print("Top Results:\n")

for document in results:

    print(f"ID: {document.id}")
    print(f"Content: {document.content}")
    print("-" * 40)