import unittest
from autentication_function import Usuario, validar_contrasena, iniciar_sesion
from autentication_function.base_datos import agregar_usuario, usuarios

class TestAutenticacion(unittest.TestCase):
# Crear un usuario de prueba 
    def setUp(self):
        self.usuario_adulto = Usuario("usuario1", "claveSegura2024")
        agregar_usuario(self.usuario_adulto)

#11. Verificar que la contraseña cumpla con las restricciones: no contener la palabara contraseña o password, no ser una sucesión de números.
    def test_validar_contrasena(self):
        with self.assertRaises(ValueError):
            validar_contrasena("password")
        with self.assertRaises(ValueError):
            validar_contrasena("contraseña")
        with self.assertRaises(ValueError):
            validar_contrasena("12345678")
        self.assertTrue(validar_contrasena("claveSegura2024"))
        #print("se ha pasado el test 11")

#13. Verificar que se pueda mantener la sesión iniciada.
    def test_mantener_sesion_iniciada(self):
        self.usuario_adulto.mantener_sesion = True
        self.assertTrue(self.usuario_adulto.mantener_sesion)
        #print("se ha pasado el test 13")

#14. Verificar que se pueda iniciar sesión con un usuario y contraseña existentes.
    def test_iniciar_sesion(self):
        self.assertTrue(iniciar_sesion("usuario1", "claveSegura2024"))
        with self.assertRaises(ValueError):
            iniciar_sesion("usuario1", "claveIncorrecta")
        #print("se ha pasado el test 14")



if __name__ == '__main__':
    unittest.main()