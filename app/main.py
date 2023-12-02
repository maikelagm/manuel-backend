import uvicorn
from fastapi import FastAPI
from fastapi_offline import FastAPIOffline

from router import connection_routes, scann_routes

app = FastAPIOffline()

app.include_router(connection_routes.connection, prefix="/connection", tags=["database"])
app.include_router(scann_routes.router, prefix="/scan", tags=["security"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)