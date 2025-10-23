from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type

T = TypeVar("T")

class BaseRepo(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get(self, db: Session, id: int) -> T | None:
        return db.get(self.model, id)

    def list(self, db: Session, limit: int = 100, offset: int = 0) -> list[T]:
        return db.query(self.model).offset(offset).limit(limit).all()
