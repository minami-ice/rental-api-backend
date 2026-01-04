import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = os.getenv("APP_SECRET", "change_me")
ALGO = "HS256"
EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

def hash_password(p: str) -> str:
    return pwd_context.hash(p)

def verify_password(p: str, h: str) -> bool:
    return pwd_context.verify(p, h)

def create_access_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=EXPIRE_MIN)
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload.get("sub") or ""
    except JWTError:
        return ""
