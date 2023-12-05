from app.test.base_test import BaseTest
from app.test.base_test import TestResult
from password_strength import PasswordPolicy, tests, PasswordStats


class PasswordStrengthTest(BaseTest):
    """ Prueba de fortaleza de contraseña
    
    Esta prueba evalúa la fortaleza de una contraseña utilizando la librería password_strength.
    
    """
    
    def __init__(self, connection_params):
        super(PasswordStrengthTest, self).__init__(connection_params)
        self.connection_params = connection_params

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
        description = f"**Detalles de la Prueba de Fortaleza de Contraseña:**\n\n"


        # Determina el estado y el riesgo basado en los resultados de la prueba
        if result_tests == []:
            status = "pass"
            risk = "low"
            description = f"La contraseña es lo suficientemente fuerte. \n"
        elif tests.EntropyBits(30).test((PasswordStats(password))):
            status = "pass"
            risk = "medium"
            description += f"La entropía de la contraseña es baja: {PasswordStats(password).entropy_bits} bits. \n"
            description += f"La contraseña contiene un alfabeto común. \n"
            description += f"La contraseña es medianamente fuerte con una puntuación: {password_strength.strength()} \n"
            description += f"Se recomienda cambiar la contraseña por una más fuerte. \n"
        else:
            status = "pass"
            risk = "high"

            # Switch para manejar diferentes tipos de errores
            if tests.Length(8).test((PasswordStats(password))) == False:
                description += f"La contraseña no cumple con la longitud mínima de 8 caracteres.\n"
            if tests.Uppercase(1).test((PasswordStats(password))) == False:
                description += f"La contraseña no contiene letras mayúsculas, se requiere al menos 1.\n"
            if tests.Numbers(1).test((PasswordStats(password)))==False:
                description += f"La contraseña no contiene números, se requiere al menos 1.\n"
            if tests.Special(1).test((PasswordStats(password))) == False:
                description += f"La contraseña no contiene caracteres especiales, se requiere al menos 1.\n"
            if tests.Strength(0.66).test((PasswordStats(password))) == False:
                description += f"La contraseña no cumple con la fortaleza mínima de 0.66.\n"
            if tests.EntropyBits(30).test((PasswordStats(password))) == False:
                description += f"La contraseña contiene un alfabeto común.\n"
                
            
        strength = round(password_strength.strength(), 2)
        description += f"**Puntuación de Fortaleza:** {strength}\n"

        # Construye y retorna el resultado
        result_data = {
            "status": status,
            "risk": risk,
            # "name": self.cls.name(),
            "name": "Fortaleza de contraseña",
            "description": description,
        }

        return TestResult(**result_data)

