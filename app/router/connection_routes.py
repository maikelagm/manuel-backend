from fastapi import APIRouter, HTTPException
from model.connection_model import Connection
from utils.db_management import attempt_db_connection
from config.db import conn
from typing import List

connection = APIRouter()


@connection.post("/create")
async def create_db_connection(
    db_host: str,
    db_port: str,
    db_name: str,
    db_user: str,
    db_password: str,
    db_engine: str,
):
    db_url = f"{db_engine}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    success,db_info = attempt_db_connection(
    db_engine, db_user, db_password, db_host, db_port, db_name
)

    if success:
        new_connection = Connection(
            db_engine=db_engine,
            db_user=db_user,
            db_password=db_password,
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
        )
        return {"status": "success", "db_url": db_url, "db_info": db_info}

    else:
        raise HTTPException(status_code=500, detail={"status": "error", "detail": db_info, "db_url": db_url})
        