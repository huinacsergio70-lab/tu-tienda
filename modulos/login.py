"""
Modulo: login.py
Descripcion: Autenticacion de usuarios con roles diferenciados (admin / cajero).
             Admin tiene acceso completo. Cajero solo puede hacer ventas y reportes basicos.
Autores: [Tu nombre] / [Nombre companero]
Fecha: 2026
"""

import os
from modulos.archivos import leer_json, escribir_json
from modulos.utilidades import limpiar_pantalla, separador, pausar

ARCHIVO = 'usuarios'

USUARIOS_DEFAULT = [
    {"usuario": "admin",  "password": "admin123",  "rol": "admin",  "nombre": "Administrador"},
    {"usuario": "cajero", "password": "cajero123", "rol": "cajero", "nombre": "Cajero"}
]

BANNER_LOGIN = """
  +--------------------------------------------------+
  |                                                  |
  |        SISTEMA POS  --  TU TIENDA                |
  |            Con carino para Dona Marta            |
  |                                                  |
  +--------------------------------------------------+
"""


def cargar_usuarios():
    """
    Carga usuarios desde JSON. Si no existe, crea el archivo con usuarios por defecto.
    Devuelve: lista de usuarios.
    """
    usuarios = leer_json(ARCHIVO)
    if not usuarios:
        escribir_json(ARCHIVO, USUARIOS_DEFAULT)
        return USUARIOS_DEFAULT
    return usuarios


def verificar_credenciales(usuario_input, password_input):
    """
    Verifica usuario y contrasena contra el archivo de usuarios.
    Recibe: usuario_input (str), password_input (str).
    Devuelve: dict del usuario si es valido, None si falla.
    """
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u['usuario'] == usuario_input and u['password'] == password_input:
            return u
    return None


def mostrar_pantalla_login():
    """
    Muestra la pantalla de login y gestiona intentos.
    Devuelve: dict del usuario autenticado, o termina el programa si se agotan los intentos.
    """
    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:
        limpiar_pantalla()
        print(BANNER_LOGIN)
        separador('=')
        print("  INICIAR SESION")
        separador('=')

        if intentos > 0:
            restantes = max_intentos - intentos
            print(f"  [!] Intentos restantes: {restantes}\n")

        usuario = input("  Usuario: ").strip()
        password = input("  Contrasena: ").strip()

        usuario_valido = verificar_credenciales(usuario, password)

        if usuario_valido:
            limpiar_pantalla()
            print(BANNER_LOGIN)
            print(f"  Bienvenido, {usuario_valido['nombre']}!")
            print(f"  Rol activo: {usuario_valido['rol'].upper()}")
            separador()
            pausar()
            return usuario_valido

        intentos += 1
        print(f"\n  [!] Usuario o contrasena incorrectos.")
        pausar()

    limpiar_pantalla()
    print("\n  Demasiados intentos fallidos. El sistema se ha cerrado.\n")
    import sys
    sys.exit(1)


def tiene_permiso(sesion, permiso):
    """
    Verifica si el usuario en sesion tiene permiso para una accion.
    Recibe: sesion (dict del usuario), permiso (str).
    Devuelve: True si tiene permiso, False si no.
    """
    if sesion['rol'] == 'admin':
        return True
    permisos_cajero = {'ventas', 'reporte_dia', 'reporte_stock_bajo'}
    return permiso in permisos_cajero


def mostrar_usuario_activo(sesion):
    """
    Muestra en consola el usuario y rol activo.
    Recibe: sesion (dict).
    """
    print(f"  Usuario: {sesion['nombre']}  |  Rol: {sesion['rol'].upper()}")