import uvicorn
from fastapi_offline import FastAPIOffline

from app.db.init_db import create_tables, init_db
from app.db.session import SessionLocal
from app.router import connection_routes, security_test_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPIOffline()




origins = [
    "http://localhost:5174",
    "http://localhost",
    "https://swr.vercel.app/examples/basic"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(connection_routes.connection, prefix="/connection", tags=["database"])
app.include_router(security_test_routes.router, prefix="/security-test", tags=["security"])


@app.on_event("startup")
def startup():
    session = SessionLocal()
    init_db(session)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
