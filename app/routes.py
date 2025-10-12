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
# Movimientos (pendiente)
# ==========================
@main_bp.route('/movimientos')
def listar_movimientos():
    return render_template('movimientos.html', page_title="Movimientos de Inventario")

# ==========================
# Reportes (pendiente)
# ==========================
@main_bp.route('/reportes')
def reportes():
    return render_template('reportes.html', page_title="Reportes")
