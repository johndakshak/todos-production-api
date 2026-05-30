from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schema.auth_schema import LoginRequest, LoginResponse
from auth.jwt import create_access_token
from security import verify_password

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == login_request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password"
        )

    # Correct password check
    password_match = verify_password(login_request.password, user.password)

    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    claims = {
        "sub": str(user.id),
        "email": user.email,
        "user_id": str(user.id)
    }

    access_token = create_access_token(claims)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        email=user.email,
        user_id=user.id
    )
