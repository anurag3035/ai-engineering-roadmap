# Gemini Chat API

A production-style AI chat backend built with FastAPI and the Gemini API.

## Features

- User Registration
- JWT Authentication
- Multi-session Chat
- Persistent Chat History (SQLite)
- Gemini AI Integration
- Streaming Responses
- REST API
- Swagger Documentation
- Automated API Tests

## Tech Stack

- FastAPI
- Google Gemini API
- SQLAlchemy
- SQLite
- JWT Authentication
- Pytest

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
MODEL_NAME=gemini-3.5-flash
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///chat.db
```

Run the server:

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

- POST /register
- POST /login
- POST /session
- POST /chat
- GET /history/{session_id}
- GET /stream
- GET /

## Testing

```bash
pytest
```

## Project Structure

```
Day-30
│
├── app
├── tests
├── requirements.txt
├── README.md
└── .env
```