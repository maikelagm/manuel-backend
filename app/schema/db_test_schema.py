from fastapi_utils.api_model import APIModel


class DBTest(APIModel):
    id: str
    name: str
    description: str
