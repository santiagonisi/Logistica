"""
Script para agregar índices a la base de datos SQLite
Esto mejora significativamente la velocidad de búsquedas y filtrados
"""
from logistica import create_app
from logistica.models import db

def agregar_indices():
    app = create_app()
    with app.app_context():
        with db.engine.connect() as conn:
            indices = [
                "CREATE INDEX IF NOT EXISTS idx_asignacion_fecha ON asignacion(fecha);",
                "CREATE INDEX IF NOT EXISTS idx_asignacion_cliente_id ON asignacion(cliente_id);",
                "CREATE INDEX IF NOT EXISTS idx_asignacion_es_tercero ON asignacion(es_tercero);",
                "CREATE INDEX IF NOT EXISTS idx_asignacion_lluvia ON asignacion(lluvia);",
                "CREATE INDEX IF NOT EXISTS idx_asignacion_fecha_es_tercero ON asignacion(fecha, es_tercero);",
                
                "CREATE INDEX IF NOT EXISTS idx_cliente_estado ON cliente(estado);",
                "CREATE INDEX IF NOT EXISTS idx_cliente_nombre ON cliente(nombre);",
                
                "CREATE INDEX IF NOT EXISTS idx_vehiculo_estado ON vehiculo(estado);",
                "CREATE INDEX IF NOT EXISTS idx_vehiculo_codigo ON vehiculo(codigo);",
                
                "CREATE INDEX IF NOT EXISTS idx_comitente_estado ON comitente(estado);",
                "CREATE INDEX IF NOT EXISTS idx_comitente_nombre ON comitente(nombre);",
            ]
            
            try:
                for idx_sql in indices:
                    conn.execute(db.text(idx_sql))
                    conn.commit()
                    print(f"✓ {idx_sql.split('CREATE INDEX IF NOT EXISTS ')[1].split(' ON')[0]}")
                
                print("\n✓ ¡Todos los índices creados exitosamente!")
                print("\nMejoras esperadas:")
                print("  • Búsquedas por fecha: 3-5x más rápido")
                print("  • Filtrados por estado: 2-3x más rápido")
                print("  • Queries complejas: hasta 10x más rápido")
                
            except Exception as e:
                print(f"✗ Error al crear índices: {e}")
                conn.rollback()

if __name__ == "__main__":
    print("Agregando índices a la base de datos...")
    print("="*60)
    agregar_indices()
