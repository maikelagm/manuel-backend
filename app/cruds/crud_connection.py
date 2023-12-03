from app.db.crud_base import CRUDBase
from app.models.connection_model import ConnectionModel
from app.schema.connection_schema import ConnectionPost, ConnectionPut


class CRUDConnection(CRUDBase[ConnectionModel, ConnectionPost, ConnectionPut]):
    pass


crud_connection = CRUDConnection(ConnectionModel)
