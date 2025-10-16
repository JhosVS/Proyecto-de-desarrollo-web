from app.db import get_connection

# Obtener todos los productos
def get_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, nombre, stock_actual, precio_unitario FROM Productos")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": r[0], "nombre": r[1], "stock": float(r[2]), "precio": float(r[3])}
        for r in rows
    ]

# Insertar nuevo producto
def insertar_producto(nombre, id_categoria, id_proveedor, unidad, stock, minimo, precio):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Productos (nombre, id_categoria, id_proveedor, unidad_medida, stock_actual, stock_minimo, precio_unitario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, id_categoria, id_proveedor, unidad, stock, minimo, precio))
    conn.commit()
    conn.close()
    return True



from app.db import get_connection

# =====================================================
#   PRODUCTOS
# =====================================================

def obtener_productos():
    conn = get_connection()
    productos = []
    try:
        cursor = conn.cursor()
        query = """
            SELECT p.id_producto, p.nombre, c.nombre AS categoria, pr.nombre AS proveedor,
                   p.unidad_medida, p.stock_actual, p.stock_minimo, p.precio_unitario, p.estado
            FROM Productos p
            INNER JOIN Categorias c ON p.id_categoria = c.id_categoria
            INNER JOIN Proveedores pr ON p.id_proveedor = pr.id_proveedor
            ORDER BY p.id_producto DESC
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            productos.append({
                "id": row.id_producto,
                "nombre": row.nombre,
                "categoria": row.categoria,
                "proveedor": row.proveedor,
                "unidad": row.unidad_medida,
                "stock": float(row.stock_actual),
                "stock_minimo": float(row.stock_minimo),  # <-- esto es nuevo
                "precio": float(row.precio_unitario),
                "estado": row.estado
            })
    finally:
        conn.close()
    return productos


def obtener_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_categoria, nombre FROM Categorias ORDER BY nombre")
    datos = [{"id": r.id_categoria, "nombre": r.nombre} for r in cursor.fetchall()]
    conn.close()
    return datos


def obtener_proveedores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_proveedor, nombre FROM Proveedores ORDER BY nombre")
    datos = [{"id": r.id_proveedor, "nombre": r.nombre} for r in cursor.fetchall()]
    conn.close()
    return datos


def agregar_producto(nombre, id_categoria, id_proveedor, unidad, stock_inicial, stock_minimo, precio_unitario):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_AgregarProducto 
                @nombre=?, @id_categoria=?, @id_proveedor=?, 
                @unidad_medida=?, @stock_inicial=?, @stock_minimo=?, @precio_unitario=?
        """, (nombre, id_categoria, id_proveedor, unidad, stock_inicial, stock_minimo, precio_unitario))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar producto:", e)
        return False
    finally:
        conn.close()


# EL SIGUIENTE AVANCE:

def obtener_producto_por_id(id_producto):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_producto, nombre, id_categoria, id_proveedor,
                   unidad_medida, stock_actual, stock_minimo, precio_unitario, estado
            FROM Productos
            WHERE id_producto = ?
        """, (id_producto,))
        
        row = cursor.fetchone()
        if not row:
            return None

        return {
            "id": row.id_producto,
            "nombre": row.nombre,
            "id_categoria": row.id_categoria,
            "id_proveedor": row.id_proveedor,
            "unidad": row.unidad_medida,
            "stock": row.stock_actual,
            "stock_minimo": row.stock_minimo,
            "precio": row.precio_unitario,
            "estado": row.estado
        }
    except Exception as e:
        print("Error en obtener_producto_por_id:", e)
        return None
    finally:
        conn.close()


def actualizar_producto(id_producto, nombre, id_categoria, id_proveedor, unidad, stock_minimo, precio):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Productos
            SET nombre=?, id_categoria=?, id_proveedor=?, 
                unidad_medida=?, stock_minimo=?, precio_unitario=?
            WHERE id_producto=?
        """, (nombre, id_categoria, id_proveedor, unidad, stock_minimo, precio, id_producto))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar producto:", e)
        return False
    finally:
        conn.close()


