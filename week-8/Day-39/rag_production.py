import asyncio
import hashlib
import time
from datetime import datetime

from cachetools import TTLCache
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel


app = FastAPI(title="Production RAG")


documents = {}
ingestion_jobs = {}

query_cache = TTLCache(
    maxsize=100,
    ttl=300
)


stats = {
    "queries": 0,
    "cache_hits": 0,
    "cache_misses": 0,
    "total_documents": 0,
    "total_chunks": 0,
    "total_latency_ms": 0
}


class IngestRequest(BaseModel):
    documents: list[str]


class QueryRequest(BaseModel):
    query: str


def create_document_id(text):
    return hashlib.md5(
        text.encode()
    ).hexdigest()


def create_chunks(text, chunk_size=300):
    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk:
            chunks.append(chunk)

    return chunks


async def ingest_documents(
    job_id,
    new_documents
):

    ingestion_jobs[job_id] = {
        "status": "running",
        "processed": 0,
        "total": len(new_documents),
        "started_at": datetime.now().isoformat()
    }

    for text in new_documents:

        document_id = create_document_id(text)

        if document_id in documents:
            ingestion_jobs[job_id]["processed"] += 1
            continue

        chunks = create_chunks(text)

        documents[document_id] = {
            "document_id": document_id,
            "content": text,
            "chunks": chunks,
            "indexed_at": datetime.now().isoformat()
        }

        ingestion_jobs[job_id]["processed"] += 1

        await asyncio.sleep(0.1)

    stats["total_documents"] = len(documents)

    stats["total_chunks"] = sum(
        len(document["chunks"])
        for document in documents.values()
    )

    ingestion_jobs[job_id]["status"] = "completed"
    ingestion_jobs[job_id]["completed_at"] = (
        datetime.now().isoformat()
    )


def search_documents(query):

    query_words = set(
        query.lower().split()
    )

    results = []

    for document in documents.values():

        for chunk in document["chunks"]:

            chunk_words = set(
                chunk.lower().split()
            )

            matched_words = query_words.intersection(
                chunk_words
            )

            if matched_words:

                score = (
                    len(matched_words)
                    / max(len(query_words), 1)
                )

                results.append({
                    "document_id": document["document_id"],
                    "content": chunk,
                    "score": score
                })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:5]


async def generate_answer(
    query,
    results
):

    if not results:
        return (
            "I could not find relevant information "
            "in the available documents."
        )

    context = "\n\n---\n\n".join(
        result["content"]
        for result in results
    )

    await asyncio.sleep(0.1)

    return (
        f"Based on the retrieved documents: "
        f"{context}"
    )


@app.post("/ingest")
async def ingest(
    request: IngestRequest,
    background_tasks: BackgroundTasks
):

    job_id = hashlib.md5(
        f"{time.time()}".encode()
    ).hexdigest()

    ingestion_jobs[job_id] = {
        "status": "queued"
    }

    background_tasks.add_task(
        ingest_documents,
        job_id,
        request.documents
    )

    return {
        "job_id": job_id,
        "status": "queued"
    }


@app.get("/ingest/{job_id}")
async def ingestion_status(
    job_id: str
):

    if job_id not in ingestion_jobs:

        return {
            "error": "Job not found"
        }

    return ingestion_jobs[job_id]


@app.post("/query")
async def query(
    request: QueryRequest
):

    start_time = time.perf_counter()

    stats["queries"] += 1

    cache_key = request.query.strip().lower()

    if cache_key in query_cache:

        stats["cache_hits"] += 1

        result = query_cache[cache_key]

        latency = (
            time.perf_counter() - start_time
        ) * 1000

        stats["total_latency_ms"] += latency

        return {
            "answer": result["answer"],
            "cached": True,
            "latency_ms": round(latency, 2)
        }

    stats["cache_misses"] += 1

    results = search_documents(
        request.query
    )

    answer = await generate_answer(
        request.query,
        results
    )

    query_cache[cache_key] = {
        "answer": answer
    }

    latency = (
        time.perf_counter() - start_time
    ) * 1000

    stats["total_latency_ms"] += latency

    return {
        "answer": answer,
        "cached": False,
        "chunks_retrieved": len(results),
        "latency_ms": round(latency, 2)
    }


@app.get("/stats")
async def get_stats():

    queries = stats["queries"]

    average_latency = 0

    if queries > 0:
        average_latency = (
            stats["total_latency_ms"]
            / queries
        )

    cache_total = (
        stats["cache_hits"]
        + stats["cache_misses"]
    )

    cache_hit_rate = 0

    if cache_total > 0:
        cache_hit_rate = (
            stats["cache_hits"]
            / cache_total
        ) * 100

    return {
        "total_queries": queries,
        "cache_hits": stats["cache_hits"],
        "cache_misses": stats["cache_misses"],
        "cache_hit_rate": round(
            cache_hit_rate,
            2
        ),
        "average_latency_ms": round(
            average_latency,
            2
        ),
        "total_documents": stats[
            "total_documents"
        ],
        "total_chunks": stats[
            "total_chunks"
        ],
        "cached_queries": len(query_cache)
    }


@app.get("/")
async def home():

    return {
        "message": "Production RAG API is running"
    }