from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType
import uuid

from app.db.base_class import Base


class SecurityTestModel(Base):
    __tablename__ = "security_tests"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
