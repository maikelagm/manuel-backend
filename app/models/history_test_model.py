from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
import uuid
from datetime import datetime

from app.db.base_class import Base
from app.models.connection_model import ConnectionModel


class HistoryTestModel(Base):
    __tablename__ = "history_tests"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    score = Column(String, nullable=False)
    connection_id = Column(UUIDType(binary=False), ForeignKey('connection_models.id'))
    connection = relationship(ConnectionModel)


class TestSecurityResultModel(Base):
    __tablename__ = "test_security_results"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    history_test_id = Column(UUIDType(binary=False), ForeignKey('history_tests.id'))
    security_test_id = Column(UUIDType(binary=False), ForeignKey('security_tests.id'))
    
    status = Column(String, nullable=False)
    risk = Column(String, nullable=False)
    description = Column(String, nullable=False)
    history_test = relationship(HistoryTestModel)