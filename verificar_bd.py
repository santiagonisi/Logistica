#!/usr/bin/env python
"""Script para verificar el estado actual de la base de datos"""

import sqlite3

def verificar_bd():
    print("\n" + "="*70)
    print("🔍 VERIFICACION DE BASE DE DATOS ACTUAL")
    print("="*70)
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Ver tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("\n📋 TABLAS EXISTENTES:")
    for t in tables:
        print(f"  ✓ {t[0]}")
    
    # Ver estructura de asignacion
    cursor.execute("PRAGMA table_info(asignacion)")
    cols = cursor.fetchall()
    print("\n📊 COLUMNAS EN 'asignacion':")
    for col in cols:
        print(f"  • {col[1]:20s} {col[2]:10s} {'NOT NULL' if col[3] else ''}")
    
    # Verificar si existe columna 'lluvia'
    col_names = [col[1] for col in cols]
    tiene_lluvia = 'lluvia' in col_names
    print(f"\n🌧️  Columna 'lluvia': {'✓ YA EXISTE' if tiene_lluvia else '✗ FALTA (se agregará)'}")
    
    # Contar registros
    print("\n📈 TOTAL DE REGISTROS:")
    try:
        cursor.execute("SELECT COUNT(*) FROM asignacion")
        print(f"  Asignaciones: {cursor.fetchone()[0]}")
    except:
        print(f"  Asignaciones: 0 (tabla vacía o error)")
    
    try:
        cursor.execute("SELECT COUNT(*) FROM cliente")
        print(f"  Clientes:     {cursor.fetchone()[0]}")
    except:
        print(f"  Clientes:     0")
    
    try:
        cursor.execute("SELECT COUNT(*) FROM vehiculo")
        print(f"  Vehículos:    {cursor.fetchone()[0]}")
    except:
        print(f"  Vehículos:    0")
    
    try:
        cursor.execute("SELECT COUNT(*) FROM comitente")
        print(f"  Comitentes:   {cursor.fetchone()[0]}")
    except:
        print(f"  Comitentes:   0")
    
    # Verificar índices
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
    indices = cursor.fetchall()
    print(f"\n🔎 INDICES EXISTENTES: {len(indices)}")
    for idx in indices:
        print(f"  • {idx[0]}")
    
    conn.close()
    
    print("\n" + "="*70)
    print("✅ VERIFICACION COMPLETADA\n")
    
    return tiene_lluvia

if __name__ == "__main__":
    verificar_bd()
