from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.cruds.crud_connection import crud_connection
from app.cruds.crud_security_test import crud_security_test
from app.db.deps import get_session
from app.models.security_test_model import SecurityTestModel
from app.services.db_tests_service import db_security_test_service

router = APIRouter()


@router.get("/list")
async def get_security_tests(db: Session = Depends(get_session)):
    return crud_security_test.get_multi(db=db)


@router.get("/run_test/{test_name}", response_class=HTMLResponse, summary="Ejecutar una prueba de seguridad")
async def run_security_test(test_name: str, password: str):
    """
    Endpoint para ejecutar una prueba de seguridad específica.

    Parámetros:
    - test_name: Nombre de la prueba de seguridad a ejecutar.
    - password: Contraseña para la prueba.

    Retorna:
    - HTMLResponse con el resultado y detalles de la ejecución.
    - HTTPException en caso de error con detalles.
    """
    try:
        result, execution_info = db_security_test_service.run_test(test_name, password)
        return HTMLResponse(content=execution_info, status_code=200) if result == "success" else HTTPException(
            status_code=500, detail=execution_info)
    except Exception as e:
        # Manejo de errores generales
        error_detail = str(e)
        return HTTPException(status_code=500, detail=f"Error durante la ejecución de la prueba: {error_detail}")
