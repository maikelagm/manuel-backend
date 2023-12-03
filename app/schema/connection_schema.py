import uuid

from fastapi_utils.api_model import APIModel


class ConnectionBase(APIModel):
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str
    db_engine: str

    def get_url(self):
        return f"{self.db_engine}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class ConnectionPost(ConnectionBase):
    pass


class ConnectionPut(ConnectionBase):
    pass


class ConnectionGet(ConnectionBase):
    id: str


class DBInfo(APIModel):
    version: str
    engine: str


class ConnectionEstablished(APIModel):
    status: str
    id: str
    db_url: str
    db_info: DBInfo
