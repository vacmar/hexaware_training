from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repo import (
    create_user,
    get_user_by_email,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


# -----------------------------
# Register User
# -----------------------------

def register_user(db: Session, user_data: dict):

    existing_user = get_user_by_email(db, user_data["email"])
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user_data["password"] = hash_password(user_data["password"])

    user = create_user(db, user_data)

    return user


# -----------------------------
# Login User
# -----------------------------

def login_user(db: Session, login_data: dict):

    user = get_user_by_email(db, login_data["email"])

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(login_data["password"], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role,
            "user_id": user.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }