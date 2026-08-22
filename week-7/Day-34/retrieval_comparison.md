# Dense Retrieval vs Hybrid Retrieval

## Dense Retrieval

- Uses vector embeddings.
- Finds semantically similar documents.
- Works well even when exact keywords are missing.

## BM25 Retrieval

- Uses keyword matching.
- Fast and effective for exact terms.
- Cannot understand semantic meaning.

## Hybrid Retrieval

Hybrid Retrieval combines both Dense Retrieval and BM25 using Reciprocal Rank Fusion (RRF).

### Advantages

- Better recall
- Better ranking quality
- Handles both semantic and keyword queries
- Commonly used in production RAG systems