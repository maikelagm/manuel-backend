from sqlalchemy.orm import Session

from .base_class import Base
from .session import engine


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def init_db(session: Session) -> None:
    create_tables()
