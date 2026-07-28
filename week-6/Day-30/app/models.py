from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    sessions = relationship(
        "ChatSession",
        back_populates="user"
    )


class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        default="New Chat"
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="sessions"
    )

    messages = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete"
    )


class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    role = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id")
    )

    session = relationship(
        "ChatSession",
        back_populates="messages"
    )