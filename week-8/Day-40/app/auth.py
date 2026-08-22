from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import JWT_SECRET


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_token(username):
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=6)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def get_username(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.PyJWTError:
        return None