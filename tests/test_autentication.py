import unittest
from autentication_function import Usuario, UsuarioExtendido, validar_contrasena, iniciar_sesion
from autentication_function.base_datos import agregar_usuario, usuarios, limpiar_usuarios

class TestAutenticacion(unittest.TestCase):
# Crear un usuario de prueba 
    def setUp(self):
        limpiar_usuarios
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