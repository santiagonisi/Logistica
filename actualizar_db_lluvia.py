from logistica import create_app
from logistica.models import db

def actualizar_db():
    app = create_app()
    with app.app_context():
        with db.engine.connect() as conn:
            try:
                result = conn.execute(db.text("PRAGMA table_info(asignacion);"))
                columns = [row[1] for row in result]
                
                if 'lluvia' not in columns:
                    conn.execute(db.text("ALTER TABLE asignacion ADD COLUMN lluvia BOOLEAN DEFAULT 0;"))
                    conn.commit()
                    print("✓ Columna 'lluvia' agregada exitosamente")
                else:
                    print("• La columna 'lluvia' ya existe")
                    
            except Exception as e:
                print(f"✗ Error: {e}")
                conn.rollback()
        
        print("\n¡Actualización completada!")

if __name__ == "__main__":
    print("Actualizando base de datos...")
    print("="*50)
    actualizar_db()
