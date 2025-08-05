from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Vehiculo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/vehiculos')
def vehiculos():
    lista = Vehiculo.query.all()
    return render_template('vehiculo.html', vehiculos=lista)

@main.route('/vehiculos/agregar', methods=['POST'])
def agregar_vehiculo():
    nuevo = Vehiculo(
        dominio=request.form['dominio'],
        marca=request.form['marca'],
        modelo=request.form['modelo'],
        tipo=request.form['tipo'],
        anio=int(request.form['anio']),
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

@main.route('/rutas')
def rutas():
    return render_template('rutas.html')
