from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import verify_token
from app.repositories.user_repo import UserRepository
from app.models.user import User

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_roles(*roles):
    def wrapper(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user
    return wrapper