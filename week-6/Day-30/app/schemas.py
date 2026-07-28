from pydantic import BaseModel


class UserRegister(BaseModel):

    username: str

    password: str


class UserLogin(BaseModel):

    username: str

    password: str


class Token(BaseModel):

    access_token: str

    token_type: str


class ChatRequest(BaseModel):

    session_id: int

    message: str


class ChatResponse(BaseModel):

    response: str


class SessionCreate(BaseModel):

    title: str


class MessageResponse(BaseModel):

    role: str

    content: str