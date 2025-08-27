CREATE TABLE asignacion_new (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    vehiculo_id INTEGER,
    equipo_id INTEGER,
    chofer TEXT,
    material TEXT,
    fecha DATE,
    hora_inicio TIME,
    hora_fin TIME,
    observaciones TEXT,
    vehiculo_tercero TEXT,
    equipo_tercero TEXT,
    empresa_tercero TEXT,
    es_tercero INTEGER
);

INSERT INTO asignacion_new SELECT * FROM asignacion;
DROP TABLE asignacion;
ALTER TABLE asignacion_new RENAME TO asignacion;