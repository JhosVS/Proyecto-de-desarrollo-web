from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import models

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
#   CLIENTES
# =====================================================

@main_bp.route("/clientes")
def listar_clientes():
    clientes = models.obtener_clientes()
    return render_template("clientes.html", clientes=clientes)


@main_bp.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]
        models.agregar_cliente(nombre, telefono, direccion, correo)
        return redirect(url_for('main.listar_clientes'))
    return render_template("cliente_form.html", cliente=None)


@main_bp.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    cliente = models.obtener_cliente_por_id(id)
    if not cliente:
        return "Cliente no encontrado", 404

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]
        models.actualizar_cliente(id, nombre, telefono, direccion, correo)
        return redirect(url_for("main.listar_clientes"))

    return render_template("cliente_form.html", cliente=cliente)


@main_bp.route("/clientes/eliminar/<int:id>")
def eliminar_cliente(id):
    models.eliminar_cliente(id)
    return redirect(url_for("main.listar_clientes"))


# =====================================================
#   FACTURAS
# =====================================================

@main_bp.route("/facturas")
def listar_facturas():
    facturas = models.obtener_facturas()
    return render_template("facturas.html", facturas=facturas)

from datetime import datetime

@main_bp.route("/facturas/nueva", methods=["GET", "POST"])
def nueva_factura():
    clientes = models.obtener_clientes()
    productos = models.obtener_productos()

    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        fecha = request.form["fecha"]
        total = request.form["total"]
        detalles = request.form.getlist("detalles[]")

        factura_id = models.agregar_factura(cliente_id, fecha, total)

        for detalle_str in detalles:
            producto_id, cantidad, precio = detalle_str.split("|")
            models.agregar_detalle_factura(factura_id, producto_id, cantidad, precio)

        return redirect(url_for("main.listar_facturas"))

    # 👇 Pasamos la fecha actual a la plantilla
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    return render_template("factura_form.html", clientes=clientes, productos=productos, fecha_actual=fecha_actual)

@main_bp.route("/facturas/<int:id>")
def ver_factura(id):
    factura = models.obtener_factura_por_id(id)
    if not factura:
        return "Factura no encontrada", 404

    detalles = models.obtener_detalles_factura(id)
    return render_template("factura_detalle.html", factura=factura, detalles=detalles)


# =====================================================
#   REPORTES / VENTAS
# =====================================================

@main_bp.route("/ventas", methods=["GET", "POST"])
def reportes_ventas():
    clientes = models.obtener_clientes()
    fecha_inicio = request.form.get("fecha_inicio")
    fecha_fin = request.form.get("fecha_fin")
    id_cliente = request.form.get("id_cliente")

    # Convertir id_cliente a entero si se seleccionó
    if id_cliente and id_cliente != "":
        id_cliente = int(id_cliente)
    else:
        id_cliente = None

    ventas = models.obtener_ventas(fecha_inicio, fecha_fin, id_cliente)

    return render_template(
        "reportes_ventas.html",
        clientes=clientes,
        ventas=ventas,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        id_cliente=id_cliente
    )


# =====================================================
#   MOVIMIENTOS DE INVENTARIO
# =====================================================

@main_bp.route("/movimientos")
def listar_movimientos():
    movimientos = models.obtener_movimientos()
    return render_template("movimientos.html", movimientos=movimientos)


@main_bp.route("/movimientos/nuevo", methods=["GET", "POST"])
def nuevo_movimiento():
    productos = models.obtener_productos()

    if request.method == "POST":
        id_producto = int(request.form.get("id_producto", 0))
        tipo_movimiento = request.form.get("tipo_movimiento")
        cantidad = float(request.form.get("cantidad", 0))
        observaciones = request.form.get("observaciones", "")

        success, mensaje = models.agregar_movimiento(id_producto, tipo_movimiento, cantidad, observaciones)
        if success:
            flash(mensaje, "warning" if "¡Atención!" in mensaje else "success")
            return redirect(url_for("main.listar_movimientos"))
        else:
            flash(mensaje, "danger")
            return redirect(url_for("main.nuevo_movimiento"))



    return render_template("movimiento_form.html", productos=productos)
