from sqlalchemy.orm import Session

from .base_class import Base
from .session import engine
# from ..services.db_tests_service import db_security_test_service


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def init_db(session: Session) -> None:
    create_tables()
    # db_security_test_service.insert_test_in_db(db=session)
