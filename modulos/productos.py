"""
Modulo: productos.py
Descripcion: CRUD completo de productos e inventario para el sistema POS.
Autores: [Tu nombre] / [Nombre companero]
Fecha: 2026
"""

from modulos.archivos import leer_json, escribir_json
from modulos.utilidades import (
    titulo, subtitulo, separador, mostrar_menu,
    pedir_texto, pedir_entero, pedir_flotante,
    formatear_moneda, confirmar, pausar, limpiar_pantalla
)

ARCHIVO = 'productos'


def cargar_productos():
    """Lee y devuelve la lista de productos desde el JSON."""
    return leer_json(ARCHIVO)


def guardar_productos(productos):
    """Guarda la lista de productos en el JSON."""
    escribir_json(ARCHIVO, productos)


def buscar_por_codigo(codigo, productos=None):
    """
    Busca un producto exacto por codigo (case-insensitive).
    Recibe: codigo (str), productos (list) opcional.
    Devuelve: dict del producto o None.
    """
    if productos is None:
        productos = cargar_productos()
    codigo = codigo.upper()
    for p in productos:
        if p['codigo'].upper() == codigo:
            return p
    return None


def buscar_productos(termino):
    """
    Busca productos por codigo o nombre (parcial, case-insensitive).
    Recibe: termino (str).
    Devuelve: lista de productos coincidentes.
    """
    productos = cargar_productos()
    t = termino.lower()
    return [p for p in productos if t in p['codigo'].lower() or t in p['nombre'].lower()]


def imprimir_tabla(productos):
    """
    Imprime los productos en formato de tabla.
    Recibe: productos (list de dict).
    """
    if not productos:
        print("  No hay productos para mostrar.")
        return
    print(f"  {'CODIGO':<8} {'NOMBRE':<25} {'CATEGORIA':<16} {'PRECIO':>10} {'STOCK':>6} {'MIN':>5}")
    separador('-')
    for p in productos:
        alerta = " [bajo]" if p['stock'] <= p['stock_minimo'] else ""
        print(
            f"  {p['codigo']:<8} {p['nombre']:<25} {p['categoria']:<16} "
            f"{formatear_moneda(p['precio']):>10} {p['stock']:>6} {p['stock_minimo']:>5}{alerta}"
        )


def registrar_producto():
    """Solicita datos y registra un nuevo producto unico en el inventario."""
    limpiar_pantalla()
    titulo("Registrar Nuevo Producto")
    productos = cargar_productos()

    while True:
        codigo = pedir_texto("  Codigo (ej: P001): ").upper()
        if buscar_por_codigo(codigo, productos):
            print(f"  [!] Ya existe un producto con el codigo '{codigo}'.")
        else:
            break

    nombre    = pedir_texto("  Nombre del producto: ")
    categoria = pedir_texto("  Categoria: ")
    precio    = pedir_flotante("  Precio unitario (Q): ", minimo=0.01)
    stock     = pedir_entero("  Stock inicial: ", minimo=0)
    stock_min = pedir_entero("  Stock minimo (alerta): ", minimo=0)

    nuevo = {
        "codigo": codigo, "nombre": nombre, "categoria": categoria,
        "precio": round(precio, 2), "stock": stock, "stock_minimo": stock_min
    }

    print(f"\n  Producto: {nombre} | Precio: {formatear_moneda(precio)} | Stock: {stock}")
    if confirmar("  Guardar producto? (s/n): "):
        productos.append(nuevo)
        guardar_productos(productos)
        print(f"  OK - Producto '{nombre}' registrado.")
    else:
        print("  Operacion cancelada.")
    pausar()


def listar_productos():
    """Muestra todos los productos en formato de tabla."""
    limpiar_pantalla()
    titulo("Listado de Productos")
    productos = cargar_productos()
    imprimir_tabla(productos)
    print(f"\n  Total: {len(productos)} producto(s).")
    pausar()


def buscar_producto_menu():
    """Menu de busqueda de producto por codigo o nombre."""
    limpiar_pantalla()
    titulo("Buscar Producto")
    termino = pedir_texto("  Ingresa codigo o nombre a buscar: ")
    resultados = buscar_productos(termino)
    if resultados:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):\n")
        imprimir_tabla(resultados)
    else:
        print("  No se encontraron productos con ese criterio.")
    pausar()


