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


@main.route('/asignaciones/agregar', methods=['POST'])
def agregar_asignacion():
    try:
        nueva = Asignacion(
            cliente_id=int(request.form['cliente_id']),
            vehiculo_id=int(request.form['vehiculo_id']),
            chofer=request.form['chofer'].strip(),
            material=request.form['material'].strip(),
            fecha=datetime.strptime(request.form['fecha'], "%Y-%m-%d").date(),
            hora_inicio=datetime.strptime(request.form['hora_inicio'], "%H:%M").time(),
            hora_fin=datetime.strptime(request.form['hora_fin'], "%H:%M").time(),
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Asignación creada correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear la asignación: {e}', 'danger')
    return redirect(url_for('main.index'))


@main.route('/asignaciones/editar/<int:id>', methods=['POST'])
def editar_asignacion(id):
    a = Asignacion.query.get_or_404(id)
    try:
        a.cliente_id = int(request.form['cliente_id'])
        a.vehiculo_id = int(request.form['vehiculo_id'])
        a.chofer = request.form['chofer'].strip()
        a.material = request.form['material'].strip()
        a.fecha = datetime.strptime(request.form['fecha'], "%Y-%m-%d").date()
        a.hora_inicio = datetime.strptime(request.form['hora_inicio'], "%H:%M").time()
        a.hora_fin = datetime.strptime(request.form['hora_fin'], "%H:%M").time()
        db.session.commit()
        flash('Asignación actualizada', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar: {e}', 'danger')
    return redirect(url_for('main.index')) 


@main.route('/asignaciones/eliminar/<int:id>')
def eliminar_asignacion(id):
    a = Asignacion.query.get_or_404(id)
    try:
        db.session.delete(a)
        db.session.commit()
        flash('Asignación eliminada', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'No se pudo eliminar: {e}', 'danger')
    return redirect(url_for('main.index')) 

