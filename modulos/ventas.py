"""
Modulo: ventas.py
Descripcion: Proceso de venta, carrito, facturacion y persistencia de ventas.
Autores: [Sergio Huinac] / [daniel adrian bartolo franciscos]
Fecha: 2026
"""

from datetime import datetime
from modulos.archivos import leer_json, escribir_json, guardar_factura
from modulos.utilidades import (
    titulo, subtitulo, separador, mostrar_menu,
    pedir_texto, pedir_entero, formatear_moneda,
    confirmar, pausar, limpiar_pantalla
)
from modulos.productos import cargar_productos, guardar_productos, buscar_por_codigo
from modulos.clientes import cargar_clientes, buscar_por_nit, NIT_CF

ARCHIVO = 'ventas'
IVA = 0.12


def cargar_ventas():
    """Lee y devuelve la lista de ventas desde el JSON."""
    return leer_json(ARCHIVO)


def guardar_ventas(ventas):
    """Guarda la lista de ventas en el JSON."""
    escribir_json(ARCHIVO, ventas)


def generar_id_venta(ventas):
    """
    Genera el siguiente ID de venta correlativo (ej: V0001).
    Recibe: ventas (list).
    Devuelve: str con el nuevo ID.
    """
    if not ventas:
        return "V0001"
    try:
        numero = int(ventas[-1]['id_venta'][1:]) + 1
    except (ValueError, KeyError):
        numero = len(ventas) + 1
    return f"V{numero:04d}"


def mostrar_carrito(carrito):
    """
    Imprime el contenido del carrito con subtotales.
    Recibe: carrito (list de dict).
    """
    if not carrito:
        print("  El carrito esta vacio.")
        return
    subtitulo("CARRITO ACTUAL")
    print(f"  {'#':<4} {'CODIGO':<8} {'NOMBRE':<25} {'CANT':>5} {'P.UNIT':>10} {'SUBTOTAL':>12}")
    separador('-')
    for i, item in enumerate(carrito, 1):
        print(
            f"  {i:<4} {item['codigo']:<8} {item['nombre']:<25} "
            f"{item['cantidad']:>5} {formatear_moneda(item['precio_unit']):>10} "
            f"{formatear_moneda(item['subtotal']):>12}"
        )
    subtotal  = sum(i['subtotal'] for i in carrito)
    iva_monto = round(subtotal * IVA, 2)
    total     = round(subtotal + iva_monto, 2)
    separador('-')
    print(f"  {'Subtotal:':>52} {formatear_moneda(subtotal):>12}")
    print(f"  {'IVA (12%):':>52} {formatear_moneda(iva_monto):>12}")
    print(f"  {'TOTAL:':>52} {formatear_moneda(total):>12}")


def agregar_al_carrito(carrito, productos):
    """
    Agrega un producto al carrito validando stock disponible.
    Recibe: carrito (list), productos (list).
    Devuelve: carrito actualizado.
    """
    codigo  = pedir_texto("  Codigo del producto: ").upper()
    producto = buscar_por_codigo(codigo, productos)

    if not producto:
        print(f"  [!] No se encontro el producto '{codigo}'.")
        return carrito

    print(f"  {producto['nombre']} | Precio: {formatear_moneda(producto['precio'])} | Stock: {producto['stock']}")

    en_carrito  = sum(i['cantidad'] for i in carrito if i['codigo'] == codigo)
    disponible  = producto['stock'] - en_carrito

    if disponible <= 0:
        print("  [!] Sin stock disponible para este producto.")
        return carrito

    cantidad = pedir_entero(f"  Cantidad (disponible: {disponible}): ", minimo=1, maximo=disponible)

    for item in carrito:
        if item['codigo'] == codigo:
            item['cantidad'] += cantidad
            item['subtotal'] = round(item['cantidad'] * item['precio_unit'], 2)
            print("  OK - Cantidad actualizada en el carrito.")
            return carrito

    carrito.append({
        "codigo": codigo,
        "nombre": producto['nombre'],
        "cantidad": cantidad,
        "precio_unit": producto['precio'],
        "subtotal": round(cantidad * producto['precio'], 2)
    })
    print(f"  OK - '{producto['nombre']}' agregado al carrito.")
    return carrito


def quitar_del_carrito(carrito):
    """
    Quita un producto del carrito por numero de linea.
    Recibe: carrito (list).
    Devuelve: carrito actualizado.
    """
    if not carrito:
        print("  El carrito esta vacio.")
        return carrito
    mostrar_carrito(carrito)
    num = pedir_entero("  Numero de linea a quitar (0 para cancelar): ", minimo=0, maximo=len(carrito))
    if num == 0:
        return carrito
    eliminado = carrito.pop(num - 1)
    print(f"  OK - '{eliminado['nombre']}' eliminado del carrito.")
    return carrito