def eliminar_producto(id_producto):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE Productos SET estado = 'Inactivo' WHERE id_producto = ?", (id_producto,))
        conn.commit()
        return True
    except Exception as e:
        print("Error al eliminar producto:", e)
        return False
    finally:
        conn.close()

def cambiar_estado_producto(id_producto, nuevo_estado):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Productos
            SET estado = ?
            WHERE id_producto = ?
        """, (nuevo_estado, id_producto))
        conn.commit()
        return True
    except Exception as e:
        print("Error al cambiar estado del producto:", e)
        return False
    finally:
        conn.close()



# =====================================================
#   CATEGORÍAS
# =====================================================

def obtener_categorias_todas():
    conn = get_connection()
    categorias = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria, nombre, descripcion FROM Categorias ORDER BY id_categoria DESC")
        for row in cursor.fetchall():
            categorias.append({
                "id": row.id_categoria,
                "nombre": row.nombre,
                "descripcion": row.descripcion
            })
    finally:
        conn.close()
    return categorias

def agregar_categoria(nombre, descripcion):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Categorias (nombre, descripcion)
            VALUES (?, ?)
        """, (nombre, descripcion))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar categoría:", e)
        return False
    finally:
        conn.close()


def obtener_categoria_por_id(id_categoria):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_categoria, nombre, descripcion
            FROM Categorias
            WHERE id_categoria = ?
        """, (id_categoria,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row.id_categoria,
            "nombre": row.nombre,
            "descripcion": row.descripcion
        }
    finally:
        conn.close()


def actualizar_categoria(id_categoria, nombre, descripcion):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Categorias
            SET nombre = ?, descripcion = ?
            WHERE id_categoria = ?
        """, (nombre, descripcion, id_categoria))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar categoría:", e)
        return False
    finally:
        conn.close()


def eliminar_categoria(id_categoria):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Categorias WHERE id_categoria = ?", (id_categoria,))
        conn.commit()
        return True
    except Exception as e:
        print("Error al eliminar categoría:", e)
        return False
    finally:
        conn.close()


# =====================================================
#   PROVEEDORES
# =====================================================

def obtener_proveedores_todos():
    conn = get_connection()
    proveedores = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_proveedor, nombre, telefono, direccion, correo FROM Proveedores ORDER BY id_proveedor DESC")
        for r in cursor.fetchall():
            proveedores.append({
                "id": r.id_proveedor,
                "nombre": r.nombre,
                "telefono": r.telefono,
                "direccion": r.direccion,
                "correo": r.correo
            })
    finally:
        conn.close()
    return proveedores


def agregar_proveedor(nombre, telefono, direccion, correo):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Proveedores (nombre, telefono, direccion, correo)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, direccion, correo))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar proveedor:", e)
        return False
    finally:
        conn.close()


def obtener_proveedor_por_id(id_proveedor):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_proveedor, nombre, telefono, direccion, correo
            FROM Proveedores
            WHERE id_proveedor = ?
        """, (id_proveedor,))
        r = cursor.fetchone()
        if not r:
            return None
        return {
            "id": r.id_proveedor,
            "nombre": r.nombre,
            "telefono": r.telefono,
            "direccion": r.direccion,
            "correo": r.correo
        }
    finally:
        conn.close()


def actualizar_proveedor(id_proveedor, nombre, telefono, direccion, correo):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Proveedores
            SET nombre=?, telefono=?, direccion=?, correo=?
            WHERE id_proveedor=?
        """, (nombre, telefono, direccion, correo, id_proveedor))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar proveedor:", e)
        return False
    finally:
        conn.close()


def eliminar_proveedor(id_proveedor):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Proveedores WHERE id_proveedor = ?", (id_proveedor,))
        conn.commit()
        return True
    except Exception as e:
        print("Error al eliminar proveedor:", e)
        return False
    finally:
        conn.close()


# =====================================================
#   CLIENTES
# =====================================================

def obtener_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre, telefono, direccion, correo FROM Clientes ORDER BY id_cliente DESC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": r.id_cliente, "nombre": r.nombre, "telefono": r.telefono, "direccion": r.direccion, "correo": r.correo}
        for r in rows
    ]


