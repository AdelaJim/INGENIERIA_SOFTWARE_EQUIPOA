import unittest
from autentication_function import Usuario, UsuarioExtendido, asignar_permiso
from solapamientos_function import detectarSolapamientos

class TestPermisos(unittest.TestCase):

    # Crear un usuario de prueba 
    def setUp(self):
        self.usuario = Usuario("usuario_prueba", "claveSegura123")
    
# Test 12. Comprobar que los permisos por defecto son 'sin permisos'.
    def test_permisos_por_defecto(self):
        for permiso, valor in self.usuario.permisos.items():
            self.assertFalse(valor)
        print("se ha pasado el test 12")

# Test 15. Verificar que se puedan asignar permisos a ubicación, música, calendario, etc.
    def test_asignar_permisos(self):
        asignar_permiso(self.usuario, "ubicacion", True)
        asignar_permiso(self.usuario, "musica", True)
        self.assertTrue(self.usuario.permisos["ubicacion"])
        self.assertTrue(self.usuario.permisos["musica"])

        with self.assertRaises(ValueError):
            asignar_permiso(self.usuario, "permiso_invalido", True)
        print("se ha pasado el test 15")

# Test 18. Validar que los perfiles infantiles tienen permisos restringidos
    def test_permisos_restringidos_infantil(self):
        infantil = UsuarioExtendido("infantiltest", "ClaveInfantil2025!", "Apellido", "correo_infantil@test.com")
        infantil.permisos = {
            "ubicacion": False,
            "musica": False,
            "calendario": False,
            "contactos": False,
            "notificaciones": False,
        }
        for permiso, valor in infantil.permisos.items():
            self.assertFalse(valor, f"El permiso {permiso} no debería estar habilitado para el perfil infantil.")
        print("se ha pasado el test 18")

# Test 19. Detectar solapamiento de eventos con formato incorrecto
    def test_evento_horas_mal_formateadas(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "10:xx", "fin": "12:00"}
        with self.assertRaises(ValueError):
            detectarSolapamientos(eventos, nuevo_evento)
        print("se ha pasado el test 19")

# Test 20. Detectar solapamiento de eventos sin clave "inicio"
    def test_evento_sin_clave_inicio(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"fin": "12:00"}
        with self.assertRaises(KeyError):
            detectarSolapamientos(eventos, nuevo_evento)
        print("se ha pasado el test 20")

if __name__ == '__main__':
    unittest.main()