def generar_texto_factura(venta, nombre_cliente):
    """
    Genera el texto completo de una factura en formato .txt.
    Recibe: venta (dict), nombre_cliente (str).
    Devuelve: str con el contenido de la factura.
    """
    lineas = [
        "=" * 52,
        "         TU TIENDA - DONA MARTA",
        "=" * 52,
        f"  Factura N.: {venta['id_venta']}",
        f"  Fecha:      {venta['fecha']}",
        f"  Cliente:    {nombre_cliente}",
        f"  NIT:        {venta['nit_cliente']}",
        "-" * 52,
        f"  {'PRODUCTO':<25} {'CANT':>5} {'P.UNIT':>8} {'SUBTOT':>10}",
        "-" * 52,
    ]
    for item in venta['items']:
        lineas.append(
            f"  {item['nombre']:<25} {item['cantidad']:>5} "
            f"Q{item['precio_unit']:>7.2f} Q{item['subtotal']:>9.2f}"
        )
    lineas += [
        "-" * 52,
        f"  {'Subtotal:':>40} Q{venta['subtotal']:>9.2f}",
        f"  {'IVA (12%):':>40} Q{venta['iva']:>9.2f}",
        f"  {'TOTAL:':>40} Q{venta['total']:>9.2f}",
        "=" * 52,
        "    Gracias por su compra!",
        "=" * 52,
    ]
    return "\n".join(lineas)


def nueva_venta():
    """Proceso completo de una nueva venta: carrito, confirmacion y facturacion."""
    limpiar_pantalla()
    titulo("Nueva Venta")
    productos = cargar_productos()
    clientes  = cargar_clientes()
    ventas    = cargar_ventas()

    nit = pedir_texto("  NIT del cliente (o 'CF' para Consumidor Final): ").upper()
    if nit == NIT_CF:
        nombre_cliente = "Consumidor Final"
    else:
        cliente = buscar_por_nit(nit, clientes)
        if not cliente:
            print(f"  [!] Cliente con NIT '{nit}' no encontrado.")
            print("  Puede registrarlo primero o usar 'CF'.")
            pausar()
            return
        nombre_cliente = cliente['nombre']

    print(f"  Cliente: {nombre_cliente}")
    carrito = []

    while True:
        limpiar_pantalla()
        titulo(f"Venta -- Cliente: {nombre_cliente}")
        mostrar_carrito(carrito)

        print()
        subtitulo("OPCIONES")
        print("  1. Agregar producto")
        print("  2. Quitar producto del carrito")
        print("  3. Confirmar venta")
        print("  4. Cancelar venta")
        separador()

        opcion = pedir_entero("  Elige una opcion: ", minimo=1, maximo=4)

        if opcion == 1:
            carrito = agregar_al_carrito(carrito, productos)
            pausar()
        elif opcion == 2:
            carrito = quitar_del_carrito(carrito)
            pausar()
        elif opcion == 3:
            if not carrito:
                print("  [!] El carrito esta vacio. Agrega productos primero.")
                pausar()
                continue
            confirmar_venta(carrito, nit, nombre_cliente, productos, ventas)
            break
        elif opcion == 4:
            if confirmar("  Cancelar la venta en curso? (s/n): "):
                print("  Venta cancelada. No se realizaron cambios.")
                pausar()
            break


def confirmar_venta(carrito, nit, nombre_cliente, productos, ventas):
    """
    Confirma la venta: descuenta stock, guarda en JSON y genera factura.
    Recibe: carrito, nit, nombre_cliente, productos y ventas (list/str).
    """
    limpiar_pantalla()
    titulo("Confirmar Venta")
    mostrar_carrito(carrito)
    print()

    if not confirmar("  Confirmar y procesar la venta? (s/n): "):
        print("  Venta no confirmada.")
        pausar()
        return

    subtotal  = round(sum(i['subtotal'] for i in carrito), 2)
    iva_monto = round(subtotal * IVA, 2)
    total     = round(subtotal + iva_monto, 2)
    fecha     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id_venta  = generar_id_venta(ventas)

    for item in carrito:
        producto = buscar_por_codigo(item['codigo'], productos)
        if producto:
            producto['stock'] -= item['cantidad']
    guardar_productos(productos)

    nueva = {
        "id_venta": id_venta, "fecha": fecha, "nit_cliente": nit,
        "items": carrito, "subtotal": subtotal, "iva": iva_monto, "total": total
    }
    ventas.append(nueva)
    guardar_ventas(ventas)

    contenido     = generar_texto_factura(nueva, nombre_cliente)
    nombre_archivo = f"factura_{id_venta}_{fecha[:10]}.txt"
    ruta          = guardar_factura(nombre_archivo, contenido)

    print(f"\n  OK - Venta {id_venta} registrada.")
    print(f"  Total cobrado: {formatear_moneda(total)}")
    if ruta:
        print(f"  Factura guardada en: {ruta}")
    print()
    print(contenido)
    pausar()


def menu_ventas():
    """Despliega el submenu del modulo de ventas."""
    opciones = ["Nueva venta"]
    while True:
        limpiar_pantalla()
        opcion = mostrar_menu(opciones, "MODULO DE VENTAS")
        if opcion == 0:
            break
        elif opcion == 1:
            nueva_venta()
