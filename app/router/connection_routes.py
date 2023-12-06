from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Path
from sqlalchemy.orm import Session

from app.cruds.crud_connection import crud_connection
from app.db.deps import get_session
from app.models.connection_model import ConnectionModel
from app.schema.connection_schema import ConnectionPost, ConnectionEstablished
from app.services.db_connection_service import db_connection_service

connection = APIRouter()


@connection.post("/create")
async def create_db_connection(
        connection: ConnectionPost,
        db: Session = Depends(get_session)
):
    success, db_info = db_connection_service.attempt_db_connection(
        connection=connection, db=db
    )

    if success:
        connection_created = crud_connection.create(db=db, obj_in=connection)
        id = connection_created.id
        connection_established = ConnectionEstablished(
            status="success",
            db_url=connection.get_url(),
            db_info=db_info,
            id=str(connection_created.id)
        )
        return connection_established

    else:
        raise HTTPException(status_code=500,
                            detail={"status": "error", "detail": db_info, "db_url": connection.get_url()})


@connection.delete("/delete")
async def delete_db_connection(
        id: str,
        db: Session = Depends(get_session)
):
    try:
        connection_removed = crud_connection.remove(db=db, id=id)

        return {"status": "success", "id": connection_removed.id}
    except Exception as e:
        raise HTTPException(status_code=404, detail={"status": "error", "error_detail": str(e)})
