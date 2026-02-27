#JWT + BCRYPT
#passlib - password hashing library
#CryptContext - class from passlib to handle password hashing and verification
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#create access token
def create_access_token(data: dict) -> str:
    to_encode = data.copy() #{"sub": "bhuvi@example.com"}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) #{"sub": "bhuvi@example.com","exp": 2026-02-25T10:30:00Z}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    return encoded_jwt