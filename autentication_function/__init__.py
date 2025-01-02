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
            "notificaciones": False,
        }
        self.mantener_sesion = mantener_sesion

def validar_contrasena(contrasena, nombre_usuario=None, apellido=None):
    min_length = 8
    max_length = 20

    # Validar longitud
    if len(contrasena) < min_length:
        raise ValueError(f"La contraseña debe tener al menos {min_length} caracteres.")
    if len(contrasena) > max_length:
        raise ValueError(f"La contraseña no puede tener más de {max_length} caracteres.")

    # Validar contenido prohibido
    if "password" in contrasena.lower() or "contraseña" in contrasena.lower():
        raise ValueError("La contraseña no puede contener 'password' o 'contraseña'.")
    if contrasena.isdigit():
        raise ValueError("La contraseña no puede ser solo números.")

    # Validar contenido obligatorio
    if not any(char.isdigit() for char in contrasena):
        raise ValueError("La contraseña debe contener al menos un número.")
    if not any(char.isupper() for char in contrasena):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
    if not any(char in "!@#$%^&*()_+-=[]{}|;:'\",.<>?/`~" for char in contrasena):
        raise ValueError("La contraseña debe contener al menos un carácter especial.")

    # Validar que no contenga el nombre o apellido
    if nombre_usuario and nombre_usuario.lower() in contrasena.lower():
        raise ValueError("La contraseña no puede contener el nombre del usuario.")
    if apellido and apellido.lower() in contrasena.lower():
        raise ValueError("La contraseña no puede contener el apellido del usuario.")

    return True

def iniciar_sesion(nombre_usuario, contrasena, mantener_sesion=False):
    """Permite a un usuario iniciar sesión si las credenciales son correctas."""
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

class UsuarioExtendido(Usuario):
    def __init__(self, nombre_usuario, contrasena, apellido, correo, permisos=None, mantener_sesion=False):
        super().__init__(nombre_usuario, contrasena, permisos, mantener_sesion)
        palabras_no_permitidas = ["ofensiva1", "ofensiva2"]
        if not nombre_usuario.strip():
            raise ValueError("El campo 'nombre_usuario' no puede estar vacío.")
        if any(palabra in nombre_usuario for palabra in palabras_no_permitidas):
            raise ValueError("El nombre de usuario contiene palabras ofensivas.")
        if not all(c.isalnum() or c.isspace() for c in nombre_usuario):
            raise ValueError("El nombre de usuario contiene caracteres no permitidos.")
        if not contrasena.strip():
            raise ValueError("El campo 'contraseña' no puede estar vacío.")
        if not apellido.strip():
            raise ValueError("El campo 'apellido' no puede estar vacío.")
        if not correo.strip():
            raise ValueError("El campo 'correo' no puede estar vacío.")
        self.apellido = apellido
        self.correo = correo

# Exportar funciones y clases
__all__ = [
    "Usuario",
    "UsuarioExtendido",
    "validar_contrasena",
    "iniciar_sesion",
    "asignar_permiso",
    "agregar_usuario",
    "verificar_usuario",
    "obtener_usuario",
]
