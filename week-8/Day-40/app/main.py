import asyncio
import json
import os
import uuid

from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.auth import check_password, create_token, get_username, hash_password
from app.config import GEMINI_API_KEY
from app.db import get_db, init_db
from app.rag import RAGService
from app.schemas import ChatRequest, LoginRequest, RegisterRequest


app = FastAPI(title="RAG Assistant - Day 40")
rag = RAGService()


@app.on_event("startup")
def startup():
    init_db()


def current_user(authorization):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    username = get_username(authorization.replace("Bearer ", "", 1))

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return username


@app.get("/health")
def health():
    return {
        "status": "ok",
        "gemini_configured": bool(GEMINI_API_KEY),
        "documents_loaded": len(rag.documents)
    }


@app.post("/auth/register")
def register(data: RegisterRequest):
    with get_db() as conn:
        try:
            conn.execute(
                "INSERT INTO users(username, password) VALUES (?, ?)",
                (data.username, hash_password(data.password))
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Username already exists")

    return {"message": "User registered successfully"}


@app.post("/auth/login")
def login(data: LoginRequest):
    with get_db() as conn:
        row = conn.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (data.username,)
        ).fetchone()

    if not row or not check_password(data.password, row[1]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"access_token": create_token(row[0]), "token_type": "bearer"}


@app.post("/documents/ingest")
async def ingest(
    file: UploadFile = File(...),
    authorization: str | None = Header(default=None)
):
    current_user(authorization)

    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is missing")

    content = (await file.read()).decode("utf-8", errors="ignore")

    if not content.strip():
        raise HTTPException(status_code=400, detail="File is empty")

    document = {
        "content": content,
        "filename": file.filename
    }

    rag.add_documents([document])

    with get_db() as conn:
        conn.execute(
            "INSERT INTO documents(filename, content) VALUES (?, ?)",
            (file.filename, content)
        )

    return {
        "message": "Document ingested",
        "filename": file.filename
    }


@app.post("/chat")
def chat(
    data: ChatRequest,
    authorization: str | None = Header(default=None)
):
    username = current_user(authorization)

    answer, sources = rag.generate(data.message)

    with get_db() as conn:
        conn.execute(
            "INSERT INTO chats(session_id, username, role, message) VALUES (?, ?, ?, ?)",
            (data.session_id, username, "user", data.message)
        )
        conn.execute(
            "INSERT INTO chats(session_id, username, role, message) VALUES (?, ?, ?, ?)",
            (data.session_id, username, "assistant", answer)
        )

    return {
        "answer": answer,
        "sources": sources
    }


@app.post("/chat/stream")
async def chat_stream(
    data: ChatRequest,
    authorization: str | None = Header(default=None)
):
    username = current_user(authorization)

    async def generate():
        answer, sources = rag.generate(data.message)

        words = answer.split()

        for word in words:
            yield f"data: {json.dumps({'type': 'token', 'text': word + ' '})}\n\n"
            await asyncio.sleep(0.02)

        yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"
        yield "data: [DONE]\n\n"

        with get_db() as conn:
            conn.execute(
                "INSERT INTO chats(session_id, username, role, message) VALUES (?, ?, ?, ?)",
                (data.session_id, username, "user", data.message)
            )
            conn.execute(
                "INSERT INTO chats(session_id, username, role, message) VALUES (?, ?, ?, ?)",
                (data.session_id, username, "assistant", answer)
            )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@app.get("/chat/{session_id}/history")
def history(
    session_id: str,
    authorization: str | None = Header(default=None)
):
    username = current_user(authorization)

    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT role, message, created_at
            FROM chats
            WHERE session_id = ? AND username = ?
            ORDER BY id
            """,
            (session_id, username)
        ).fetchall()

    return {
        "session_id": session_id,
        "messages": [
            {
                "role": row[0],
                "message": row[1],
                "created_at": row[2]
            }
            for row in rows
        ]
    }


@app.get("/stats")
def stats(authorization: str | None = Header(default=None)):
    current_user(authorization)

    with get_db() as conn:
        document_count = conn.execute(
            "SELECT COUNT(*) FROM documents"
        ).fetchone()[0]

        chat_count = conn.execute(
            "SELECT COUNT(*) FROM chats WHERE role = 'user'"
        ).fetchone()[0]

    return {
        "documents": document_count,
        "queries": chat_count,
        "loaded_documents_in_memory": len(rag.documents)
    }
