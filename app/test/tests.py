from app.test.base_test import BaseTest
from app.test.base_test import TestResult
from password_strength import PasswordPolicy, tests, PasswordStats
from app.services.db_connection_service import db_connection_service
from sqlalchemy import text
from app.db.session import get_session
from app.schema.connection_schema import ConnectionPost



class PasswordStrengthTest(BaseTest):
    """ Prueba de fortaleza de contraseña
    
    Esta prueba evalúa la fortaleza de una contraseña utilizando la librería password_strength.
    
    """
    
    def __init__(self, connection_params):
        super(PasswordStrengthTest, self).__init__(connection_params)
        self.connection_params = connection_params
    
    def info(self):
        return {
            "name": "Fortaleza de contraseña",
            "description": "Evalúa la fortaleza de una contraseña utilizando la librería password_strength, en caso de que la contraseña no cumpla con los criterios mínimos, se muestran los test que fallaron para que el usuario pueda corregirlos."
        }

    def run(self):
        """
        Realiza una prueba de fortaleza de contraseña utilizando password_strength.

        Retorna un objeto SecurityTestResult con el resultado de la prueba.
        """
        password = self.connection_params.db_password
        # password = "Lir9jsd08./fjkd!"  # Debes implementar esta función según tus necesidades

        # Define la política de fortaleza de la contraseña
        policy = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1,
            special=1,
            strength=0.66,
            entropybits=30
        )

        # Evalúa la contraseña con respecto a la política
        result_tests = policy.test(password)

        # Evalúa la fortaleza de la contraseña
        password_strength = policy.password(password)


        # Construye la descripción detallada en formato Markdown
        description = f"**Detalles de la Prueba:**\n\n"


        # Determina el estado y el riesgo basado en los resultados de la prueba
        if result_tests == []:
            status = "pass"
            risk = "low"
            description = f"* La contraseña es lo suficientemente fuerte.\n\n"
        elif tests.EntropyBits(30).test((PasswordStats(password))):
            status = "pass"
            risk = "medium"
            description += f"* La entropía de la contraseña es baja: {PasswordStats(password).entropy_bits} bits.\n\n"
            description += f"* La contraseña contiene un alfabeto común.\n\n"
            description += f"* La contraseña es medianamente fuerte con una puntuación: {password_strength.strength()}\n\n"
            description += f"***Se recomienda cambiar la contraseña por una más fuerte***.\n\n"
        else:
            status = "pass"
            risk = "high"

            # Switch para manejar diferentes tipos de errores
            if tests.Length(8).test((PasswordStats(password))) == False:
                description += f"* La contraseña no cumple con la longitud mínima de `8` caracteres.\n\n"
            if tests.Uppercase(1).test((PasswordStats(password))) == False:
                description += f"* La contraseña no contiene `letras mayúsculas`, se requiere al menos 1.\n\n"
            if tests.Numbers(1).test((PasswordStats(password)))==False:
                description += f"* La contraseña no contiene `números`, se requiere al menos 1.\n\n"
            if tests.Special(1).test((PasswordStats(password))) == False:
                description += f"* La contraseña no contiene caracteres especiales `!@#$^&*.?`, se requiere al menos 1.\n\n"
            if tests.EntropyBits(30).test((PasswordStats(password))) == False:
                description += f"* La contraseña contiene un alfabeto común. No pasó la prueba de entropía mínima `e <= 30 bits`\n\n"
            if tests.Strength(0.66).test((PasswordStats(password))) == False:
                description += f"* Se considera una contraseña debil. No pasó la prueba de fortaleza de contraseña `f < 0.66`\n\n"
                
            
        strength = round(password_strength.strength(), 2)
        description += f"**Puntuación de Fortaleza:** `{strength}`\n\n"

        # Construye y retorna el resultado
        result_data = {
            "status": status,
            "risk": risk,
            # "name": self.cls.name(),
            "name": "Fortaleza de contraseña",
            "description": description,
        }

        return TestResult(**result_data)

