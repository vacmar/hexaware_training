from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return payload

def require_role(required_role: str):
    def role_checker(current_user: str = Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return role_checker

'''
Payload of the JWT token:
{
  "sub": "bhuvi@example.com",
  "role": "admin",
  "exp": 1740486000
}
get_current_user will decode the token and extract the email and role. 

return current_user will return a dictionary like:
{
  "sub": "bhuvi@example.com",
  "role": "user"
}

'''