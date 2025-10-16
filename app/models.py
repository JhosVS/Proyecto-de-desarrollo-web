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
    """Obtiene todos los productos usando sp_ObtenerProductos"""
    conn = get_connection()
    productos = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProductos")
        
        for row in cursor.fetchall():
            productos.append({
                "id": row.id_producto,
                "nombre": row.nombre,
                "categoria": row.categoria,
                "proveedor": row.proveedor,
                "unidad": row.unidad_medida,
                "stock": float(row.stock_actual),
                "stock_minimo": float(row.stock_minimo),
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
    """Agrega producto usando sp_AgregarProducto"""
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


def obtener_producto_por_id(id_producto):
    """Obtiene un producto por ID usando sp_ObtenerProductoPorId"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProductoPorId @id_producto=?", (id_producto,))
        
        row = cursor.fetchone()
        if not row:
            return None

        return {
            "id": row.id_producto,
            "nombre": row.nombre,
            "id_categoria": row.id_categoria,
            "id_proveedor": row.id_proveedor,
            "unidad": row.unidad_medida,
            "stock": float(row.stock_actual),
            "stock_minimo": float(row.stock_minimo),
            "precio": float(row.precio_unitario),
            "estado": row.estado
        }
    except Exception as e:
        print("Error en obtener_producto_por_id:", e)
        return None
    finally:
        conn.close()


def actualizar_producto(id_producto, nombre, id_categoria, id_proveedor, unidad, stock_minimo, precio):
    """Actualiza producto usando sp_ActualizarProducto"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_ActualizarProducto
                @id_producto=?, @nombre=?, @id_categoria=?, @id_proveedor=?,
                @unidad_medida=?, @stock_minimo=?, @precio_unitario=?
        """, (id_producto, nombre, id_categoria, id_proveedor, unidad, stock_minimo, precio))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar producto:", e)
        return False
    finally:
        conn.close()


def eliminar_producto(id_producto):
    """Elimina (inactiva) producto"""
    return cambiar_estado_producto(id_producto, 'Inactivo')


def cambiar_estado_producto(id_producto, nuevo_estado):
    """Cambia estado usando sp_CambiarEstadoProducto"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_CambiarEstadoProducto @id_producto=?, @nuevo_estado=?", 
                      (id_producto, nuevo_estado))
        conn.commit()
        return True
    except Exception as e:
        print("Error al cambiar estado:", e)
        return False
    finally:
        conn.close()



# =====================================================
#   CATEGORÍAS
# =====================================================

def obtener_categorias():
    """Lista simple para dropdowns"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM Categorias ORDER BY nombre")
        return [{"id": r.id_categoria, "nombre": r.nombre} for r in cursor.fetchall()]
    finally:
        conn.close()

def obtener_categorias_todas():
    """Obtiene todas las categorías con detalles usando sp_ObtenerCategorias"""
    conn = get_connection()
    categorias = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerCategorias")
        
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
    """Agrega categoría usando sp_AgregarCategoria"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_AgregarCategoria @nombre=?, @descripcion=?", 
                      (nombre, descripcion))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar categoría:", e)
        return False
    finally:
        conn.close()

def obtener_categoria_por_id(id_categoria):
    """Obtiene una categoría por ID usando sp_ObtenerCategoriaPorId"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerCategoriaPorId @id_categoria=?", (id_categoria,))
        
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
    """Actualiza categoría usando sp_ActualizarCategoria"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ActualizarCategoria @id_categoria=?, @nombre=?, @descripcion=?",
                      (id_categoria, nombre, descripcion))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar categoría:", e)
        return False
    finally:
        conn.close()


def eliminar_categoria(id_categoria):
    """Elimina categoría usando sp_EliminarCategoria"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_EliminarCategoria @id_categoria=?", (id_categoria,))
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
    """Obtiene todos los proveedores usando sp_ObtenerProveedores"""
    conn = get_connection()
    proveedores = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProveedores")
        
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
    """Agrega proveedor usando sp_AgregarProveedor"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_AgregarProveedor @nombre=?, @telefono=?, @direccion=?, @correo=?",
                      (nombre, telefono, direccion, correo))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar proveedor:", e)
        return False
    finally:
        conn.close()


def obtener_proveedor_por_id(id_proveedor):
    """Obtiene proveedor por ID usando sp_ObtenerProveedorPorId"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProveedorPorId @id_proveedor=?", (id_proveedor,))
        
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
    """Actualiza proveedor usando sp_ActualizarProveedor"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_ActualizarProveedor 
                @id_proveedor=?, @nombre=?, @telefono=?, @direccion=?, @correo=?
        """, (id_proveedor, nombre, telefono, direccion, correo))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar proveedor:", e)
        return False
    finally:
        conn.close()


def eliminar_proveedor(id_proveedor):
    """Elimina proveedor usando sp_EliminarProveedor"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_EliminarProveedor @id_proveedor=?", (id_proveedor,))
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
    """Obtiene todos los clientes usando sp_ObtenerClientes"""
    conn = get_connection()
    clientes = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerClientes")
        
        for r in cursor.fetchall():
            clientes.append({
                "id": r.id_cliente,
                "nombre": r.nombre,
                "telefono": r.telefono,
                "direccion": r.direccion,
                "correo": r.correo
            })
    finally:
        conn.close()
    return clientes


