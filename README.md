# tu-tienda
#  Sistema POS — Tu Tienda

> Sistema de punto de venta en consola desarrollado en Python para pequeños negocios de barrio.  
> Diseñado para ser simple, robusto y fácil de usar sin conexión a internet.

---

## Descripción

**Tu Tienda** es una herramienta POS (Point of Sale) que permite a Doña Marta y su familia gestionar:

- Inventario de productos con alertas de stock bajo
- Registro de clientes
- Proceso de ventas con carrito y facturación automática
- Reportes de ventas, cierres de caja y estadísticas

Todos los datos se guardan en archivos **JSON locales**, sin necesidad de internet ni servidores externos. Funciona perfectamente en laptops con Windows, Linux o macOS.

---

## Estructura del proyecto

```
tu-tienda/
├── main.py                  # Punto de entrada y menú principal
├── modulos/
│   ├── productos.py         # CRUD de productos e inventario
│   ├── clientes.py          # CRUD de clientes
│   ├── ventas.py            # Proceso de venta y facturación
│   ├── reportes.py          # Consultas y estadísticas
│   ├── archivos.py          # Lectura/escritura JSON
│   └── utilidades.py        # Validaciones, formateo, menús
├── datos/
│   ├── productos.json
│   ├── clientes.json
│   └── ventas.json
├── facturas/                # Facturas generadas en .txt
└── README.md
```

---

## Requisitos

- Python **3.10 o superior**
- No requiere librerías externas (solo módulos estándar: `json`, `datetime`, `os`)

---

## Cómo ejecutar

1. Clona o descarga el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-tienda.git
   cd tu-tienda
   ```

2. Ejecuta el sistema:
   ```bash
   python main.py
   ```

> Las carpetas `datos/` y `facturas/` se crean automáticamente si no existen.

---

## Menú principal

```
╔══════════════════════════════════════════════════╗
       SISTEMA  — TU TIENDA              
         Con cariño para Doña Marta           
╚══════════════════════════════════════════════════╝

MENÚ PRINCIPAL
══════════════════════════════════════════════════════════════
  1.   Productos (Inventario)
  2.   Clientes
  3.   Ventas
  4.   Reportes
  0. Salir del sistema
```

---

##  Módulo de Productos

| # | Función |
|---|---------|
| 1 | Registrar producto nuevo |
| 2 | Listar todos los productos |
| 3 | Buscar por código o nombre |
| 4 | Actualizar precio |
| 5 | Ajustar stock (compra / merma / ajuste) |
| 6 | Eliminar producto |
| 7 | Ver productos con stock bajo ⚠ |

---

##  Módulo de Clientes

| # | Función |
|---|---------|
| 1 | Registrar cliente nuevo |
| 2 | Listar todos los clientes |
| 3 | Buscar por NIT o nombre |
| 4 | Actualizar teléfono o email |
| 5 | Eliminar cliente |

>  Soporta ventas a **Consumidor Final** usando el NIT especial `CF`.

---

## 🛍 Módulo de Ventas

1. Ingresar NIT del cliente o usar `CF`
2. Agregar productos al carrito por código
3. Ver, modificar o quitar productos del carrito
4. Calcular subtotal, IVA (12%) y total automáticamente
5. Confirmar venta → descuenta stock, guarda en `ventas.json` y genera factura `.txt`

**Ejemplo de factura generada:**
```
════════════════════════════════════════════════════
         TU TIENDA - DOÑA MARTA
════════════════════════════════════════════════════
  Factura #: V0001
  Fecha:     2026-05-15 10:32:00
  Cliente:   María López
  NIT:       1234567-8
────────────────────────────────────────────────────
  PRODUCTO                  CANT  P.UNIT   SUBTOTAL
────────────────────────────────────────────────────
  Azúcar 1lb                   2  Q   6.50  Q    13.00
────────────────────────────────────────────────────
                 Subtotal:           Q    13.00
                 IVA (12%):          Q     1.56
                 TOTAL:              Q    14.56
════════════════════════════════════════════════════
    ¡Gracias por su compra!
```

---

##  Módulo de Reportes

| Reporte | Descripción |
|---------|-------------|
| Top 5 productos | Los más vendidos por unidades |
| Ventas del día | Transacciones y monto del día actual |
| Ventas por fechas | Filtro por rango de fechas |
| Stock bajo | Productos que necesitan reposición |
| Historial cliente | Compras de un cliente específico |
| Cierre de caja | Total, ticket promedio y unidades vendidas del día |

---

##  Validaciones y robustez

- Códigos de producto y NITs únicos
- Precios y stock no pueden ser negativos
- Cantidades en venta deben ser enteros positivos
- Email validado con `@` y `.`
- Entradas de texto inválidas no crashean el programa (`try/except`)
- Archivos JSON protegidos contra corrupción y ausencia
- Datos guardados inmediatamente en cada operación

---

##  Autores

- **[Tu nombre]** — [tu-email@correo.com]
- **[Nombre compañero]** — [compañero@correo.com]

Proyecto Final · Programación 1 · 2026

---
