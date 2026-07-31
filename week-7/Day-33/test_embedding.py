from embedding_service import EmbeddingService

embedder = EmbeddingService()

vector = embedder.embed(
    "Artificial Intelligence is transforming education."
)

print(len(vector))
print(vector[:10])