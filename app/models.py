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
                   p.unidad_medida, p.stock_actual, p.precio_unitario, p.estado
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
