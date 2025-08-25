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

class Asignacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable=True)
    chofer = db.Column(db.String(100), nullable=False)
    material = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    vehiculo_tercero = db.Column(db.String(100), nullable=True)
    equipo_tercero = db.Column(db.String(100), nullable=True)
    empresa_tercero = db.Column(db.String(100), nullable=True)
    es_tercero = db.Column(db.Boolean, default=False)

    cliente = db.relationship('Cliente', backref=db.backref('asignaciones', lazy=True))
    vehiculo = db.relationship('Vehiculo', foreign_keys=[vehiculo_id])
    equipo = db.relationship('Vehiculo', foreign_keys=[equipo_id])