def actualizar_precio():
    """Actualiza el precio de un producto por codigo."""
    limpiar_pantalla()
    titulo("Actualizar Precio de Producto")
    productos = cargar_productos()
    codigo = pedir_texto("  Codigo del producto: ").upper()
    producto = buscar_por_codigo(codigo, productos)

    if not producto:
        print(f"  [!] No se encontro el producto '{codigo}'.")
        pausar()
        return

    print(f"  Producto: {producto['nombre']} | Precio actual: {formatear_moneda(producto['precio'])}")
    nuevo_precio = pedir_flotante("  Nuevo precio (Q): ", minimo=0.01)

    if confirmar(f"  Actualizar precio a {formatear_moneda(nuevo_precio)}? (s/n): "):
        producto['precio'] = round(nuevo_precio, 2)
        guardar_productos(productos)
        print("  OK - Precio actualizado.")
    else:
        print("  Operacion cancelada.")
    pausar()


def ajustar_stock():
    """Suma o resta unidades del stock de un producto con motivo registrado."""
    limpiar_pantalla()
    titulo("Ajustar Stock")
    productos = cargar_productos()
    codigo = pedir_texto("  Codigo del producto: ").upper()
    producto = buscar_por_codigo(codigo, productos)

    if not producto:
        print(f"  [!] No se encontro el producto '{codigo}'.")
        pausar()
        return

    print(f"  Producto: {producto['nombre']} | Stock actual: {producto['stock']}")
    print("  Motivos: 1) Compra  2) Merma  3) Ajuste")
    motivo_idx = pedir_entero("  Selecciona motivo: ", minimo=1, maximo=3)
    motivos = {1: "Compra", 2: "Merma", 3: "Ajuste"}
    motivo = motivos[motivo_idx]

    cantidad = pedir_entero("  Cantidad (positivo para sumar, negativo para restar): ")
    nuevo_stock = producto['stock'] + cantidad

    if nuevo_stock < 0:
        print(f"  [!] Stock insuficiente. Stock actual: {producto['stock']}.")
        pausar()
        return

    print(f"  Motivo: {motivo} | Stock nuevo: {nuevo_stock}")
    if confirmar("  Confirmar ajuste? (s/n): "):
        producto['stock'] = nuevo_stock
        guardar_productos(productos)
        print(f"  OK - Stock actualizado a {nuevo_stock}.")
    else:
        print("  Operacion cancelada.")
    pausar()


def eliminar_producto(ventas_existentes=None):
    """
    Elimina un producto si no tiene ventas registradas.
    Recibe: ventas_existentes (list) para validar.
    """
    limpiar_pantalla()
    titulo("Eliminar Producto")
    productos = cargar_productos()
    codigo = pedir_texto("  Codigo del producto a eliminar: ").upper()
    producto = buscar_por_codigo(codigo, productos)

    if not producto:
        print(f"  [!] No se encontro el producto '{codigo}'.")
        pausar()
        return

    if ventas_existentes:
        for venta in ventas_existentes:
            for item in venta.get('items', []):
                if item['codigo'].upper() == codigo:
                    print(f"  [!] No se puede eliminar: tiene ventas registradas.")
                    pausar()
                    return

    print(f"  Producto a eliminar: {producto['nombre']} | Stock: {producto['stock']}")
    if confirmar("  Eliminar definitivamente? (s/n): "):
        productos.remove(producto)
        guardar_productos(productos)
        print(f"  OK - Producto '{producto['nombre']}' eliminado.")
    else:
        print("  Operacion cancelada.")
    pausar()


def mostrar_stock_bajo():
    """Muestra productos cuyo stock actual es menor o igual al stock minimo."""
    limpiar_pantalla()
    titulo("Productos con Stock Bajo")
    productos = cargar_productos()
    bajos = [p for p in productos if p['stock'] <= p['stock_minimo']]
    if bajos:
        imprimir_tabla(bajos)
        print(f"\n  Total en alerta: {len(bajos)} producto(s).")
    else:
        print("  Todos los productos tienen stock suficiente.")
    pausar()


def menu_productos(ventas):
    """
    Despliega el submenu del modulo de productos.
    Recibe: ventas (list) para validar eliminaciones.
    """
    opciones = [
        "Registrar producto nuevo",
        "Listar todos los productos",
        "Buscar producto",
        "Actualizar precio",
        "Ajustar stock",
        "Eliminar producto",
        "Productos con stock bajo",
    ]
    while True:
        limpiar_pantalla()
        opcion = mostrar_menu(opciones, "MODULO DE PRODUCTOS")
        if opcion == 0:
            break
        elif opcion == 1:
            registrar_producto()
        elif opcion == 2:
            listar_productos()
        elif opcion == 3:
            buscar_producto_menu()
        elif opcion == 4:
            actualizar_precio()
        elif opcion == 5:
            ajustar_stock()
        elif opcion == 6:
            eliminar_producto(ventas)
        elif opcion == 7:
            mostrar_stock_bajo()

