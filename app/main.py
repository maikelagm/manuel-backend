from fastapi import FastAPI
from router import connection_routes, scann_routes

app = FastAPI()

app.include_router(connection_routes.connection, prefix="/connection", tags=["database"])
app.include_router(scann_routes.router, prefix="/scan", tags=["security"])
