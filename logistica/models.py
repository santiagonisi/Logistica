from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False, unique=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    dominio = db.Column(db.String(10), nullable=False, unique=True)
    estado = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Vehiculo {self.codigo}>'

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    comitente = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(10), nullable=False, default="Activo")

    def __repr__(self):
        return f'<Cliente {self.nombre}>'
