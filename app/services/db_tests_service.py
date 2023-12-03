import re
import markdown
import time  # Necesario para simular un retraso durante la ejecución


class DBTestService:
    available_tests = ["password_strength_test"]

    def check_password_strength(self, password):
        """
        Verifica la fortaleza de una contraseña según criterios específicos.
        Devuelve un valor entre 0 y 1, donde 0 significa débil y 1 significa fuerte.
        """
        # Ejemplo de criterios: al menos una mayúscula, una minúscula, un número y un carácter especial
        uppercase_regex = re.compile(r"[A-Z]")
        lowercase_regex = re.compile(r"[a-z]")
        digit_regex = re.compile(r"\d")
        special_char_regex = re.compile(r"[!@#$%^&*(),.?\":{}|<>]")

        strength = 0

        if uppercase_regex.search(password):
            strength += 0.25
        if lowercase_regex.search(password):
            strength += 0.25
        if digit_regex.search(password):
            strength += 0.25
        if special_char_regex.search(password):
            strength += 0.25

        # Asegura una longitud mínima de 8 caracteres
        if len(password) >= 8:
            strength += 0.25

        return min(1, strength)

    def run_test(self, test_name, password):
        if test_name in self.available_tests:
            try:
                # Simulamos un retraso de 3 segundos para simular una prueba en progreso
                time.sleep(3)

                # Intenta ejecutar la prueba
                strength = self.check_password_strength(password)

                # Construye la información detallada en formato Markdown
                execution_info = f"# Resultado de la Prueba: success\n\n"
                execution_info += f"## Detalles de la Ejecución:\n"
                execution_info += f"- **Fortaleza de la Contraseña:** {strength}\n"
                execution_info += f"- Otros detalles relevantes...\n"

                return "success", markdown.markdown(execution_info)
            except Exception as e:
                # Manejo de errores durante la ejecución de la prueba
                error_detail = str(e)
                execution_info = f"# Resultado de la Prueba: error\n\n"
                execution_info += f"## Detalles del Error:\n"
                execution_info += f"- **Mensaje de Error:** {error_detail}\n"

                return "error", markdown.markdown(execution_info)
        else:
            return "error", f"Prueba '{test_name}' no encontrada"


db_test_service = DBTestService()
