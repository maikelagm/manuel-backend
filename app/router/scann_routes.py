from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from  utils.security_tests import available_tests, run_test

router = APIRouter()

@router.get("/security_tests", response_class=HTMLResponse)
async def get_security_tests():
    # Endpoint para obtener la lista de pruebas de seguridad disponibles
    tests_list = "<ul>"
    for test_name in available_tests:
        tests_list += f"<li>{test_name}</li>"
    tests_list += "</ul>"
    return f"<h2>Pruebas de Seguridad Disponibles:</h2>{tests_list}"

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
        result, execution_info = run_test(test_name, password)
        return HTMLResponse(content=execution_info, status_code=200) if result == "success" else HTTPException(status_code=500, detail=execution_info)
    except Exception as e:
        # Manejo de errores generales
        error_detail = str(e)
        return HTTPException(status_code=500, detail=f"Error durante la ejecución de la prueba: {error_detail}")
