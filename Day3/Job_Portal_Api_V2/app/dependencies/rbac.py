from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database.session import get_db
from app.repositories.user_repo import get_user_by_email
from app.core.security import oauth2_scheme
from app.core.config import SECRET_KEY, ALGORITHM


# -------------------------------------------------
# Get Current Authenticated User
# -------------------------------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Extract user from JWT token and return DB user object.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
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

    user = get_user_by_email(db, email)

    if user is None:
        raise credentials_exception

    return user


# -------------------------------------------------
# Single Role Required
# -------------------------------------------------

def role_required(required_role: str):
    """
    Restrict access to a single role.
    """

    def role_checker(user=Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return user

    return role_checker


# -------------------------------------------------
# Multiple Roles Allowed
# -------------------------------------------------

def roles_required(allowed_roles: list[str]):
    """
    Restrict access to multiple roles.
    """

    def role_checker(user=Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return user

    return role_checker