def obtener_cliente_por_id(id_cliente):
    """Obtiene cliente por ID usando sp_ObtenerClientePorId"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerClientePorId @id_cliente=?", (id_cliente,))
        
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
    """Agrega cliente usando sp_AgregarCliente"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_AgregarCliente @nombre=?, @telefono=?, @direccion=?, @correo=?",
                      (nombre, telefono, direccion, correo))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar cliente:", e)
        return False
    finally:
        conn.close()

def actualizar_cliente(id_cliente, nombre, telefono, direccion, correo):
    """Actualiza cliente usando sp_ActualizarCliente"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_ActualizarCliente 
                @id_cliente=?, @nombre=?, @telefono=?, @direccion=?, @correo=?
        """, (id_cliente, nombre, telefono, direccion, correo))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar cliente:", e)
        return False
    finally:
        conn.close()


def eliminar_cliente(id_cliente):
    """Elimina cliente usando sp_EliminarCliente"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_EliminarCliente @id_cliente=?", (id_cliente,))
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
    """Obtiene todas las facturas usando sp_ObtenerFacturas"""
    conn = get_connection()
    facturas = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerFacturas")
        
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
    """Agrega factura (método simplificado, considera usar sp_RegistrarFactura completo)"""
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
    """Agrega detalle de factura (método simplificado)"""
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
    """Obtiene factura por ID usando sp_ObtenerFacturaPorId"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerFacturaPorId @id_factura=?", (id_factura,))
        
        # Primera consulta: encabezado
        row = cursor.fetchone()
        if not row:
            return None
            
        factura = {
            "id": row.id_factura,
            "cliente": row.cliente,
            "fecha": row.fecha_factura.strftime("%d/%m/%Y %H:%M"),
            "total": float(row.total),
            "tipo": row.tipo_factura,
            "observaciones": row.observaciones
        }
        
        return factura
    finally:
        conn.close()



def obtener_detalles_factura(id_factura):
    """Obtiene detalles de factura (segunda parte de sp_ObtenerFacturaPorId)"""
    conn = get_connection()
    detalles = []
    try:
        cursor = conn.cursor()
        # Ejecutar el procedimiento completo
        cursor.execute("EXEC sp_ObtenerFacturaPorId @id_factura=?", (id_factura,))
        
        # Saltar el primer resultset (encabezado)
        cursor.nextset()
        
        # Obtener el segundo resultset (detalles)
        for r in cursor.fetchall():
            detalles.append({
                "producto": r.producto,
                "cantidad": float(r.cantidad),
                "precio_unitario": float(r.precio_unitario),
                "subtotal": float(r.subtotal)
            })
    finally:
        conn.close()
    return detalles

# =====================================================
#   REPORTES / VENTAS
# =====================================================

def obtener_ventas(fecha_inicio=None, fecha_fin=None, id_cliente=None):
    """Obtiene ventas con filtros usando sp_ObtenerVentas"""
    conn = get_connection()
    ventas = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_ObtenerVentas 
                @fecha_inicio=?, 
                @fecha_fin=?, 
                @id_cliente=?
        """, (fecha_inicio, fecha_fin, id_cliente))
        
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
    """Registra movimiento usando sp_RegistrarMovimiento con OUTPUT"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Ejecutar procedimiento con parámetro OUTPUT
        cursor.execute("""
            DECLARE @mensaje NVARCHAR(500)
            EXEC sp_RegistrarMovimiento 
                @id_producto=?, 
                @tipo_movimiento=?, 
                @cantidad=?, 
                @observaciones=?,
                @mensaje_salida=@mensaje OUTPUT
            SELECT @mensaje
        """, (id_producto, tipo_movimiento, cantidad, observaciones))
        
        # Obtener mensaje de salida
        mensaje = cursor.fetchone()[0]
        conn.commit()
        
        # Retornar True y el mensaje
        return True, mensaje
        
    except Exception as e:
        error_msg = str(e)
        print("Error al registrar movimiento:", error_msg)
        
        # Si el error viene del procedimiento, extraer el mensaje
        if "Stock insuficiente" in error_msg or "bajo mínimo" in error_msg:
            return False, error_msg
        
        return False, "Error al registrar el movimiento"
    finally:
        conn.close()



def obtener_movimientos(fecha_inicio=None, fecha_fin=None, tipo_movimiento=None):
    """Obtiene movimientos con filtros usando sp_ObtenerMovimientos"""
    conn = get_connection()
    movimientos = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_ObtenerMovimientos 
                @fecha_inicio=?, 
                @fecha_fin=?, 
                @tipo_movimiento=?
        """, (fecha_inicio, fecha_fin, tipo_movimiento))
        
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