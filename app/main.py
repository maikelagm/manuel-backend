from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_offline import FastAPIOffline

from app.db.init_db import create_tables, init_db
from app.db.session import SessionLocal
from router import connection_routes, scann_routes

app = FastAPIOffline()

app.include_router(connection_routes.connection, prefix="/connection", tags=["database"])
app.include_router(scann_routes.router, prefix="/scan", tags=["security"])


@app.on_event("startup")
def startup():
    session = SessionLocal()
    init_db(session)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
