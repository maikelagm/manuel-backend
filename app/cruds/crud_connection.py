from app.db.crud_base import CRUDBase
from app.models.connection_model import Connection
from app.schema.connection_schema import ConnectionPost, ConnectionPut


class CRUDConnection(CRUDBase[Connection, ConnectionPost, ConnectionPut]):
    pass


crud_connection = CRUDConnection(Connection)
