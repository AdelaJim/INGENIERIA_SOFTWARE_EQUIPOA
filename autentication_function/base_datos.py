# Lista que actúa como base de datos
usuarios = []


def agregar_usuario(usuario):
    if any(u.nombre_usuario == usuario.nombre_usuario for u in usuarios):
        raise ValueError(f"El usuario {usuario.nombre_usuario} ya existe.")
    usuarios.append(usuario)


def obtener_usuario(nombre_usuario):
    for usuario in usuarios:
        if usuario.nombre_usuario == nombre_usuario:
            return usuario
    return None


def verificar_usuario(nombre_usuario, contrasena):
    usuario = obtener_usuario(nombre_usuario)
    if usuario and usuario.contrasena == contrasena:
        return True
    return False
