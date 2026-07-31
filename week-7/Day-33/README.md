# Day-33: Vector Store Abstraction

## Overview

This project implements a common Vector Store interface for ChromaDB and Qdrant using Gemini embeddings.

## Features

- Vector Store abstraction
- ChromaDB backend
- Qdrant backend
- Gemini Embeddings
- Similarity Search
- Metadata Filtering
- Document Deletion
- Persistent Storage

## Requirements

```bash
pip install -r requirements.txt
```

## Configure

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
MODEL_NAME=gemini-embedding-001
CHROMA_DB_PATH=./chroma_db
QDRANT_PATH=./qdrant_db
COLLECTION_NAME=documents
```

## Run

```bash
python main.py
```

## Test

```bash
python test_vector_store.py
```

## Project Structure

```
Day-33/
│
├── chroma_store.py
├── qdrant_store.py
├── vector_store.py
├── embedding_service.py
├── config.py
├── models.py
├── main.py
├── test_vector_store.py
├── requirements.txt
└── README.md
```