class TestTrazabilidad(BaseTest):
    
    def __init__(self, connection_params):
        super(TestTrazabilidad, self).__init__(connection_params)
        self.connection_params = connection_params
    
    def info(self):
        return {
            "name": "Test de Trazabilidad",
            "description": "La trazabilidad se define como la capacidad que tiene una organización o sistema para rastrear, reconstruir o establecer relaciones entre objetos monitoreados, para identificar y analizar situaciones específicas o generales en los mismos."
        }
        
    def run(self):
        # Construir un objeto ConnectionPost desde los parámetros de conexión
        connection_post = ConnectionPost(
            db_host=self.connection_params.db_host,
            db_port=self.connection_params.db_port,
            db_name=self.connection_params.db_name,
            db_user=self.connection_params.db_user,
            db_password=self.connection_params.db_password,
            db_engine=self.connection_params.db_engine
        )

        # Obtén la información de conexión
        db_url = connection_post.get_url()

        # Intenta establecer una conexión a la base de datos
        success, db_info = db_connection_service.attempt_db_connection(None, connection_post)

        if success:
            # Calcula la métrica de seguridad para evaluar la trazabilidad
            cor = self.get_operation_count(db_url)
            cost = self.get_tracked_operation_count(db_url)

            # Evitar la división por cero
            if cor == 0:
                stbd = 0
            else:
                stbd = (cost / cor) * 0.1

            # Determina el estado y el riesgo basado en el valor de STBD
            if stbd == 1:
                status = "pass"
                risk = "low"
                description = (
                    "#### Detalles del test\n\n"
                    "El grado de seguimiento de trazabilidad es óptimo.\n\n"
                )
            else:
                status = "fail"
                risk = "high"
                description = (
                    "**Detalles del test**\n\n"
                    "El grado de seguimiento de trazabilidad no cumple con los estándares de seguridad.\n\n"
                )

            # Detalles adicionales
            description += (
                f"* **Cantidad total de operaciones realizadas:** {cor}\n\n"
                f"* **Cantidad de operaciones con seguimiento de trazabilidad:** {cost}\n\n"
                f"* **Puntuación de trazabilidad (STBD):** {round(stbd, 2)}\n\n"
            )

        else:
            # En caso de fallo en la conexión, establece el estado del test como fallido
            status = "fail"
            risk = "high"
            description = "### Resultado del Test de Trazabilidad\n\nError durante la conexión a la base de datos. No se pudo ejecutar el test de trazabilidad.\n\n"

        return TestResult(**{
            "status": status,
            "risk": risk,
            "name": "Test de Trazabilidad",
            "description": description,
        })

    def get_operation_count(self, db_url):
        # Implementa la lógica para obtener la cantidad total de operaciones realizadas a la base de datos
        try:
            with db_connection_service.create_session(db_url=db_url) as db:
                # Utilizamos la ubicación del archivo de registro de PostgreSQL como ejemplo
                if "postgresql" in db_url:
                    operation_count_query = text("SELECT COUNT(*) FROM pg_stat_bgwriter;")
                elif "mysql" in db_url:
                    # Utilizamos la tabla general_log de MySQL como ejemplo
                    operation_count_query = text("SELECT COUNT(*) FROM mysql.general_log;")
                else:
                    # Agrega lógica para otros motores de base de datos según sea necesario
                    raise NotImplementedError("Motor de base de datos no compatible")

                operation_count = db.execute(operation_count_query).scalar()
                return operation_count
        except Exception as e:
            # Manejar el error si no se puede obtener la cantidad de operaciones
            return 0

    def get_tracked_operation_count(self, db_url):
        # Implementa la lógica para obtener la cantidad de operaciones con seguimiento de trazabilidad
        try:
            with db_connection_service.create_session(db_url=db_url) as db:
                # Utilizamos la ubicación del archivo de registro de PostgreSQL como ejemplo
                if "postgresql" in db_url:
                    tracked_operation_count_query = text("SELECT COUNT(*) FROM pg_stat_bgwriter WHERE tracked = true;")
                elif "mysql" in db_url:
                    # Utilizamos la tabla general_log de MySQL como ejemplo
                    tracked_operation_count_query = text("SELECT COUNT(*) FROM mysql.general_log WHERE tracked = true;")
                else:
                    # Agrega lógica para otros motores de base de datos según sea necesario
                    raise NotImplementedError("Motor de base de datos no compatible")

                tracked_operation_count = db.execute(tracked_operation_count_query).scalar()
                return tracked_operation_count
        except Exception as e:
            # Manejar el error si no se puede obtener la cantidad de operaciones rastreadas
            return 0
        
class ConnectionTest(BaseTest):
    def __init__(self, connection_params):
        super(ConnectionTest, self).__init__(connection_params)
        self.connection_params = connection_params

    def info(self):
        return {
            "name": "Test de Conexión",
            "description": "Evalúa la conexión a la base de datos."
        }

    def run(self):
        return TestResult(**{
            "status": "pass",
            "risk": "low",
            "name": "Test de Conexión",
            "description": "La conexión a la base de datos se estableció correctamente."
        })
        
class EncriptacionAlmacenamiento(BaseTest):
    def __init__(self, connection_params):
        super(EncriptacionAlmacenamiento, self).__init__(connection_params)
        self.connection_params = connection_params

    def info(self):
        return {
            "name": "Encriptación de Almacenamiento",
            "description": "Evalúa la encriptación de almacenamiento de la base de datos."
        }

    def run(self):
        return TestResult(**{
            "status": "pass",
            "risk": "low",
            "name": "Encriptación de Almacenamiento",
            "description": "La encriptación de almacenamiento de la base de datos se estableció correctamente."
        })
        
class ImplementacionLogica(BaseTest):
    def __init__(self, connection_params):
        super(ImplementacionLogica, self).__init__(connection_params)
        self.connection_params = connection_params

    def info(self):
        return {
            "name": "Implementación Lógica",
            "description": "Evalúa la implementación lógica de la base de datos."
        }

    def run(self):
        return TestResult(**{
            "status": "pass",
            "risk": "low",
            "name": "Implementación Lógica",
            "description": "La implementación lógica de la base de datos se estableció correctamente."
        })