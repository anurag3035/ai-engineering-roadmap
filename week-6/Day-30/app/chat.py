from sqlalchemy.orm import Session

from app.models import Message
from app.models import ChatSession

from app.gemini_client import GeminiClient


class ChatService:

    def __init__(self):

        self.client = GeminiClient()

    def send_message(
        self,
        db: Session,
        session_id: int,
        user_message: str
    ):

        session = db.query(
            ChatSession
        ).filter(
            ChatSession.id == session_id
        ).first()

        if not session:
            raise ValueError("Chat session not found.")

        history = db.query(
            Message
        ).filter(
            Message.session_id == session_id
        ).all()

        user = Message(
            role="user",
            content=user_message,
            session_id=session_id
        )

        db.add(user)
        db.commit()

        reply = self.client.chat(
            history,
            user_message
        )

        assistant = Message(
            role="assistant",
            content=reply,
            session_id=session_id
        )

        db.add(assistant)
        db.commit()

        return reply

    def get_history(
        self,
        db: Session,
        session_id: int
    ):

        return db.query(
            Message
        ).filter(
            Message.session_id == session_id
        ).all()