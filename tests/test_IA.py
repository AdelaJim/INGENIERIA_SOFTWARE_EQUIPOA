"""
 import unittest
 import sys
 import os

 # Agregar la ruta raíz del proyecto al PYTHONPATH
 sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

 from autentication_function import Usuario, UsuarioExtendido, validar_contrasena, iniciar_sesion, asignar_permiso
 from autentication_function.base_datos import usuarios, agregar_usuario, verificar_usuario
 from solapamientos_function import detectarSolapamientos

 class TestAutenticacionYEventos(unittest.TestCase):

     def setUp(self):
         # Limpia la base de datos simulada antes de cada test
         usuarios.clear()

         # Configuración inicial de un usuario de prueba
         self.usuario = UsuarioExtendido("usuarioPrueba", "ClaveSegura1234!", "ApellidoPrueba", "correo@prueba.com")
         agregar_usuario(self.usuario)

     # Test 26: Verificar agregar usuario duplicado lanza error
     def test_agregar_usuario_duplicado(self):
         with self.assertRaises(ValueError):
             agregar_usuario(self.usuario)

     # Test 27: Validar contraseña correcta
     def test_validar_contrasena_correcta(self):
         self.assertTrue(validar_contrasena("ClaveSegura1234!"))

     # Test 28: Validar contraseña incorrecta
     def test_validar_contrasena_incorrecta(self):
         self.assertFalse(validar_contrasena("clave123"))

     # Test 29: Iniciar sesión con credenciales válidas
     def test_iniciar_sesion_valido(self):
         self.assertTrue(verificar_usuario("usuarioPrueba", "ClaveSegura1234!"))

     # Test 30: Iniciar sesión con credenciales inválidas
     def test_iniciar_sesion_invalido(self):
         self.assertFalse(verificar_usuario("usuarioPrueba", "ClaveIncorrecta"))

     # Test 31: Asignar permiso a usuario existente
     def test_asignar_permiso(self):
         asignar_permiso(self.usuario, "admin")
         self.assertIn("admin", self.usuario.permisos)

     # Test 32: Detectar solapamiento básico entre dos eventos
     def test_detectar_solapamiento_basico(self):
         eventos = [{"inicio": "10:00", "fin": "11:00"}]
         nuevo_evento = {"inicio": "10:30", "fin": "11:30"}
         self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))

     # Test 33: No detectar solapamiento entre eventos no coincidentes
     def test_no_detectar_solapamiento(self):
         eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "11:30", "fin": "12:30"}
         self.assertFalse(detectarSolapamientos(eventos, nuevo_evento))

     # Test 34: Detectar solapamiento exacto
     def test_detectar_solapamiento_exacto(self):
         eventos = [{"inicio": "10:00", "fin": "11:00"}]
         nuevo_evento = {"inicio": "10:00", "fin": "11:00"}
         self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))

     # Test 35: Detectar solapamiento cuando un evento contiene otro
     def test_detectar_solapamiento_contenido(self):
         eventos = [{"inicio": "10:00", "fin": "12:00"}]
         nuevo_evento = {"inicio": "10:30", "fin": "11:30"}
         self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))

     # Test 36: Detectar solapamiento en límites exactos
     def test_detectar_solapamiento_limites(self):
         eventos = [{"inicio": "10:00", "fin": "11:00"}]
         nuevo_evento = {"inicio": "11:00", "fin": "12:00"}
         self.assertFalse(detectarSolapamientos(eventos, nuevo_evento))

     # Test 37: Convertir hora a minutos correctamente
     def test_convertir_a_minutos(self):
         from solapamientos_function import convertir_a_minutos
         self.assertEqual(convertir_a_minutos("02:30"), 150)

     # Test 38: Detectar múltiples solapamientos
     def test_detectar_multiples_solapamientos(self):
         eventos = [
             {"inicio": "09:00", "fin": "10:00"},
             {"inicio": "10:30", "fin": "11:30"}
         ]
         nuevo_evento = {"inicio": "10:00", "fin": "11:00"}
         self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))

     # Test 39: Usuario no existente al verificar credenciales
     def test_verificar_usuario_no_existente(self):
         self.assertFalse(verificar_usuario("noExiste", "clave"))

     # Test 40: Comprobar permisos asignados correctamente
     def test_comprobar_permisos_asignados(self):
         asignar_permiso(self.usuario, "editor")
         self.assertIn("editor", self.usuario.permisos)

 if __name__ == '__main__':
     unittest.main()
 """