from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import models
from datetime import datetime
import json

# Definir el blueprint principal
main_bp = Blueprint('main', __name__)

# ==========================
# Página de inicio
# ==========================
@main_bp.route('/')
def inicio():
    return render_template('inicio.html', page_title="Inicio")

# ==========================
# Listado de productos
# ==========================
@main_bp.route('/productos')
def listar_productos():
    productos = models.obtener_productos()
    return render_template('productos.html', productos=productos, page_title="Productos")

# ==========================
# Nuevo producto
# ==========================
@main_bp.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_categoria = request.form['categoria']
        id_proveedor = request.form['proveedor']
        unidad = request.form['unidad']
        stock_inicial = request.form['stock_inicial']
        stock_minimo = request.form['stock_minimo']
        precio = request.form['precio']

        ok = models.agregar_producto(
            nombre, id_categoria, id_proveedor, unidad,
            stock_inicial, stock_minimo, precio
        )
        if ok:
            flash("✅ Producto agregado correctamente.")
        else:
            flash("❌ Error al agregar producto.")
        return redirect(url_for('main.listar_productos'))

    categorias = models.obtener_categorias()
    proveedores = models.obtener_proveedores()
    return render_template(
        'producto_form.html',
        categorias=categorias,
        proveedores=proveedores,
        page_title="Nuevo Producto"
    )

# ==========================
# Editar producto
# ==========================
@main_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_categoria = request.form['categoria']
        id_proveedor = request.form['proveedor']
        unidad = request.form['unidad']
        stock_minimo = request.form['stock_minimo']
        precio = request.form['precio']

        ok = models.actualizar_producto(
            id, nombre, id_categoria, id_proveedor, unidad, stock_minimo, precio
        )
        if ok:
            flash("✅ Producto actualizado correctamente.")
        else:
            flash("❌ Error al actualizar producto.")
        return redirect(url_for('main.listar_productos'))

    producto = models.obtener_producto_por_id(id)
    categorias = models.obtener_categorias()
    proveedores = models.obtener_proveedores()
    return render_template(
        'producto_form.html',
        producto=producto,
        categorias=categorias,
        proveedores=proveedores,
        page_title="Editar Producto"
    )

# ==========================
# Eliminar producto
# ==========================
@main_bp.route('/productos/toggle_estado/<int:id>/<string:estado_actual>')
def toggle_estado_producto(id, estado_actual):
    nuevo_estado = 'Inactivo' if estado_actual == 'Activo' else 'Activo'
    ok = models.cambiar_estado_producto(id, nuevo_estado)

    if ok:
        mensaje = f"✅ Producto {'desactivado' if nuevo_estado == 'Inactivo' else 'activado'} correctamente."
        flash(mensaje)
    else:
        flash("❌ No se pudo actualizar el estado del producto.")

    return redirect(url_for('main.listar_productos'))

# =====================================================
#   CATEGORÍAS
# =====================================================

@main_bp.route('/categorias')
def listar_categorias():
    categorias = models.obtener_categorias_todas()
    return render_template('categorias.html', categorias=categorias, page_title="Categorías")

@main_bp.route('/categorias/nueva', methods=['GET', 'POST'])
def nueva_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        if models.agregar_categoria(nombre, descripcion):
            flash("✅ Categoría agregada correctamente.")
        else:
            flash("❌ Error al agregar categoría.")
        return redirect(url_for('main.listar_categorias'))
    return render_template('categoria_form.html', categoria=None, page_title="Nueva categoría")

