from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Vehiculo, Cliente

main = Blueprint('main', __name__)

def paginar_query(query, page, per_page=10):
    total = query.count()
    total_pages = max((total + per_page - 1) // per_page, 1)
    
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return items, total, total_pages, page


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/vehiculos')
def vehiculos():
    page = request.args.get('page', 1, type=int)
    query = Vehiculo.query.order_by(Vehiculo.id)
    vehiculos, total, total_pages, page = paginar_query(query, page)
    return render_template('vehiculo.html',
                           vehiculos=vehiculos,
                           page=page,
                           total_pages=total_pages)


@main.route('/vehiculos/agregar', methods=['POST'])
def agregar_vehiculo():
    nuevo = Vehiculo(
        codigo=request.form['codigo'],
        marca=request.form['marca'],
        modelo=request.form['modelo'],
        tipo=request.form['tipo'],
        dominio=request.form['dominio'],
        estado=request.form['estado']
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('main.vehiculos'))


@main.route('/vehiculos/eliminar/<int:id>')
def eliminar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    db.session.delete(vehiculo)
    db.session.commit()
    return redirect(url_for('main.vehiculos'))


@main.route('/vehiculos/editar/<int:id>', methods=['POST'])
def editar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    vehiculo.codigo = request.form['codigo']
    vehiculo.marca = request.form['marca']
    vehiculo.modelo = request.form['modelo']
    vehiculo.tipo = request.form['tipo']
    vehiculo.dominio = request.form['dominio']
    vehiculo.estado = request.form['estado']
    db.session.commit()
    return redirect(url_for('main.vehiculos'))


@main.route('/rutas')
def rutas():
    return render_template('rutas.html')


@main.route('/clientes')
def clientes():
    page = request.args.get('page', 1, type=int)
    query = Cliente.query.filter_by(estado="Activo").order_by(Cliente.id)
    clientes, total, total_pages, page = paginar_query(query, page)
    return render_template('clientes.html',
                           clientes=clientes,
                           page=page,
                           total_pages=total_pages)


@main.route('/clientes/baja/<int:id>')
def baja_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.estado = "Inactivo"
    db.session.commit()
    return redirect(url_for('main.clientes'))


@main.route('/clientes/agregar', methods=['POST'])
def agregar_cliente():
    nuevo = Cliente(
        nombre=request.form['nombre'],
        ubicacion=request.form['ubicacion'],
        comitente=request.form['comitente'],
        estado="Activo"
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('main.clientes'))
