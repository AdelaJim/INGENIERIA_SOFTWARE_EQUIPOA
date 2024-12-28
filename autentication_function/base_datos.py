# Lista que actúa como base de datos
usuarios = []


def agregar_usuario(usuario):
    usuarios.append(usuario)
    #print(f"Usuario {usuario.nombre_usuario} agregado con éxito.")

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