@main_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    categoria = models.obtener_categoria_por_id(id)
    if not categoria:
        flash("❌ Categoría no encontrada.")
        return redirect(url_for('main.listar_categorias'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        if models.actualizar_categoria(id, nombre, descripcion):
            flash("✅ Categoría actualizada correctamente.")
        else:
            flash("❌ Error al actualizar categoría.")
        return redirect(url_for('main.listar_categorias'))

    return render_template('categoria_form.html', categoria=categoria, page_title="Editar categoría")

@main_bp.route('/categorias/eliminar/<int:id>')
def eliminar_categoria(id):
    if models.eliminar_categoria(id):
        flash("🗑️ Categoría eliminada.")
    else:
        flash("❌ No se pudo eliminar la categoría.")
    return redirect(url_for('main.listar_categorias'))

# =====================================================
#   PROVEEDORES
# =====================================================

@main_bp.route('/proveedores')
def listar_proveedores():
    proveedores = models.obtener_proveedores_todos()
    return render_template('proveedores.html', proveedores=proveedores, page_title="Proveedores")

@main_bp.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        if models.agregar_proveedor(nombre, telefono, direccion, correo):
            flash("✅ Proveedor agregado correctamente.")
        else:
            flash("❌ Error al agregar proveedor.")
        return redirect(url_for('main.listar_proveedores'))
    return render_template('proveedor_form.html', proveedor=None, page_title="Nuevo proveedor")

@main_bp.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    proveedor = models.obtener_proveedor_por_id(id)
    if not proveedor:
        flash("❌ Proveedor no encontrado.")
        return redirect(url_for('main.listar_proveedores'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        if models.actualizar_proveedor(id, nombre, telefono, direccion, correo):
            flash("✅ Proveedor actualizado correctamente.")
        else:
            flash("❌ Error al actualizar proveedor.")
        return redirect(url_for('main.listar_proveedores'))

    return render_template('proveedor_form.html', proveedor=proveedor, page_title="Editar proveedor")

@main_bp.route('/proveedores/eliminar/<int:id>')
def eliminar_proveedor(id):
    if models.eliminar_proveedor(id):
        flash("🗑️ Proveedor eliminado.")
    else:
        flash("❌ No se pudo eliminar el proveedor.")
    return redirect(url_for('main.listar_proveedores'))

# =====================================================
#   VENTAS
# =====================================================

@main_bp.route("/ventas")
def listar_ventas():
    """Página principal de gestión de ventas y clientes"""
    clientes = models.obtener_clientes()
    ventas = models.obtener_ventas()
    return render_template("ventas.html", 
                         clientes=clientes, 
                         ventas=ventas, 
                         page_title="Gestión de Ventas y Clientes")

@main_bp.route("/ventas/nueva", methods=["GET", "POST"])
def nueva_venta():
    """Registra una nueva venta usando sp_RegistrarVenta (sin usuario)"""
    if request.method == "POST":
        try:
            cliente_id = int(request.form["cliente_id"])
            detalles_json = request.form["detalles"]
            
            print("=== DEBUG VENTA ===")
            print("Cliente ID:", cliente_id)
            print("Detalles JSON:", detalles_json)
            
            # Registrar la venta
            success, mensaje = models.registrar_venta(cliente_id, detalles_json)
            
            print("Resultado:", success, mensaje)
            print("=== FIN DEBUG ===")
            
            if success:
                flash("✅ Venta registrada correctamente.", "success")
                return redirect(url_for("main.listar_ventas"))
            else:
                flash(f"❌ Error al registrar venta: {mensaje}", "error")
                
        except Exception as e:
            print("Error en nueva_venta:", e)
            flash(f"❌ Error en el formulario: {str(e)}", "error")

    return redirect(url_for('main.listar_ventas'))

@main_bp.route("/ventas/<int:id>")
def ver_venta(id):
    """Muestra el detalle de una venta usando sp_ObtenerVentaPorId"""
    venta, detalles = models.obtener_venta_por_id(id)
    if not venta:
        flash("❌ Venta no encontrada.", "error")
        return redirect(url_for('main.listar_ventas'))

    # Pasamos la venta específica y sus detalles al template ventas.html
    clientes = models.obtener_clientes()
    ventas = models.obtener_ventas()  # Para mantener el historial
    
    return render_template(
        "ventas.html", 
        clientes=clientes,
        ventas=ventas,
        venta_especifica=venta,
        detalles_venta=detalles,
        page_title=f"Detalle de Venta #{venta['id']}"
    )

@main_bp.route("/api/ventas/calcular-total", methods=["POST"])
def calcular_total_venta():
    """API para calcular el total de una venta en tiempo real"""
    try:
        data = request.get_json()
        detalles = data.get('detalles', [])
        
        total = 0
        for detalle in detalles:
            cantidad = float(detalle['cantidad'])
            precio = float(detalle['precio'])
            total += cantidad * precio
            
        return jsonify({"success": True, "total": round(total, 2)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@main_bp.route("/api/productos_venta")
def api_productos_venta():
    """API para obtener productos disponibles para venta"""
    try:
        productos = models.obtener_productos_para_venta()
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================================
#   CLIENTES
# =====================================================

@main_bp.route("/nuevo_cliente", methods=["GET", "POST"])
def nuevo_cliente():
    """Crea un nuevo cliente usando sp_AgregarCliente"""
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]
        
        if models.agregar_cliente(nombre, telefono, direccion, correo):
            flash("✅ Cliente agregado correctamente.", "success")
        else:
            flash("❌ Error al agregar cliente.", "error")
        return redirect(url_for('main.listar_ventas'))
    
    return render_template("cliente_form.html", cliente=None, page_title="Nuevo Cliente")

@main_bp.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    """Edita un cliente usando sp_ActualizarCliente"""
    cliente = models.obtener_cliente_por_id(id)
    if not cliente:
        flash("❌ Cliente no encontrado.", "error")
        return redirect(url_for('main.listar_ventas'))

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]
        
        if models.actualizar_cliente(id, nombre, telefono, direccion, correo):
            flash("✅ Cliente actualizado correctamente.", "success")
        else:
            flash("❌ Error al actualizar cliente.", "error")
        return redirect(url_for('main.listar_ventas'))

    return render_template("cliente_form.html", cliente=cliente, page_title="Editar Cliente")

@main_bp.route("/eliminar_cliente/<int:id>")
def eliminar_cliente(id):
    """Elimina un cliente usando sp_EliminarCliente"""
    if models.eliminar_cliente(id):
        flash("🗑️ Cliente eliminado correctamente.", "success")
    else:
        flash("❌ No se pudo eliminar el cliente.", "error")
    return redirect(url_for('main.listar_ventas'))

# =====================================================
#   DASHBOARD
# =====================================================

@main_bp.route("/dashboard")
def dashboard():
    """Dashboard con gráficas del sistema"""
    # Datos para las gráficas usando procedimientos almacenados
    datos = {
        "total_productos": models.obtener_total_productos(),
        "total_ventas": models.obtener_total_ventas(),
        "total_clientes": models.obtener_total_clientes(),
        "ventas_por_mes": models.obtener_ventas_ultimos_meses(6),
        "productos_mas_vendidos": models.obtener_productos_mas_vendidos(5),
        "stock_bajo": models.obtener_productos_stock_bajo()
    }
    return render_template("dashboard.html", datos=datos, page_title="Dashboard")

# =====================================================
#   REABASTECIMIENTO DE INVENTARIO
# =====================================================

@main_bp.route("/inventario/reabastecer", methods=["GET", "POST"])
def reabastecer_inventario():
    """Reabastece el inventario de productos"""
    productos = models.obtener_productos()
    productos_bajos = models.obtener_productos_stock_bajo()  # <- NUEVA LÍNEA
    producto_seleccionado = request.args.get('producto_id')
    
    if request.method == "POST":
        try:
            producto_id = int(request.form["producto_id"])
            cantidad = float(request.form["cantidad"])
            observaciones = request.form.get("observaciones", "Reabastecimiento de inventario")
            
            # Registrar el movimiento de entrada
            success, mensaje = models.agregar_movimiento(
                producto_id, 'Entrada', cantidad, observaciones
            )
            
            if success:
                flash(f"✅ {mensaje}", "success")
            else:
                flash(f"❌ {mensaje}", "error")
                
            return redirect(url_for('main.reabastecer_inventario'))
            
        except Exception as e:
            flash(f"❌ Error en el formulario: {str(e)}", "error")
    
    return render_template("reabastecer.html", 
                         productos=productos, 
                         productos_bajos=productos_bajos,  # <- NUEVO PARÁMETRO
                         producto_seleccionado=producto_seleccionado,
                         page_title="Reabastecer Inventario")