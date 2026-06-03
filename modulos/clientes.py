"""
Modulo: clientes.py
Descripcion: CRUD completo de clientes del sistema POS.
             Soporta ventas a Consumidor Final (NIT: CF).
Autores: [Tu nombre] / [Nombre companero]
Fecha: 2026
"""

from modulos.archivos import leer_json, escribir_json
from modulos.utilidades import (
    titulo, separador, mostrar_menu,
    pedir_texto, validar_email_input,
    confirmar, pausar, limpiar_pantalla
)

ARCHIVO = 'clientes'
NIT_CF = 'CF'


def cargar_clientes():
    """Lee y devuelve la lista de clientes desde el JSON."""
    return leer_json(ARCHIVO)


def guardar_clientes(clientes):
    """Guarda la lista de clientes en el JSON."""
    escribir_json(ARCHIVO, clientes)


def buscar_por_nit(nit, clientes=None):
    """
    Busca un cliente exacto por NIT (case-insensitive).
    Recibe: nit (str), clientes (list) opcional.
    Devuelve: dict del cliente o None.
    """
    if clientes is None:
        clientes = cargar_clientes()
    nit = nit.upper()
    for c in clientes:
        if c['nit'].upper() == nit:
            return c
    return None


def buscar_clientes(termino):
    """
    Busca clientes por NIT o nombre (parcial, case-insensitive).
    Recibe: termino (str).
    Devuelve: lista de coincidencias.
    """
    clientes = cargar_clientes()
    t = termino.lower()
    return [c for c in clientes if t in c['nit'].lower() or t in c['nombre'].lower()]


def imprimir_tabla(clientes):
    """
    Imprime clientes en formato tabla.
    Recibe: clientes (list de dict).
    """
    if not clientes:
        print("  No hay clientes para mostrar.")
        return
    print(f"  {'NIT':<15} {'NOMBRE':<25} {'TELEFONO':<14} {'EMAIL':<30}")
    separador('-')
    for c in clientes:
        print(f"  {c['nit']:<15} {c['nombre']:<25} {c['telefono']:<14} {c['email']:<30}")


def registrar_cliente():
    """Solicita datos y registra un nuevo cliente con NIT unico."""
    limpiar_pantalla()
    titulo("Registrar Nuevo Cliente")
    clientes = cargar_clientes()

    while True:
        nit = pedir_texto("  NIT (ej: 1234567-8): ").upper()
        if nit == NIT_CF:
            print("  [!] 'CF' esta reservado para Consumidor Final.")
            continue
        if buscar_por_nit(nit, clientes):
            print(f"  [!] Ya existe un cliente con el NIT '{nit}'.")
        else:
            break

    nombre   = pedir_texto("  Nombre completo: ")
    telefono = pedir_texto("  Telefono: ")
    email    = validar_email_input("  Email: ")

    nuevo = {"nit": nit, "nombre": nombre, "telefono": telefono, "email": email}

    print(f"\n  Cliente: {nombre} | NIT: {nit} | Tel: {telefono}")
    if confirmar("  Guardar cliente? (s/n): "):
        clientes.append(nuevo)
        guardar_clientes(clientes)
        print(f"  OK - Cliente '{nombre}' registrado.")
    else:
        print("  Operacion cancelada.")
    pausar()


def listar_clientes():
    """Muestra todos los clientes en formato tabla."""
    limpiar_pantalla()
    titulo("Listado de Clientes")
    clientes = cargar_clientes()
    imprimir_tabla(clientes)
    print(f"\n  Total: {len(clientes)} cliente(s).")
    pausar()


def buscar_cliente_menu():
    """Menu de busqueda de cliente por NIT o nombre."""
    limpiar_pantalla()
    titulo("Buscar Cliente")
    termino = pedir_texto("  Ingresa NIT o nombre: ")
    resultados = buscar_clientes(termino)
    if resultados:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):\n")
        imprimir_tabla(resultados)
    else:
        print("  No se encontraron clientes con ese criterio.")
    pausar()


def actualizar_cliente():
    """Actualiza telefono o email de un cliente existente."""
    limpiar_pantalla()
    titulo("Actualizar Datos de Cliente")
    clientes = cargar_clientes()
    nit = pedir_texto("  NIT del cliente: ").upper()
    cliente = buscar_por_nit(nit, clientes)

    if not cliente:
        print(f"  [!] No se encontro el cliente con NIT '{nit}'.")
        pausar()
        return

    print(f"  Cliente: {cliente['nombre']}")
    print(f"  Telefono actual: {cliente['telefono']}  |  Email actual: {cliente['email']}")
    print("  (Deja en blanco para conservar el valor actual)")

    nuevo_tel   = input("  Nuevo telefono: ").strip()
    nuevo_email = input("  Nuevo email: ").strip()

    if nuevo_tel:
        cliente['telefono'] = nuevo_tel
    if nuevo_email:
        if not ('@' in nuevo_email and '.' in nuevo_email):
            print("  [!] Email invalido. No se actualizo el email.")
        else:
            cliente['email'] = nuevo_email

    if confirmar("  Guardar cambios? (s/n): "):
        guardar_clientes(clientes)
        print("  OK - Datos actualizados.")
    else:
        print("  Operacion cancelada.")
    pausar()


def eliminar_cliente(ventas_existentes=None):
    """
    Elimina un cliente si no tiene ventas registradas.
    Recibe: ventas_existentes (list) para validar.
    """
    limpiar_pantalla()
    titulo("Eliminar Cliente")
    clientes = cargar_clientes()
    nit = pedir_texto("  NIT del cliente a eliminar: ").upper()
    cliente = buscar_por_nit(nit, clientes)

    if not cliente:
        print(f"  [!] No se encontro el cliente con NIT '{nit}'.")
        pausar()
        return

    if ventas_existentes:
        for venta in ventas_existentes:
            if venta.get('nit_cliente', '').upper() == nit:
                print(f"  [!] No se puede eliminar: tiene ventas registradas.")
                pausar()
                return

    print(f"  Cliente a eliminar: {cliente['nombre']} | NIT: {nit}")
    if confirmar("  Eliminar definitivamente? (s/n): "):
        clientes.remove(cliente)
        guardar_clientes(clientes)
        print(f"  OK - Cliente '{cliente['nombre']}' eliminado.")
    else:
        print("  Operacion cancelada.")
    pausar()


def menu_clientes(ventas):
    """
    Despliega el submenu del modulo de clientes.
    Recibe: ventas (list) para validar eliminaciones.
    """
    opciones = [
        "Registrar cliente nuevo",
        "Listar todos los clientes",
        "Buscar cliente",
        "Actualizar datos de contacto",
        "Eliminar cliente",
    ]
    while True:
        limpiar_pantalla()
        opcion = mostrar_menu(opciones, "MODULO DE CLIENTES")
        if opcion == 0:
            break
        elif opcion == 1:
            registrar_cliente()
        elif opcion == 2:
            listar_clientes()
        elif opcion == 3:
            buscar_cliente_menu()
        elif opcion == 4:
            actualizar_cliente()
        elif opcion == 5:
            eliminar_cliente(ventas)
