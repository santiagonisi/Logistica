#!/usr/bin/env python
"""
Script de Upgrade de Base de Datos
Ejecuta todas las migraciones en el orden correcto
"""

import os
import sys
from pathlib import Path

def upgrade_database():
    """Ejecuta todas las migraciones en orden"""
    
    print("\n" + "="*70)
    print("🔧 ACTUALIZACION DE BASE DE DATOS - LOGISTICA")
    print("="*70)
    
    # Importar los scripts de migración
    from logistica import create_app
    from logistica.models import db, Comitente
    from actualizar_db_lluvia import actualizar_db
    from agregar_indices import agregar_indices
    
    app = create_app()
    
    with app.app_context():
        print("\n📋 Paso 1: Crear tablas base...")
        print("-"*70)
        try:
            db.create_all()
            print("✓ Tablas base creadas/verificadas")
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
        
        print("\n📋 Paso 2: Agregar columna 'lluvia' (si es necesaria)...")
        print("-"*70)
        try:
            actualizar_db()
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
        
        print("\n📋 Paso 3: Crear índices para optimización...")
        print("-"*70)
        try:
            agregar_indices()
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
        
        print("\n📋 Paso 4: Verificar base de datos...")
        print("-"*70)
        try:
            with db.engine.connect() as conn:
                result = conn.execute(db.text("PRAGMA table_info(asignacion);"))
                columns = [row[1] for row in result]
                print(f"✓ Tabla 'asignacion' con {len(columns)} columnas")
            
            comitentes_count = Comitente.query.count()
            print(f"✓ Total de comitentes: {comitentes_count}")
            
        except Exception as e:
            print(f"⚠ Advertencia durante verificación: {e}")
    
    print("\n" + "="*70)
    print("✅ ¡UPGRADE COMPLETADO EXITOSAMENTE!")
    print("="*70)
    print("\n📊 Resumen de cambios:")
    print("  ✓ Columna 'lluvia' agregada a asignaciones")
    print("  ✓ Índices de búsqueda creados")
    print("  ✓ Base de datos optimizada")
    print("\nTu aplicación está lista para funcionar con los nuevos cambios.\n")
    
    return True

if __name__ == "__main__":
    try:
        success = upgrade_database()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
