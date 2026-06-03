"""
Modulo: utilidades.py
Descripcion: Funciones de validacion, formateo de texto y presentacion de menus.
Autores: [Sergio Huinac] / [daniel adrian bartolo franciscos]
Fecha: 2026
"""

import os


def limpiar_pantalla():
    """Limpia la consola segun el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pedir_entero(mensaje, minimo=None, maximo=None):
    """
    Pide un numero entero al usuario con validacion.
    Recibe: mensaje (str), minimo y maximo opcionales (int).
    Devuelve: entero validado.
    """
    while True:
        try:
            valor = int(input(mensaje).strip())
            if minimo is not None and valor < minimo:
                print(f"  [!] El valor minimo permitido es {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  [!] El valor maximo permitido es {maximo}.")
                continue
            return valor
        except ValueError:
            print("  [!] Ingresa un numero entero valido.")


def pedir_flotante(mensaje, minimo=0.0):
    """
    Pide un numero decimal al usuario con validacion.
    Recibe: mensaje (str), minimo (float).
    Devuelve: float validado.
    """
    while True:
        try:
            valor = float(input(mensaje).strip())
            if valor < minimo:
                print(f"  [!] El valor no puede ser menor a {minimo}.")
                continue
            return valor
        except ValueError:
            print("  [!] Ingresa un numero decimal valido (usa punto, ej: 6.50).")


def pedir_texto(mensaje, requerido=True):
    """
    Pide una cadena de texto al usuario.
    Recibe: mensaje (str), requerido (bool).
    Devuelve: texto ingresado sin espacios al inicio o final.
    """
    while True:
        valor = input(mensaje).strip()
        if requerido and not valor:
            print("  [!] Este campo no puede estar vacio.")
            continue
        return valor


def validar_email(email):
    """
    Valida que un email contenga '@' y '.'.
    Recibe: email (str).
    Devuelve: True si es valido, False si no.
    """
    return '@' in email and '.' in email


def validar_email_input(mensaje):
    """
    Pide un email y lo valida antes de devolverlo.
    Recibe: mensaje (str).
    Devuelve: email validado (str).
    """
    while True:
        email = input(mensaje).strip()
        if validar_email(email):
            return email
        print("  [!] Email invalido. Debe contener '@' y '.'.")


def separador(caracter='-', ancho=60):
    """Imprime una linea separadora."""
    print(caracter * ancho)


def titulo(texto):
    """Imprime un bloque de titulo con bordes."""
    separador('=')
    print(f"  {texto.upper()}")
    separador('=')


def subtitulo(texto):
    """Imprime un subtitulo con separador simple."""
    separador()
    print(f"  {texto}")
    separador()


def mostrar_menu(opciones, titulo_menu="MENU"):
    """
    Muestra un menu numerado y devuelve la opcion elegida.
    Recibe: opciones (list de str), titulo_menu (str).
    Devuelve: entero con la opcion seleccionada.
    """
    print()
    subtitulo(titulo_menu)
    for i, opcion in enumerate(opciones, 1):
        print(f"  {i}. {opcion}")
    print(f"  0. Volver / Salir")
    separador()
    return pedir_entero("  Elige una opcion: ", minimo=0, maximo=len(opciones))


def formatear_moneda(valor):
    """
    Formatea un float como moneda con 2 decimales.
    Recibe: valor (float).
    Devuelve: str con formato 'Q 1,234.56'.
    """
    return f"Q {valor:,.2f}"


def confirmar(mensaje="Confirmar? (s/n): "):
    """
    Pide confirmacion s/n al usuario.
    Recibe: mensaje (str).
    Devuelve: True si responde 's', False en caso contrario.
    """
    respuesta = input(mensaje).strip().lower()
    return respuesta == 's'


def pausar():
    """Pausa la ejecucion esperando que el usuario presione Enter."""
    input("\n  Presiona Enter para continuar...")
