"""
Modulo: archivos.py
Descripcion: Funciones para leer y escribir archivos JSON con manejo de errores.
Autores: [Sergio Huinac] / [daniel adrian bartolo franciscos]
Fecha: 2026
"""

import json
import os

RUTA_DATOS    = os.path.join(os.path.dirname(__file__), '..', 'datos')
RUTA_FACTURAS = os.path.join(os.path.dirname(__file__), '..', 'facturas')


def asegurar_directorios():
    """Crea las carpetas 'datos' y 'facturas' si no existen."""
    os.makedirs(RUTA_DATOS, exist_ok=True)
    os.makedirs(RUTA_FACTURAS, exist_ok=True)


def leer_json(nombre_archivo):
    """
    Lee y devuelve el contenido de un archivo JSON.
    Recibe: nombre del archivo (str), sin ruta ni extension.
    Devuelve: lista o dict con los datos, o lista vacia si hay error.
    """
    ruta = os.path.join(RUTA_DATOS, f"{nombre_archivo}.json")
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"  [!] Error: el archivo {nombre_archivo}.json esta corrupto.")
        return []


def escribir_json(nombre_archivo, datos):
    """
    Escribe datos en un archivo JSON, sobreescribiendo el contenido.
    Recibe: nombre_archivo (str), datos (list o dict).
    Devuelve: True si tuvo exito, False si hubo error.
    """
    ruta = os.path.join(RUTA_DATOS, f"{nombre_archivo}.json")
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True
    except OSError as e:
        print(f"  [!] Error al guardar {nombre_archivo}.json: {e}")
        return False


def guardar_factura(nombre_archivo, contenido):
    """
    Guarda un archivo de factura .txt en la carpeta facturas/.
    Recibe: nombre_archivo (str), contenido (str).
    Devuelve: ruta completa del archivo guardado.
    """
    ruta = os.path.join(RUTA_FACTURAS, nombre_archivo)
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return ruta
    except OSError as e:
        print(f"  [!] Error al guardar factura: {e}")
        return None
