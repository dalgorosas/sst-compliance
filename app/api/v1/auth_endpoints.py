from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.session import get_db
from app.repositories.user_repo import UserRepo
from app.schemas.auth import LoginRequest, TokenResponse, UserCreate, UserRead, UserWithToken
from app.services.google_sheets import GoogleSheetsRegistry


registry = GoogleSheetsRegistry()

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepo()
    if repo.get_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    user = repo.create_user(
        db,
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
        role=user_in.role,
    )
    registry.register_user(
        email=user.email,
        hashed_password=user.hashed_password,
        role=user.role.value if hasattr(user.role, "value") else str(user.role),
    )
    return user


@router.post("/login", response_model=UserWithToken)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    repo = UserRepo()
    user = repo.authenticate(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = TokenResponse(access_token=create_access_token(str(user.id)))
    return UserWithToken(user=user, token=token)


@router.get("/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    repo = UserRepo()
    return repo.list(db)
