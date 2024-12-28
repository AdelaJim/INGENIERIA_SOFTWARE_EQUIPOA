
# La función de autenticación permite a los usuarios iniciar sesión, asignar permisos y mantener la sesión iniciada.

from autentication_function.base_datos import usuarios, agregar_usuario, verificar_usuario, obtener_usuario

class Usuario:
    def __init__(self, nombre_usuario, contrasena, permisos=None, mantener_sesion=False):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.permisos = permisos or {
            "ubicacion": False,
            "musica": False,
            "calendario": False,
            "contactos": False,
            "notificaciones": False
        }
        self.mantener_sesion = mantener_sesion

def validar_contrasena(contrasena):
    if "password" in contrasena.lower() or "contraseña" in contrasena.lower():
        raise ValueError("La contraseña no puede contener 'password' o 'contraseña'.")
    if contrasena.isdigit():
        raise ValueError("La contraseña no puede ser una sucesión de números.")
    return True

def iniciar_sesion(nombre_usuario, contrasena, mantener_sesion=False):
    if verificar_usuario(nombre_usuario, contrasena):
        usuario = obtener_usuario(nombre_usuario)
        usuario.mantener_sesion = mantener_sesion
        return True
    raise ValueError("Usuario o contraseña incorrectos.")

def asignar_permiso(usuario, permiso, valor=True):
    if permiso in usuario.permisos:
        usuario.permisos[permiso] = valor
        return True
    else:
        raise ValueError("Permiso no válido.")
    

if __name__ == '__main__':
    usuario = Usuario("usuario1", "claveSegura2024")
    agregar_usuario(usuario)
    
