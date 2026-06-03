"""
Modulo: main.py
Descripcion: Punto de entrada del sistema POS Tu Tienda.
             Inicializa directorios, gestiona login y muestra el menu segun rol.
Autores: [Tu nombre] / [Nombre companero]
Fecha: 2026
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modulos.archivos import asegurar_directorios
from modulos.utilidades import separador, limpiar_pantalla, pausar
from modulos.login import mostrar_pantalla_login, tiene_permiso, mostrar_usuario_activo
from modulos.ventas import cargar_ventas, menu_ventas
from modulos.productos import menu_productos
from modulos.clientes import menu_clientes
from modulos.reportes import menu_reportes

BANNER = """
--------------------------------------------------
            TU TIENDA               
            Dona Marta            
--------------------------------------------------                                          
"""


def menu_principal(sesion):
    """
    Muestra el menu principal segun el rol del usuario en sesion.
    Admin ve todo. Cajero solo ve Ventas y reportes basicos.
    Recibe: sesion (dict) con datos del usuario autenticado.
    """
    es_admin = sesion['rol'] == 'admin'

    while True:
        limpiar_pantalla()
        print(BANNER)
        separador('=')
        mostrar_usuario_activo(sesion)
        separador('=')
        print("  MENU PRINCIPAL\n")

        indices = {}
        num = 1

        if es_admin:
            print(f"  {num}. Productos (Inventario)")
            indices[num] = 'productos'
            num += 1
            print(f"  {num}. Clientes")
            indices[num] = 'clientes'
            num += 1

        print(f"  {num}. Ventas")
        indices[num] = 'ventas'
        num += 1
        print(f"  {num}. Reportes")
        indices[num] = 'reportes'
        num += 1
        print(f"  0. Cerrar sesion")
        separador('=')

        try:
            opcion = int(input("  Elige una opcion: ").strip())
        except ValueError:
            print("  [!] Ingresa un numero valido.")
            pausar()
            continue

        if opcion == 0:
            cerrar_sesion(sesion)
            break

        accion = indices.get(opcion)

        if not accion:
            print("  [!] Opcion no valida.")
            pausar()
            continue

        if not tiene_permiso(sesion, accion):
            print("  [!] No tienes permiso para esta seccion.")
            pausar()
            continue

        ventas = cargar_ventas()

        if accion == 'productos':
            menu_productos(ventas)
        elif accion == 'clientes':
            menu_clientes(ventas)
        elif accion == 'ventas':
            menu_ventas()
        elif accion == 'reportes':
            menu_reportes(sesion)


def cerrar_sesion(sesion):
    """Muestra mensaje de cierre de sesion."""
    limpiar_pantalla()
    print(f"\n  Sesion cerrada. Hasta pronto, {sesion['nombre']}!\n")


def salir():
    """Mensaje de despedida y cierre del sistema."""
    limpiar_pantalla()
    print()
    print("  ==========================================")
    print("    Gracias por usar el Sistema .")
    print("    Hasta pronto, Dona Marta!")
    print("  ==========================================")
    print()
    sys.exit(0)


if __name__ == "__main__":
    asegurar_directorios()

    while True:
        sesion = mostrar_pantalla_login()
        if sesion:
            menu_principal(sesion)
            print()
            if input("  Iniciar nueva sesion? (s/n): ").strip().lower() != 's':
                salir()
