from typing import Union, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, create_session, Session
from contextlib import contextmanager

from app.cruds.crud_connection import crud_connection
from app.schema.connection_schema import ConnectionPost, DBInfo


class DBConnectionService:
    @contextmanager
    def create_session(self, db_url: str):
        engine = create_engine(db_url)
        db = sessionmaker(bind=engine)()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()

    def get_session(self, db_url: str) -> Optional[Session]:
        try:
            return create_session(db_url=db_url)
        except Exception as e:
            return None

    def attempt_db_connection(self, db: Session, connection: ConnectionPost) -> tuple[bool, object]:
        db_url: str = connection.get_url()

        with self.create_session(db_url=db_url) as db:
            try:
                # Intenta conectar a la base de datos
                version_query = text("SELECT version()")
                db_version = db.execute(version_query).scalar()

                engine_query = text("SELECT current_setting('server_version_num') AS engine")
                db_engine = db.execute(engine_query).scalar()

                # Guarda la conexión en la base de datos de la aplicación solo si el estado es "success"
                if db_version and db_engine:
                    print("Conexión exitosa")
                    # Importante: No es necesario commit aquí, ya que se hace en el administrador de contexto
                else:
                    raise Exception("Error durante la conexión")

                db_info = DBInfo(version=db_version, engine=db_engine)
                return True, db_info
            except Exception as e:
                # Captura cualquier error durante la conexión
                error_detail = str(e)
                return False, {"error_detail": error_detail}


db_connection_service = DBConnectionService()
