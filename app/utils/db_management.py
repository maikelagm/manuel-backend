from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from  model.connection_model import Connection

@contextmanager
def create_session(db_url):
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

def attempt_db_connection(db_engine, db_user, db_password, db_host, db_port, db_name):
    db_url = f"{db_engine}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    with create_session(db_url) as db:
        try:
            # Intenta conectar a la base de datos
            version_query = text("SELECT version()")
            db_version = db.execute(version_query).scalar()

            engine_query = text("SELECT current_setting('server_version_num') AS engine")
            db_engine = db.execute(engine_query).scalar()

            # Guarda la conexión en la base de datos de la aplicación solo si el estado es "success"
            if db_version and db_engine:
                # connection = Connection(
                #     db_engine=db_engine,
                #     db_user=db_user,
                #     db_password=db_password,
                #     db_host=db_host,
                #     db_port=db_port,
                #     db_name=db_name
                # )
                # db.add(connection)
                print("Conexión exitosa")

                # Importante: No es necesario commit aquí, ya que se hace en el administrador de contexto
            else:
                raise Exception("Error durante la conexión")

            return True, {"version": db_version, "engine": db_engine}
        except Exception as e:
            # Captura cualquier error durante la conexión
            error_detail = str(e)
            return False, {"error_detail": error_detail}

