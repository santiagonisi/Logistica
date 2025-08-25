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
    cliente_id = request.form['cliente_id']
    vehiculo_id = request.form['vehiculo_id']
    equipo_id = request.form.get('equipo_id') or None
    chofer = request.form['chofer']
    material = request.form['material']
    fecha = request.form['fecha']
    hora_inicio = request.form['hora_inicio']
    hora_fin = request.form['hora_fin']
    nueva = Asignacion(
        cliente_id=cliente_id,
        vehiculo_id=vehiculo_id,
        equipo_id=equipo_id if equipo_id else None,
        chofer=chofer,
        material=material,
        fecha=datetime.strptime(fecha, '%Y-%m-%d'),
        hora_inicio=datetime.strptime(hora_inicio, '%H:%M').time(),
        hora_fin=datetime.strptime(hora_fin, '%H:%M').time()
    )
    db.session.add(nueva)
    db.session.commit()
    flash('Asignación agregada', 'success')
    return redirect(url_for('main.asignaciones'))

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
    asignaciones = Asignacion.query.order_by(Asignacion.fecha.desc()).all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Asignaciones"
    # Encabezados, incluye Observaciones
    ws.append([
        "ID", "Obra", "Vehículo", "Chofer", "Material", "Fecha",
        "Inicio", "Fin", "Observaciones"
    ])
    for a in asignaciones:
        ws.append([
            a.id,
            a.cliente.nombre if a.cliente else "",
            f"{a.vehiculo.codigo} ({a.vehiculo.dominio})" if a.vehiculo else "",
            a.chofer,
            a.material,
            a.fecha.strftime('%Y-%m-%d') if a.fecha else "",
            a.hora_inicio.strftime('%H:%M') if a.hora_inicio else "",
            a.hora_fin.strftime('%H:%M') if a.hora_fin else "",
            a.observaciones or ""
        ])
    from io import BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(
        output,
        download_name="asignaciones.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@main.route('/asignaciones')
def asignaciones():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    asignaciones_query = Asignacion.query.order_by(Asignacion.fecha.desc())
    total = asignaciones_query.count()
    total_pages = max((total + per_page - 1) // per_page, 1)
    asignaciones = asignaciones_query.offset((page - 1) * per_page).limit(per_page).all()
    clientes = Cliente.query.all()
    vehiculos = Vehiculo.query.all()
    return render_template(
        'asignaciones.html',
        asignaciones=asignaciones,
        clientes=clientes,
        vehiculos=vehiculos,
        page=page,
        total_pages=total_pages
    )

@main.route('/asignaciones/observaciones/<int:id>', methods=['POST'])
def editar_observaciones(id):
    a = Asignacion.query.get_or_404(id)
    a.observaciones = request.form['observaciones'].strip()
    db.session.commit()
    flash('Observaciones actualizadas', 'success')
    return redirect(url_for('main.asignaciones'))
