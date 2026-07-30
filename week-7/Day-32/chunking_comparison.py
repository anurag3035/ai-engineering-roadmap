from pathlib import Path
from statistics import mean

import nltk
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


with open("sample.txt", "r", encoding="utf-8") as file:
    text = file.read()


model = SentenceTransformer("all-MiniLM-L6-v2")
def fixed_size_chunking(
    text,
    chunk_size=1000,
    overlap=200
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks
def recursive_chunking(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_text(text)
def sentence_chunking(
    text,
    sentences_per_chunk=5
):

    sentences = nltk.sent_tokenize(text)

    chunks = []

    for i in range(0, len(sentences), sentences_per_chunk):

        chunk = " ".join(sentences[i:i + sentences_per_chunk])

        chunks.append(chunk)

    return chunks
def semantic_chunking(
    text,
    threshold=0.65
):

    sentences = nltk.sent_tokenize(text)

    embeddings = model.encode(sentences)

    chunks = []

    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):

        similarity = cosine_similarity(
            [embeddings[i - 1]],
            [embeddings[i]]
        )[0][0]

        if similarity >= threshold:

            current_chunk.append(sentences[i])

        else:

            chunks.append(" ".join(current_chunk))

            current_chunk = [sentences[i]]

    if current_chunk:

        chunks.append(" ".join(current_chunk))

    return chunks
def show_statistics(
    name,
    chunks
):

    sizes = [len(chunk) for chunk in chunks]

    print("=" * 60)

    print(name)

    print(f"Chunks: {len(chunks)}")

    print(f"Average Size: {mean(sizes):.2f}")

    print(f"Minimum Size: {min(sizes)}")

    print(f"Maximum Size: {max(sizes)}")

    print()
fixed_chunks = fixed_size_chunking(text)

recursive_chunks = recursive_chunking(text)

sentence_chunks = sentence_chunking(text)

semantic_chunks = semantic_chunking(text)


show_statistics(
    "Fixed Size Chunking",
    fixed_chunks
)

show_statistics(
    "Recursive Character Chunking",
    recursive_chunks
)

show_statistics(
    "Sentence-aware Chunking",
    sentence_chunks
)

show_statistics(
    "Semantic Chunking",
    semantic_chunks
)


report = f"""
# Chunking Comparison Report

| Strategy | Chunks | Average Size | Min Size | Max Size |
|----------|---------|--------------|----------|----------|
| Fixed Size | {len(fixed_chunks)} | {mean([len(c) for c in fixed_chunks]):.2f} | {min(len(c) for c in fixed_chunks)} | {max(len(c) for c in fixed_chunks)} |
| Recursive | {len(recursive_chunks)} | {mean([len(c) for c in recursive_chunks]):.2f} | {min(len(c) for c in recursive_chunks)} | {max(len(c) for c in recursive_chunks)} |
| Sentence | {len(sentence_chunks)} | {mean([len(c) for c in sentence_chunks]):.2f} | {min(len(c) for c in sentence_chunks)} | {max(len(c) for c in sentence_chunks)} |
| Semantic | {len(semantic_chunks)} | {mean([len(c) for c in semantic_chunks]):.2f} | {min(len(c) for c in semantic_chunks)} | {max(len(c) for c in semantic_chunks)} |

## Recommendation

- Fixed-size chunking is simple and fast.
- Recursive chunking preserves natural text boundaries better than fixed-size splitting.
- Sentence-aware chunking keeps complete sentences together, making it suitable for articles and reports.
- Semantic chunking groups related ideas together, producing the highest-quality chunks for Retrieval-Augmented Generation (RAG), although it requires embedding computation.

Overall, semantic chunking is the best choice when retrieval quality is the priority, while recursive chunking provides an excellent balance between speed and quality.
"""

with open(
    "chunking_report.md",
    "w",
    encoding="utf-8"
) as file:

    file.write(report)

print("=" * 60)
print("Chunking comparison completed.")
print("Report saved as chunking_report.md")

