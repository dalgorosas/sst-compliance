from __future__ import annotations

from typing import Generic, Iterable, TypeVar, Type

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepo(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get(self, db: Session, id_: int) -> T | None:
        return db.get(self.model, id_)

    def list(self, db: Session, limit: int = 100, offset: int = 0) -> list[T]:
        stmt = select(self.model).offset(offset).limit(limit)
        return list(db.execute(stmt).scalars())

    def create(self, db: Session, **data) -> T:
        obj = self.model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: T, **data) -> T:
        for key, value in data.items():
            setattr(obj, key, value)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: T) -> None:
        db.delete(obj)
        db.commit()

    def bulk_create(self, db: Session, items: Iterable[dict]) -> list[T]:
        objs = [self.model(**item) for item in items]
        db.add_all(objs)
        db.commit()
        for obj in objs:
            db.refresh(obj)
        return objs
