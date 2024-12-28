import unittest
from autentication_function import Usuario, asignar_permiso

class TestPermisos(unittest.TestCase):
# Crear un usuario de prueba 
    def setUp(self):
        self.usuario = Usuario("usuario_prueba", "claveSegura123")
    
# 12. Comprobar que los permisos por defecto son 'sin permisos'.
    def test_permisos_por_defecto(self):
        for permiso, valor in self.usuario.permisos.items():
            self.assertFalse(valor)
        #print("se ha pasado el test 12")

# 15. Verificar que se puedan asignar permisos a ubicación, música, calendario, etc.
    def test_asignar_permisos(self):
        asignar_permiso(self.usuario, "ubicacion", True)
        asignar_permiso(self.usuario, "musica", True)
        self.assertTrue(self.usuario.permisos["ubicacion"])
        self.assertTrue(self.usuario.permisos["musica"])

        with self.assertRaises(ValueError):
            asignar_permiso(self.usuario, "permiso_invalido", True)
        #print("se ha pasado el test 15")

if __name__ == '__main__':
    unittest.main()