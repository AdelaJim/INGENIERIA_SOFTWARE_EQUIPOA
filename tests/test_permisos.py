import unittest
from autentication_function import Usuario, UsuarioExtendido, validar_contrasena, iniciar_sesion, asignar_permiso
from autentication_function.base_datos import usuarios, agregar_usuario
from solapamientos_function import detectarSolapamientos

class TestExtension(unittest.TestCase):

    def setUp(self):
        # Limpia la base de datos simulada antes de cada test
        usuarios.clear()

        # Usuario de prueba inicial
        self.usuario = UsuarioExtendido("usuarioTest", "ClaveSegura2025!", "Apellido", "correo@test.com")
        agregar_usuario(self.usuario)


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

# Test 19: Evento nuevo antes + después de todos los eventos existentes (sin solapamiento)
    def test_evento_sin_solapamiento(self):
        eventos = [{"inicio": "10:00", "fin": "12:00"}]
        nuevo_evento = {"inicio": "12:30", "fin": "13:30"}
        solapamiento = detectarSolapamientos(eventos, nuevo_evento)
        self.assertFalse(solapamiento)
        print("Se ha pasado el test 19")

# Test 20: Evento nuevo que empieza y termina dentro de un evento existente
    def test_evento_dentro_de_existente(self):
        eventos = [{"inicio": "10:00", "fin": "12:00"}]
        nuevo_evento = {"inicio": "10:30", "fin": "11:30"}
        solapamiento = detectarSolapamientos(eventos, nuevo_evento)
        self.assertTrue(solapamiento)
        print("Se ha pasado el test 20")

# Test 21: Evento nuevo que es igual a un evento existente (total solapamiento)
    def test_evento_solapamiento_total(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "10:00", "fin": "11:00"}
        solapamiento = detectarSolapamientos(eventos, nuevo_evento)
        self.assertTrue(solapamiento)
        print("Se ha pasado el test 21")

# Test 22: Evento nuevo con horas mal formateadas (prueba de validación)
    def test_evento_horas_mal_formateadas(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "10:xx", "fin": "12:00"}
        with self.assertRaises(ValueError):
            detectarSolapamientos(eventos, nuevo_evento)
        print("Se ha pasado el test 22")

# Test 23: Evento nuevo sin clave "fin" (prueba de errores)
    def test_evento_sin_clave_fin(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "10:00"}
        with self.assertRaises(KeyError):
            detectarSolapamientos(eventos, nuevo_evento)
        print("Se ha pasado el test 23")

# Test 24: Evento nuevo sin clave "inicio" (prueba de errores)
    def test_evento_sin_clave_inicio(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"fin": "11:00"}
        with self.assertRaises(KeyError):
            detectarSolapamientos(eventos, nuevo_evento)
        print("Se ha pasado el test 24")

# Test 25: En caso de solapamiento, envía un mensaje
    def test_mensaje_en_caso_de_solapamiento(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "10:30", "fin": "11:30"}
        with self.assertLogs('solapamientos_function', level='WARNING') as log:
            detectarSolapamientos(eventos, nuevo_evento)
            self.assertIn("Solapamiento detectado", log.output[0])
        print("Se ha pasado el test 25")


if __name__ == '__main__':
    unittest.main()