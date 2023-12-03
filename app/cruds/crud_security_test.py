from app.db.crud_base import CRUDBase
from app.models.security_test_model import SecurityTestModel
from app.schema.security_test_schema import SecurityTest, SecurityTestPost, SecurityTestPut


class CRUDSecurityTest(CRUDBase[SecurityTestModel, SecurityTestPost, SecurityTestPut]):
    pass


crud_security_test = CRUDSecurityTest(SecurityTestModel)
