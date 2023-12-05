from fastapi_utils.api_model import APIModel
from typing import List

class SecurityTest(APIModel):
    name: str
    description: str


class SecurityTestPost(APIModel):
    connection_id: str
    security_tests: List[str]
    pass


class SecurityTestPut(SecurityTest):
    pass


class SecurityTestGet(SecurityTest):
    id: str


class SecurityTestResult(APIModel):
    status: str
    risk: str
    name: str
    description: str
