import traceback

try:
    print("Importing EmbeddingService...")
    from embedding_service import EmbeddingService
    print("Import successful.")

    print("Creating EmbeddingService...")
    embedder = EmbeddingService()
    print("EmbeddingService created.")

    print("Generating embedding...")
    vector = embedder.embed(
        "Artificial Intelligence is transforming education."
    )

    print("Embedding generated successfully.")
    print("Embedding Length:", len(vector))
    print("First 5 values:", vector[:5])

except Exception as e:
    print("\nAn error occurred:\n")
    traceback.print_exc()