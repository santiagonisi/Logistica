from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False, unique=True)  # Código interno
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    dominio = db.Column(db.String(10), nullable=False, unique=True)  # Patente
    estado = db.Column(db.String(10), nullable=False)  # Activo / Inactivo

    def __repr__(self):
        return f'<Vehiculo {self.codigo}>'
