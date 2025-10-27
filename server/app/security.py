from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  return pwd_context.hash(password)

def _create(data: dict, secret: str, delta: timedelta):
  to_encode = data.copy()
  to_encode.update({"exp": datetime.now(timezone.utc) + delta})
  return jwt.encode(to_encode, secret, algorithm=ALGORITHM)

def create_access_token(sub: str, secret: str):  # type: access
  return _create({"sub": sub, "type":"access"}, secret, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(sub: str, secret: str): # type: refresh
  return _create({"sub": sub, "type":"refresh"}, secret, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

def create_reset_token(sub: str, secret: str):   # type: reset
  return _create({"sub": sub, "type":"reset"}, secret, timedelta(minutes=30))

def decode_token(token: str, secret: str) -> Optional[dict]:
  try: return jwt.decode(token, secret, algorithms=[ALGORITHM])
  except JWTError: return None
