from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType
import uuid

from app.db.base_class import Base


class ConnectionModel(Base):
    __tablename__ = "connections"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    db_engine = Column(String, nullable=False)
    db_user = Column(String, nullable=False)
    db_password = Column(String, nullable=False)
    db_host = Column(String, nullable=False)
    db_port = Column(String, nullable=False)
    db_name = Column(String, nullable=False)
