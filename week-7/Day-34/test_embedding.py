from embedding_service import EmbeddingService

embedder = EmbeddingService()

vector = embedder.embed(
    "Artificial Intelligence is transforming education."
)

print("Embedding Length :", len(vector))

print("First 5 Values :")

print(vector[:5])