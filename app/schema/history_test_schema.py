from fastapi_utils.api_model import APIModel
from typing import List

from app.schema.security_test_schema import SecurityTestResult

class HistoryTest(APIModel):
    date: str
    score: float
    security_tests: List[SecurityTestResult]

class HistoryTestPost(APIModel):
    connection_id: str
    security_tests: List[str]
    pass


class HistoryTestPut(HistoryTest):
    pass


class HistoryTestGet(HistoryTest):
    id: str


class HistoryTestResult(APIModel):
    status: str
    risk: str
    name: str
    description: str