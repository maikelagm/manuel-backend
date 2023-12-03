from fastapi_utils.api_model import APIModel


class SecurityTest(APIModel):
    name: str
    description: str


class SecurityTestPost(SecurityTest):
    pass


class SecurityTestPut(SecurityTest):
    pass


class SecurityTestGet(SecurityTest):
    id: str
