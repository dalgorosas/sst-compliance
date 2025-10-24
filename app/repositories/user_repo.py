from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import PasswordManager
from app.models.user import User
from .base import BaseRepo


class UserRepo(BaseRepo[User]):
    def __init__(self) -> None:
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    def authenticate(self, db: Session, email: str, password: str) -> User | None:
        user = self.get_by_email(db, email)
        if user and PasswordManager.verify_password(password, user.hashed_password):
            return user
        return None

    def create_user(self, db: Session, email: str, password: str, full_name: str, role: str) -> User:
        hashed = PasswordManager.hash_password(password)
        return self.create(db, email=email, hashed_password=hashed, full_name=full_name, role=role)