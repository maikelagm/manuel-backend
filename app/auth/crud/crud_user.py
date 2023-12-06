from typing import Any, Dict

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.auth import schemas
from app.auth.models import User
from app.db.crud_base import CRUDBase


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    @staticmethod
    def get_by_email(db: Session, *, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_username(db: Session, *, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            name=obj_in.name,
            surname=obj_in.surname,
            email=obj_in.email,
            ci=obj_in.ci,
            role=obj_in.role,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: User,
            obj_in: schemas.UserUpdate | Dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, target_id=db_obj.id, obj_in=update_data)

    def authenticate(
            self,
            db: Session,
            *,
            email: str,
            password: str
    ) -> User | None:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active


user = CRUDUser(User)