def obtener_cliente_por_id(id_cliente):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_cliente, nombre, telefono, direccion, correo
            FROM Clientes
            WHERE id_cliente = ?
        """, (id_cliente,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row.id_cliente,
            "nombre": row.nombre,
            "telefono": row.telefono,
            "direccion": row.direccion,
            "correo": row.correo
        }
    finally:
        conn.close()


def agregar_cliente(nombre, telefono, direccion, correo):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clientes (nombre, telefono, direccion, correo)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, direccion, correo))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar cliente:", e)
        return False
    finally:
        conn.close()


def actualizar_cliente(id_cliente, nombre, telefono, direccion, correo):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Clientes
            SET nombre = ?, telefono = ?, direccion = ?, correo = ?
            WHERE id_cliente = ?
        """, (nombre, telefono, direccion, correo, id_cliente))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar cliente:", e)
        return False
    finally:
        conn.close()


def eliminar_cliente(id_cliente):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clientes WHERE id_cliente = ?", (id_cliente,))
        conn.commit()
        return True
    except Exception as e:
        print("Error al eliminar cliente:", e)
        return False
    finally:
        conn.close()


# =====================================================
#   FACTURAS
# =====================================================

def obtener_facturas():
    conn = get_connection()
    facturas = []
    try:
        cursor = conn.cursor()
        query = """
            SELECT f.id_factura, c.nombre AS cliente, 
                   f.fecha_factura, f.total, f.tipo_factura, f.observaciones
            FROM Facturas f
            INNER JOIN Clientes c ON f.id_cliente = c.id_cliente
            ORDER BY f.id_factura DESC
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            facturas.append({
                "id": row.id_factura,
                "cliente": row.cliente,
                "fecha": row.fecha_factura.strftime("%d/%m/%Y %H:%M"),
                "total": float(row.total),
                "tipo": row.tipo_factura,
                "observaciones": row.observaciones
            })
    finally:
        conn.close()
    return facturas


def agregar_factura(cliente_id, fecha, total):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Facturas (id_cliente, fecha_factura, total)
            VALUES (?, ?, ?)
        """, (cliente_id, fecha, total))
        cursor.execute("SELECT SCOPE_IDENTITY()")
        factura_id = cursor.fetchone()[0]
        conn.commit()
        return factura_id
    except Exception as e:
        print("Error al agregar factura:", e)
        conn.rollback()
        return None
    finally:
        conn.close()


