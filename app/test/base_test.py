from app.schema.security_test_schema import SecurityTestResult
from six import with_metaclass

class TestResult(SecurityTestResult):
    # Puedes agregar campos adicionales específicos de esta prueba si es necesario
    pass


class BaseTestMeta(type):
    """ Metaclass that collects class names into `BaseTest.test_classes` dict.

        To define more classes, just subclass `BaseTest`.
        If class name starts with `_`, it's ignored.
    """ 
    def __new__(cls, name, bases, attrs):
        is_base = 'test_classes' in attrs
        test_classes = attrs['test_classes'] if is_base else BaseTest.test_classes

        cls = super(BaseTestMeta, cls).__new__(cls, name, bases, attrs)
        if not is_base and not name.startswith('_'):
            test_classes[name] = cls

        return cls

class BaseTest(with_metaclass(BaseTestMeta, object)):
    """ Clase base para las pruebas de seguridad.

        Para crear una prueba personalizada, simplemente hereda de ella e implementa los siguientes métodos:

        * __init__() que toma los argumentos de configuración
        * run() que ejecuta la prueba de seguridad y retorna un objeto TestResult
    """
    # Mapa de clases de prueba: { nombre : clase }
    test_classes = {}

    def __init__(self, *args):
        self.args = args  # Store args

    @classmethod
    def name(cls):
        """ Obtener el nombre de la prueba de seguridad. """
        return cls.__name__()
    
    def info(self):
        """ Obtener información sobre la prueba de seguridad. """
        raise NotImplementedError
    
    def run(self, connection_params):
        """ Ejecutar la prueba de seguridad.
        
        
        :param connection_params: Parámetros de conexión a la base de datos
        :type connection_params: dict
        :return: Resultado de la prueba
        :rtype: dict
        """
        raise NotImplementedError

def __repr__(self):
        return '{cls}({args})'.format(cls=self.__class__.__name__, args=', '.join(map(str, self.args)))


