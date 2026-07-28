from sqlalchemy.orm import Session

from app.models import ChatSession
from app.models import Message


class HistoryService:

    def get_sessions(
        self,
        db: Session,
        user_id: int
    ):

        return db.query(
            ChatSession
        ).filter(
            ChatSession.user_id == user_id
        ).all()

    def get_messages(
        self,
        db: Session,
        session_id: int
    ):

        return db.query(
            Message
        ).filter(
            Message.session_id == session_id
        ).all()

    def delete_session(
        self,
        db: Session,
        session_id: int
    ):

        session = db.query(
            ChatSession
        ).filter(
            ChatSession.id == session_id
        ).first()

        if session:

            db.delete(session)

            db.commit()

            return True

        return False