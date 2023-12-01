from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Connection(Base):
    __tablename__ = "connections"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    db_engine = Column(String, nullable=False)
    db_user = Column(String, nullable=False)
    db_password = Column(String, nullable=False)
    db_host = Column(String, nullable=False)
    db_port = Column(String, nullable=False)
    db_name = Column(String, nullable=False)

    def get_db_url(self):
        return f"{self.db_engine}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
