"""
Modulo: reportes.py
Descripcion: Reportes y estadisticas del sistema POS.
Autores: [Sergio Huinac] / [daniel adrian bartolo franciscos]
Fecha: 2026
"""

from datetime import datetime, date
from collections import defaultdict
from modulos.archivos import leer_json
from modulos.utilidades import (
    titulo, subtitulo, separador, mostrar_menu,
    pedir_texto, formatear_moneda, pausar, limpiar_pantalla
)
from modulos.productos import cargar_productos

ARCHIVO_VENTAS  = 'ventas'
ARCHIVO_CLIENTES = 'clientes'


def cargar_ventas():
    """Lee y devuelve la lista de ventas."""
    return leer_json(ARCHIVO_VENTAS)


def cargar_clientes():
    """Lee y devuelve la lista de clientes."""
    return leer_json(ARCHIVO_CLIENTES)


def parsear_fecha(fecha_str):
    """
    Convierte una cadena de fecha a objeto date.
    Recibe: fecha_str (str) en formato 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS'.
    Devuelve: objeto date o None si falla.
    """
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(fecha_str, fmt).date()
        except ValueError:
            continue
    return None


def pedir_fecha(mensaje):
    """
    Pide una fecha al usuario en formato YYYY-MM-DD.
    Recibe: mensaje (str).
    Devuelve: objeto date validado.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            return datetime.strptime(entrada, "%Y-%m-%d").date()
        except ValueError:
            print("  [!] Formato invalido. Usa YYYY-MM-DD (ej: 2026-05-15).")


def top5_productos():
    """Muestra los 5 productos mas vendidos por cantidad de unidades."""
    limpiar_pantalla()
    titulo("Top 5 Productos Mas Vendidos")
    ventas = cargar_ventas()
    conteo = defaultdict(lambda: {"nombre": "", "cantidad": 0, "total": 0.0})

    for venta in ventas:
        for item in venta.get('items', []):
            cod = item['codigo']
            conteo[cod]['nombre']   = item['nombre']
            conteo[cod]['cantidad'] += item['cantidad']
            conteo[cod]['total']    += item['subtotal']

    ranking = sorted(conteo.items(), key=lambda x: x[1]['cantidad'], reverse=True)[:5]

    if not ranking:
        print("  No hay ventas registradas.")
        pausar()
        return

    print(f"  {'#':<4} {'CODIGO':<8} {'NOMBRE':<28} {'UNIDADES':>9} {'INGRESOS':>12}")
    separador('-')
    for pos, (codigo, datos) in enumerate(ranking, 1):
        print(
            f"  {pos:<4} {codigo:<8} {datos['nombre']:<28} "
            f"{datos['cantidad']:>9} {formatear_moneda(datos['total']):>12}"
        )
    pausar()


def ventas_del_dia():
    """Muestra el total de ventas de la fecha actual."""
    limpiar_pantalla()
    titulo("Ventas de Hoy")
    hoy = date.today()
    ventas = cargar_ventas()
    ventas_hoy = [v for v in ventas if parsear_fecha(v['fecha']) == hoy]

    print(f"  Fecha: {hoy.strftime('%d/%m/%Y')}")
    separador('-')

    if not ventas_hoy:
        print("  No hay ventas registradas para hoy.")
        pausar()
        return

    total = sum(v['total'] for v in ventas_hoy)
    print(f"  Transacciones: {len(ventas_hoy)}")
    print(f"  Monto total:   {formatear_moneda(total)}")
    print()
    for v in ventas_hoy:
        print(f"  {v['id_venta']}  {v['fecha']}  NIT: {v['nit_cliente']:<15}  Total: {formatear_moneda(v['total'])}")
    pausar()


def ventas_rango_fechas():
    """Muestra el total de ventas entre dos fechas ingresadas por el usuario."""
    limpiar_pantalla()
    titulo("Ventas por Rango de Fechas")
    fecha_inicio = pedir_fecha("  Fecha inicio (YYYY-MM-DD): ")
    fecha_fin    = pedir_fecha("  Fecha fin   (YYYY-MM-DD): ")

    if fecha_inicio > fecha_fin:
        print("  [!] La fecha inicio no puede ser posterior a la fecha fin.")
        pausar()
        return

    ventas   = cargar_ventas()
    filtradas = [v for v in ventas if fecha_inicio <= parsear_fecha(v['fecha']) <= fecha_fin]

    print(f"\n  Rango: {fecha_inicio} -> {fecha_fin}")
    separador('-')

    if not filtradas:
        print("  No hay ventas en ese rango.")
        pausar()
        return

    total = sum(v['total'] for v in filtradas)
    print(f"  Transacciones: {len(filtradas)}")
    print(f"  Monto total:   {formatear_moneda(total)}")
    print()
    for v in filtradas:
        print(f"  {v['id_venta']}  {v['fecha']}  Total: {formatear_moneda(v['total'])}")
    pausar()


def productos_stock_bajo():
    """Muestra productos con stock actual menor o igual al minimo."""
    limpiar_pantalla()
    titulo("Alerta: Productos con Stock Bajo")
    productos = cargar_productos()
    bajos = [p for p in productos if p['stock'] <= p['stock_minimo']]

    if not bajos:
        print("  Todos los productos tienen stock suficiente.")
        pausar()
        return

    print(f"  {'CODIGO':<8} {'NOMBRE':<28} {'STOCK':>7} {'MINIMO':>7}")
    separador('-')
    for p in bajos:
        print(f"  {p['codigo']:<8} {p['nombre']:<28} {p['stock']:>7} {p['stock_minimo']:>7}  [REPONER]")
    print(f"\n  Total en alerta: {len(bajos)} producto(s).")
    pausar()


def historial_cliente():
    """Muestra el historial de compras de un cliente especifico."""
    limpiar_pantalla()
    titulo("Historial de Compras por Cliente")
    nit     = pedir_texto("  NIT del cliente (o 'CF'): ").upper()
    ventas  = cargar_ventas()
    clientes = cargar_clientes()

    nombre = "Consumidor Final"
    if nit != "CF":
        for c in clientes:
            if c['nit'].upper() == nit:
                nombre = c['nombre']
                break

    historial = [v for v in ventas if v['nit_cliente'].upper() == nit]

    print(f"\n  Cliente: {nombre} | NIT: {nit}")
    separador('-')

    if not historial:
        print("  No hay compras registradas para este cliente.")
        pausar()
        return

    total_general = 0.0
    for v in historial:
        print(f"\n  Venta: {v['id_venta']}  Fecha: {v['fecha']}")
        for item in v['items']:
            print(f"    - {item['nombre']} x{item['cantidad']} -> {formatear_moneda(item['subtotal'])}")
        print(f"    Total: {formatear_moneda(v['total'])}")
        total_general += v['total']

    separador('-')
    print(f"  Total historico: {formatear_moneda(total_general)} en {len(historial)} venta(s).")
    pausar()


def cierre_de_caja():
    """Genera el cierre de caja del dia con estadisticas completas."""
    limpiar_pantalla()
    titulo("Cierre de Caja del Dia")
    hoy    = date.today()
    ventas = cargar_ventas()
    ventas_hoy = [v for v in ventas if parsear_fecha(v['fecha']) == hoy]

    print(f"  Fecha: {hoy.strftime('%d/%m/%Y')}")
    separador('=')

    if not ventas_hoy:
        print("  No hay transacciones registradas para hoy.")
        pausar()
        return

    total     = sum(v['total'] for v in ventas_hoy)
    num_trans = len(ventas_hoy)
    ticket    = total / num_trans if num_trans > 0 else 0

    prod_vendidos = defaultdict(lambda: {"nombre": "", "cantidad": 0})
    for v in ventas_hoy:
        for item in v['items']:
            prod_vendidos[item['codigo']]['nombre']   = item['nombre']
            prod_vendidos[item['codigo']]['cantidad'] += item['cantidad']

    print(f"  Numero de transacciones: {num_trans}")
    print(f"  Total de ventas:         {formatear_moneda(total)}")
    print(f"  Ticket promedio:         {formatear_moneda(ticket)}")
    print()
    subtitulo("PRODUCTOS VENDIDOS HOY")
    print(f"  {'CODIGO':<8} {'NOMBRE':<28} {'UNIDADES':>9}")
    separador('-')
    for codigo, datos in sorted(prod_vendidos.items()):
        print(f"  {codigo:<8} {datos['nombre']:<28} {datos['cantidad']:>9}")
    separador('=')
    pausar()


def menu_reportes(sesion=None):
    """
    Despliega el submenu de reportes segun el rol del usuario.
    Admin ve todos los reportes. Cajero solo ve opciones basicas.
    Recibe: sesion (dict) opcional con datos del usuario.
    """
    es_admin = (sesion is None) or (sesion.get('rol') == 'admin')

    opciones_admin = [
        ("Top 5 productos mas vendidos",      top5_productos),
        ("Total de ventas del dia",            ventas_del_dia),
        ("Ventas en rango de fechas",          ventas_rango_fechas),
        ("Productos con stock bajo",           productos_stock_bajo),
        ("Historial de compras de un cliente", historial_cliente),
        ("Cierre de caja del dia",             cierre_de_caja),
    ]

    opciones_cajero = [
        ("Total de ventas del dia",  ventas_del_dia),
        ("Productos con stock bajo", productos_stock_bajo),
        ("Cierre de caja del dia",   cierre_de_caja),
    ]

    opciones_activas = opciones_admin if es_admin else opciones_cajero
    etiquetas = [o[0] for o in opciones_activas]

    while True:
        limpiar_pantalla()
        opcion = mostrar_menu(etiquetas, "MODULO DE REPORTES")
        if opcion == 0:
            break
        if 1 <= opcion <= len(opciones_activas):
            opciones_activas[opcion - 1][1]()