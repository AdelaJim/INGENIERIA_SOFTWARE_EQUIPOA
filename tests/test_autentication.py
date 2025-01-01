import unittest
import sys
import os

# Agregar la ruta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autentication_function import UsuarioExtendido, validar_contrasena, agregar_usuario
from autentication_function.base_datos import usuarios

class TestAutenticacion(unittest.TestCase):
    def setUp(self):
        # Limpia la base de datos simulada antes de cada test
        usuarios.clear()

        # Configuración inicial del usuario de prueba
        self.nombre = "nombreusuario1"
        self.apellido = "apellidousuario1"
        self.contrasena = "claveSegura2024"
        self.correo = "usuario1@gmail.com"
        self.usuario = UsuarioExtendido(self.nombre, self.contrasena, self.apellido, self.correo)
        agregar_usuario(self.usuario)

#1. Verificar que, al crear un usuario, el nombre y apellidos se han introducido correctamente
    def test_crear_usuario_nombre_apellido(self):
        nuevo_usuario = UsuarioExtendido(f"{self.nombre} {self.apellido}", self.contrasena, self.apellido, self.correo)
        self.assertEqual(nuevo_usuario.nombre_usuario, f"{self.nombre} {self.apellido}")
        print("Se ha pasado el test 1")

#2. Verificar que, al crear un usuario, el nombre de usuario elegido no está repetido con la base de datos
    def test_nombre_usuario_no_repetido(self):
        # Intentar registrar un usuario con un nombre que ya existe
        nuevo_usuario = UsuarioExtendido(f"{self.nombre} {self.apellido}", self.contrasena, self.apellido, self.correo)
        if nuevo_usuario.nombre_usuario == "nombreusuario1":
            print("Error: nombre de usuario repetido.")

        usuario_unico = UsuarioExtendido("usuariounico", "claveDiferente2024", "Apellido", "correo_unico@gmail.com")
        agregar_usuario(usuario_unico)
        self.assertIn(usuario_unico, usuarios)
        print("Se ha pasado el test 2")

#3. Verificar que, al crear un usuario, ningún campo de datos personales esté vacío.
    def test_todos_los_campos_obligatorios_completos(self):
        with self.assertRaises(ValueError):
            UsuarioExtendido("", self.contrasena, self.apellido, self.correo)
        print("Error: campo 'nombre' vacío.")

        with self.assertRaises(ValueError):
            UsuarioExtendido(self.nombre, "", self.apellido, self.correo)
        print("Error: campo 'contraseña' vacío.")

        with self.assertRaises(ValueError):
            UsuarioExtendido(self.nombre, self.contrasena, "", self.correo)
        print("Error: campo 'apellido' vacío.")

        with self.assertRaises(ValueError):
            UsuarioExtendido(self.nombre, self.contrasena, self.apellido, "")
        print("Error: campo 'correo' vacío.")

        self.assertEqual(self.usuario.nombre_usuario, self.nombre)
        self.assertEqual(self.usuario.contrasena, self.contrasena)
        self.assertEqual(self.usuario.apellido, self.apellido)
        self.assertEqual(self.usuario.correo, self.correo)
        print("Se ha pasado el test 3")

#4. Verificar la longitud del nombre de usuario al crear un nuevo usuario.
    def test_nombre_usuario_longitud_valida(self):
        self.min_longitud = 3
        self.max_longitud = 20
        nombre_valido = "UsuarioValido"
        usuario = UsuarioExtendido(nombre_valido, self.contrasena, self.apellido, self.correo)
        self.assertGreaterEqual(len(usuario.nombre_usuario), self.min_longitud)
        self.assertLessEqual(len(usuario.nombre_usuario), self.max_longitud)
        print("Se ha pasado el test 4")

#5. Verificar que, al crear un usuario, el nombre de usuario no contenga caracteres raros ni palabras ofensivas.
    def test_nombre_usuario_valido(self):
        palabras_no_permitidas = ["ofensiva1", "ofensiva2", "123$", "@nombre", ""]
        usuario = UsuarioExtendido("NombreValido", self.contrasena, self.apellido, self.correo)
        self.assertNotIn(usuario.nombre_usuario, palabras_no_permitidas)
        self.assertTrue(usuario.nombre_usuario.isalnum())
        print("Se ha pasado el test 5")

        nombre_invalido = "@nombre"
        with self.assertRaises(ValueError):
            UsuarioExtendido(nombre_invalido, self.contrasena, self.apellido, self.correo)
        print("Error: nombre con caracteres extraños.")

        nombre_ofensivo = "ofensiva1"
        with self.assertRaises(ValueError):
            UsuarioExtendido(nombre_ofensivo, self.contrasena, self.apellido, self.correo)
        print("Error: palabra ofensiva en el nombre de usuario.")

