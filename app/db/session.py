from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLITE_URI, pool_pre_ping=True, echo=True)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def get_session() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