def agregar_detalle_factura(factura_id, producto_id, cantidad, precio):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Detalle_Factura (id_factura, id_producto, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
        """, (factura_id, producto_id, cantidad, precio))
        conn.commit()
    except Exception as e:
        print("Error al agregar detalle de factura:", e)
        conn.rollback()
    finally:
        conn.close()


def obtener_factura_por_id(id_factura):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.id_factura, c.nombre AS cliente, f.fecha_factura, f.total, 
                   f.tipo_factura, f.observaciones
            FROM Facturas f
            INNER JOIN Clientes c ON f.id_cliente = c.id_cliente
            WHERE f.id_factura = ?
        """, (id_factura,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row.id_factura,
            "cliente": row.cliente,
            "fecha": row.fecha_factura.strftime("%d/%m/%Y %H:%M"),
            "total": float(row.total),
            "tipo": row.tipo_factura,
            "observaciones": row.observaciones
        }
    finally:
        conn.close()


def obtener_detalles_factura(id_factura):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.nombre AS producto, d.cantidad, d.precio_unitario
            FROM Detalle_Factura d
            INNER JOIN Productos p ON d.id_producto = p.id_producto
            WHERE d.id_factura = ?
        """, (id_factura,))
        rows = cursor.fetchall()
        return [
            {
                "producto": r.producto,
                "cantidad": r.cantidad,
                "precio_unitario": float(r.precio_unitario),
                "subtotal": float(r.cantidad * r.precio_unitario)
            }
            for r in rows
        ]
    finally:
        conn.close()

# =====================================================
#   REPORTES / VENTAS
# =====================================================

def obtener_ventas(fecha_inicio=None, fecha_fin=None, id_cliente=None):
    """
    Retorna una lista de facturas (ventas) con filtros opcionales:
    - fecha_inicio: YYYY-MM-DD
    - fecha_fin: YYYY-MM-DD
    - id_cliente: int
    """
    conn = get_connection()
    ventas = []
    try:
        cursor = conn.cursor()
        query = """
            SELECT f.id_factura, c.nombre AS cliente, 
                   f.fecha_factura, f.total, f.tipo_factura, f.observaciones
            FROM Facturas f
            INNER JOIN Clientes c ON f.id_cliente = c.id_cliente
            WHERE f.tipo_factura = 'Venta'
        """
        params = []

        # Filtro por fecha
        if fecha_inicio:
            query += " AND f.fecha_factura >= ?"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND f.fecha_factura <= ?"
            params.append(fecha_fin)

        # Filtro por cliente
        if id_cliente:
            query += " AND f.id_cliente = ?"
            params.append(id_cliente)

        query += " ORDER BY f.fecha_factura DESC"

        cursor.execute(query, params)

        for row in cursor.fetchall():
            ventas.append({
                "id": row.id_factura,
                "cliente": row.cliente,
                "fecha": row.fecha_factura.strftime("%d/%m/%Y %H:%M"),
                "total": float(row.total),
                "observaciones": row.observaciones
            })
    finally:
        conn.close()
    return ventas


# =====================================================
#   MOVIMIENTOS DE INVENTARIO
# =====================================================

def agregar_movimiento(id_producto, tipo_movimiento, cantidad, observaciones):
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Obtener stock actual y mínimo
        cursor.execute("SELECT stock_actual, stock_minimo FROM Productos WHERE id_producto = ?", (id_producto,))
        row = cursor.fetchone()
        if not row:
            return False, "Producto no encontrado"
        stock_actual = float(row.stock_actual)
        stock_minimo = float(row.stock_minimo)

        # Validación: no permitir salida mayor al stock disponible
        if tipo_movimiento == "Salida" and cantidad > stock_actual:
            return False, f"No se puede registrar la salida. Stock disponible: {stock_actual}"

        # Registrar movimiento
        cursor.execute("""
            INSERT INTO Movimientos_Inventario (id_producto, tipo_movimiento, cantidad, observaciones)
            VALUES (?, ?, ?, ?)
        """, (id_producto, tipo_movimiento, cantidad, observaciones))

        # Actualizar stock
        nuevo_stock = stock_actual - cantidad if tipo_movimiento == "Salida" else stock_actual + cantidad
        cursor.execute("UPDATE Productos SET stock_actual = ? WHERE id_producto = ?", (nuevo_stock, id_producto))

        # Aviso si stock por debajo del mínimo
        mensaje_aviso = ""
        if tipo_movimiento == "Salida" and nuevo_stock <= stock_minimo:
            mensaje_aviso = f"¡Atención! Stock actual ({nuevo_stock}) ha llegado al mínimo ({stock_minimo})."

        conn.commit()
        return True, mensaje_aviso or "Movimiento registrado correctamente"
    finally:
        conn.close()



def obtener_movimientos():
    conn = get_connection()
    movimientos = []
    try:
        cursor = conn.cursor()
        query = """
            SELECT m.id_movimiento, p.nombre AS producto, m.tipo_movimiento, m.cantidad,
                   m.fecha_movimiento, m.observaciones
            FROM Movimientos_Inventario m
            INNER JOIN Productos p ON m.id_producto = p.id_producto
            ORDER BY m.fecha_movimiento DESC
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            movimientos.append({
                "id": row.id_movimiento,
                "producto": row.producto,
                "tipo": row.tipo_movimiento,
                "cantidad": float(row.cantidad),
                "fecha": row.fecha_movimiento.strftime("%d/%m/%Y %H:%M"),
                "observaciones": row.observaciones
            })
    finally:
        conn.close()
    return movimientos
