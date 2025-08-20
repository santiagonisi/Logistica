from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from .models import db, Vehiculo, Cliente, Asignacion
from datetime import datetime
from openpyxl import Workbook
import io

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
    clientes = Cliente.query.filter_by(estado="Activo").order_by(Cliente.nombre).all()
    vehiculos = Vehiculo.query.order_by(Vehiculo.codigo).all()
    asignaciones = Asignacion.query.order_by(
        Asignacion.fecha.desc(), Asignacion.hora_inicio.desc()
    ).all()
    return render_template(
        'asignaciones.html',
        clientes=clientes,
        vehiculos=vehiculos,
        asignaciones=asignaciones
    )


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

@main.route('/asignaciones/exportar')
def exportar_asignaciones():
    asignaciones = Asignacion.query.order_by(
        Asignacion.cliente_id, Asignacion.fecha, Asignacion.hora_inicio
    ).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Asignaciones"
    headers = ["Obra", "Vehículo", "Chofer", "Material", "Fecha", "Hora inicio", "Hora fin"]
    ws.append(headers)

    for a in asignaciones:
        ws.append([
            a.cliente.nombre,
            a.vehiculo.codigo,
            a.chofer,
            a.material,
            a.fecha.strftime('%Y-%m-%d'),
            a.hora_inicio.strftime('%H:%M'),
            a.hora_fin.strftime('%H:%M'),
        ])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='asignaciones.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
