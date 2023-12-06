from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.cruds.crud_connection import crud_connection
from app.db.session import get_session
from app.schema.security_test_schema import SecurityTestPost, SecurityTestResult
from app.test.base_test import BaseTest, TestResult

from app.test.policy import TestPolicy
from typing import List
import datetime

router = APIRouter()

@router.get("/list")
async def get_security_tests(db: Session = Depends(get_session)):
    try:
        test_info = {}
        
        for test_name in BaseTest.test_classes.keys():
            test_class = BaseTest.test_classes[test_name]
            test_instance = test_class({})
            info = test_instance.info()
            test_info[test_name] = info

        return test_info
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "error_detail": str(e)})
    
    



@router.post("/run-select", summary="Ejecutar una prueba de seguridad")
async def run_security_test(
    test: SecurityTestPost,
    db: Session = Depends(get_session)
):
    try:
        results: List[TestResult] = []
        
        run_test = test.security_tests
        connection_id = test.connection_id
        
        connection_params = crud_connection.get(db=db, id=connection_id)
        
        print(connection_params)

        for test_name in BaseTest.test_classes.keys():
            test_class = BaseTest.test_classes[test_name]
            
            if test_name not in run_test:
                continue
            test_instance = test_class(connection_params)
            result = test_instance.run()
            results.append(result)  # Aquí se agrega el resultado como una instancia de TestResult
            print(results)

        response_data = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id": "c8e9a7b6-4d3f-4a2e-9c7b-6d4d3f4a2e9c",
            "score": 0.5,
            "security_tested": results
        }

        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "error_detail": str(e)})
