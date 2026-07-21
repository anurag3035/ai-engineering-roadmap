import os
import numpy as np

from dotenv import load_dotenv
from google import genai
from data import sentences

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "text-embedding-004"


def get_embedding(text, task_type="RETRIEVAL_DOCUMENT"):
    response = client.models.embed_content(
        model=MODEL,
        contents=text,
        config={
            "task_type": task_type
        }
    )

    return np.array(response.embeddings[0].values)


print("Generating embeddings...\n")

embeddings = []

for sentence in sentences:
    vector = get_embedding(sentence)
    embeddings.append(vector)

embeddings = np.array(embeddings)

norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
embeddings = embeddings / norms


def semantic_search(query, top_k=5):

    query_embedding = get_embedding(
        query,
        task_type="RETRIEVAL_QUERY"
    )

    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    similarities = embeddings @ query_embedding

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for idx in top_indices:
        results.append(
            (
                sentences[idx],
                float(similarities[idx])
            )
        )

    return results


queries = [
    "AI models",
    "cloud platforms",
    "healthy lifestyle",
    "coding",
    "sports",
    "animals",
    "space",
    "databases",
    "music",
    "renewable energy"
]

for query in queries:

    print("=" * 70)
    print(f"Query: {query}\n")

    results = semantic_search(query)

    for rank, (sentence, score) in enumerate(results, start=1):
        print(f"{rank}. {sentence}")
        print(f"   Similarity: {score:.4f}")

    print()