# Test 6: Verificar longitud mínima y máxima de contraseñas
    def test_password_length(self):
        contrasena_corta = "Short1!"
        contrasena_larga = "a" * 21
        contrasena_valida = "Valid2024!"

        with self.assertRaises(ValueError):
            validar_contrasena(contrasena_corta)
        with self.assertRaises(ValueError):
            validar_contrasena(contrasena_larga)
        self.assertTrue(validar_contrasena(contrasena_valida))
        print("Se ha pasado el test 6")

    # Test 7: Verificar que se pueda registrar un perfil adulto
    def test_adult_profile(self):
        usuario_adulto = UsuarioExtendido("AdultUser", "Secure2024!", "LastName", "adult.user@gmail.com")
        agregar_usuario(usuario_adulto)
        self.assertIn(usuario_adulto, usuarios)
        print("Se ha pasado el test 7")

    # Test 8: Verificar que un perfil infantil esté vinculado a un adulto
    def test_child_profile_linked_to_adult(self):
        adulto = UsuarioExtendido("AdultUser", "Secure2024!", "LastName", "adult.user@gmail.com")
        agregar_usuario(adulto)

        infantil = UsuarioExtendido("ChildUser", "ChildSecure2024!", "ChildLastName", "child.user@gmail.com")
        infantil.vinculado_a = adulto.nombre_usuario
        self.assertEqual(infantil.vinculado_a, adulto.nombre_usuario)
        print("Se ha pasado el test 8")

    # Test 9: Verificar que las contraseñas incluyan caracteres especiales, mayúsculas y números
    def test_password_complexity(self):
        contrasena_simple = "password"
        contrasena_valida = "Valid2024!"

        with self.assertRaises(ValueError):
            validar_contrasena(contrasena_simple)
        self.assertTrue(validar_contrasena(contrasena_valida))
        print("Se ha pasado el test 9")

    # Test 10: Verificar que las contraseñas no incluyan el nombre o apellido del usuario
    def test_password_no_name_or_surname(self):
        contrasena_con_nombre = "John123!"
        contrasena_con_apellido = "Doe2024!"
        contrasena_valida = "Valid2024!"

        with self.assertRaises(ValueError):
            validar_contrasena(contrasena_con_nombre, nombre_usuario="John", apellido="Doe")
        with self.assertRaises(ValueError):
            validar_contrasena(contrasena_con_apellido, nombre_usuario="John", apellido="Doe")
        self.assertTrue(validar_contrasena(contrasena_valida, nombre_usuario="John", apellido="Doe"))
        print("Se ha pasado el test 10")

#11. Verificar que la contraseña cumpla con las restricciones: no contener la palabara contraseña o password, no ser una sucesión de números.
    def test_validar_contrasena(self):
        with self.assertRaises(ValueError):
            validar_contrasena("password")
        with self.assertRaises(ValueError):
            validar_contrasena("contraseña")
        with self.assertRaises(ValueError):
            validar_contrasena("12345678")
        self.assertTrue(validar_contrasena("claveSegura2024"))
        print("Se ha pasado el test 11")

#13. Verificar que se pueda mantener la sesión iniciada.
    def test_mantener_sesion_iniciada(self):
        self.usuario.mantener_sesion = True
        self.assertTrue(self.usuario.mantener_sesion)
        print("Se ha pasado el test 13")

#14. Verificar que se pueda iniciar sesión con un usuario y contraseña existentes.
    def test_iniciar_sesion(self):
        self.assertTrue(iniciar_sesion(self.nombre, self.contrasena))
        with self.assertRaises(ValueError):
            iniciar_sesion(self.nombre, "claveIncorrecta")
        print("Se ha pasado el test 14")



if __name__ == '__main__':
    unittest.main()