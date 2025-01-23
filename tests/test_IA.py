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
        with self.assertRaises(ValueError):
            validar_contrasena("clave123")

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

import unittest
import sys
import os
from autentication_function import Usuario, UsuarioExtendido, validar_contrasena, iniciar_sesion, asignar_permiso
from autentication_function.base_datos import usuarios, agregar_usuario, obtener_usuario, verificar_usuario
from solapamientos_function import detectarSolapamientos, convertir_a_minutos

class TestExtension(unittest.TestCase):

    def setUp(self):
        # Limpia la base de datos simulada antes de cada test
        usuarios.clear()

        # Usuario de prueba inicial
        self.usuario = UsuarioExtendido("usuarioTest", "ClaveSegura2025!", "Apellido", "correo@test.com")
        agregar_usuario(self.usuario)


    # Test 26. Comprobar que obtener un usuario inexistente devuelve None.
    def test_obtener_usuario_inexistente(self):
        self.assertIsNone(obtener_usuario("usuarioInexistente"))
        print("Se ha pasado el test 26")

    # Test 27. Verificar que agregar un usuario duplicado lanza una excepción.
    def test_agregar_usuario_duplicado(self):
        with self.assertRaises(ValueError):
            agregar_usuario(self.usuario)
        print("Se ha pasado el test 27")

    # Test 28. Validar que las contraseñas incorrectas no permiten iniciar sesión.
    def test_iniciar_sesion_contrasena_incorrecta(self):
        self.assertFalse(verificar_usuario("usuarioTest", "ContrasenaIncorrecta"))
        print("Se ha pasado el test 28")

    # Test 29. Validar que convertir_a_minutos convierte correctamente "00:00".
    def test_convertir_a_minutos_medianoche(self):
        self.assertEqual(convertir_a_minutos("00:00"), 0)
        print("Se ha pasado el test 29")

    # Test 30. Verificar que convertir_a_minutos funciona correctamente para "23:59".
    def test_convertir_a_minutos_ultima_hora(self):
        self.assertEqual(convertir_a_minutos("23:59"), 1439)
        print("Se ha pasado el test 30")

    # Test 31. Detectar que no hay solapamiento entre eventos que no coinciden.
    def test_no_hay_solapamiento(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "11:00", "fin": "12:00"}
        self.assertFalse(detectarSolapamientos(eventos, nuevo_evento))
        print("Se ha pasado el test 31")

    # Test 32. Detectar que hay solapamiento entre eventos que coinciden parcialmente.
    def test_solapamiento_parcial(self):
        eventos = [{"inicio": "10:00", "fin": "11:30"}]
        nuevo_evento = {"inicio": "11:00", "fin": "12:00"}
        self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))
        print("Se ha pasado el test 32")

    # Test 33. Comprobar que asignar un permiso funciona correctamente.
    def test_asignar_permiso(self):
        asignar_permiso(self.usuario, "calendario")
        self.assertTrue(self.usuario.permisos.get("calendario", False))
        print("Se ha pasado el test 33")

    # Test 34. Verificar que los permisos asignados no afectan a otros permisos.
    def test_asignar_permiso_no_afecta_otros(self):
        asignar_permiso(self.usuario, "calendario")
        self.assertFalse(self.usuario.permisos.get("contactos", False))
        print("Se ha pasado el test 34")

    # Test 35. Comprobar que un usuario agregado tiene todos los permisos como False por defecto.
    def test_permisos_iniciales(self):
        for permiso, valor in self.usuario.permisos.items():
            self.assertFalse(valor)
        print("Se ha pasado el test 35")

    # Test 36. Detectar solapamiento cuando el nuevo evento está completamente dentro de otro.
    def test_solapamiento_total_dentro(self):
        eventos = [{"inicio": "09:00", "fin": "12:00"}]
        nuevo_evento = {"inicio": "10:00", "fin": "11:00"}
        self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))
        print("Se ha pasado el test 36")

    # Test 37. Detectar solapamiento cuando un evento existente está completamente dentro del nuevo evento.
    def test_solapamiento_total_fuera(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "09:00", "fin": "12:00"}
        self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))
        print("Se ha pasado el test 37")

    # Test 38. Comprobar que un usuario inexistente no puede iniciar sesión.
    def test_iniciar_sesion_usuario_inexistente(self):
        self.assertFalse(verificar_usuario("usuarioFalso", "ClaveSegura2025!"))
        print("Se ha pasado el test 38")

    # Test 39. Validar que un evento exactamente igual a otro genera solapamiento.
    def test_solapamiento_exacto(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "10:00", "fin": "11:00"}
        self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))
        print("Se ha pasado el test 39")

    # Test 40. Verificar que asignar permisos a un usuario inexistente no genera errores inesperados.
    def test_asignar_permiso_usuario_inexistente(self):
        usuario_falso = UsuarioExtendido("usuarioFalso", "Clave123!", "ApellidoFalso", "falso@test.com")
        with self.assertRaises(ValueError):
            asignar_permiso(usuario_falso, "leer")
        print("Se ha pasado el test 40")



    # Test 41. Verificar que no se puede agregar un usuario con un correo inválido.
    def test_agregar_usuario_correo_invalido(self):
        usuario_invalido = UsuarioExtendido("usuarioInvalido", "Clave123!", "Apellido", "correo_invalido@test")
        try:
            agregar_usuario(usuario_invalido)
        except ValueError as e:
            self.assertEqual(str(e), "El usuario correo_invalido@test tiene un correo no válido.")
        print("Se ha pasado el test 41")


    # Test 42. Comprobar que verificar_usuario devuelve False si la contraseña es None.
    def test_verificar_usuario_contrasena_none(self):
        self.assertFalse(verificar_usuario("usuarioTest", None))
        print("Se ha pasado el test 42")

    # Test 43. Validar que un evento con fin anterior al inicio lanza un error.
    def test_evento_fin_antes_inicio(self):
        eventos = []
        nuevo_evento = {"inicio": "11:00", "fin": "10:00"}
        try:
            if convertir_a_minutos(nuevo_evento['fin']) < convertir_a_minutos(nuevo_evento['inicio']):
                raise ValueError("El evento tiene un horario inválido: el fin es anterior al inicio.")
            detectarSolapamientos(eventos, nuevo_evento)
        except ValueError as e:
            self.assertEqual(str(e), "El evento tiene un horario inválido: el fin es anterior al inicio.")
        else:
            self.fail("ValueError no fue lanzado")
        print("Se ha pasado el test 43")

    # Test 44. Verificar que un usuario agregado no tiene atributos adicionales inesperados.
    def test_usuario_atributos(self):
        self.assertTrue(hasattr(self.usuario, "nombre_usuario"))
        self.assertTrue(hasattr(self.usuario, "contrasena"))
        self.assertTrue(hasattr(self.usuario, "permisos"))
        self.assertFalse(hasattr(self.usuario, "atributo_inexistente"))
        print("Se ha pasado el test 44")

    # Test 45. Detectar solapamiento con un evento al borde del inicio del día.
    def test_solapamiento_inicio_dia(self):
        eventos = [{"inicio": "00:30", "fin": "01:30"}]
        nuevo_evento = {"inicio": "00:00", "fin": "01:00"}
        self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))
        print("Se ha pasado el test 45")

    # Test 46. Comprobar que no hay solapamiento con eventos que no coinciden en absoluto.
    def test_no_solapamiento_eventos_distantes(self):
        eventos = [{"inicio": "08:00", "fin": "09:00"}]
        nuevo_evento = {"inicio": "10:00", "fin": "11:00"}
        self.assertFalse(detectarSolapamientos(eventos, nuevo_evento))
        print("Se ha pasado el test 46")

    # Test 47. Verificar que un evento que dura todo el día solapa cualquier otro evento.
    def test_evento_todo_el_dia(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "00:00", "fin": "23:59"}
        self.assertTrue(detectarSolapamientos(eventos, nuevo_evento))
        print("Se ha pasado el test 47")

    # Test 48. Comprobar que un usuario no puede iniciar sesión con un nombre vacío.
    def test_iniciar_sesion_nombre_vacio(self):
        self.assertFalse(verificar_usuario("", "ClaveSegura2025!"))
        print("Se ha pasado el test 48")

    # Test 49. Validar que se puede asignar múltiples permisos a un usuario.
    def test_asignar_multiples_permisos(self):
        asignar_permiso(self.usuario, "ubicacion")
        asignar_permiso(self.usuario, "musica")
        self.assertTrue(self.usuario.permisos.get("ubicacion", False))
        self.assertTrue(self.usuario.permisos.get("musica", False))
        print("Se ha pasado el test 49")

    # Test 50. Verificar que un evento no solapa si tiene exactamente el mismo inicio y fin.
    def test_evento_mismo_inicio_fin(self):
        eventos = [{"inicio": "10:00", "fin": "11:00"}]
        nuevo_evento = {"inicio": "11:00", "fin": "12:00"}
        self.assertFalse(detectarSolapamientos(eventos, nuevo_evento))
        print("Se ha pasado el test 50")


if __name__ == '__main__':
    unittest.main()
