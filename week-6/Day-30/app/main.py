from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.database import get_db

from app.models import User
from app.models import ChatSession

from app.schemas import (
    UserRegister,
    UserLogin,
    ChatRequest,
    ChatResponse,
    SessionCreate,
)

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.chat import ChatService
from app.history import HistoryService
from app.stream import StreamService


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gemini Chat API",
    version="1.0.0"
)

chat_service = ChatService()
history_service = HistoryService()
stream_service = StreamService()
@app.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered successfully."
    }
@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
        )

    token = create_access_token(
        {
            "sub": db_user.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@app.post("/session")
def create_session(
    session: SessionCreate,
    db: Session = Depends(get_db)
):

    new_session = ChatSession(
        title=session.title,
        user_id=1
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "session_id": new_session.id,
        "title": new_session.title
    }
@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    reply = chat_service.send_message(
        db=db,
        session_id=request.session_id,
        user_message=request.message
    )

    return ChatResponse(
        response=reply
    )
@app.get("/history/{session_id}")
def history(
    session_id: int,
    db: Session = Depends(get_db)
):

    messages = history_service.get_messages(
        db,
        session_id
    )

    return [
        {
            "role": message.role,
            "content": message.content
        }
        for message in messages
    ]
