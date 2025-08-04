from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dominio = db.Column(db.String(10), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(10), nullable=False)  # Activo / Inactivo

    def __repr__(self):
        return f'<Vehiculo {self.dominio}>'
