#!/usr/bin/env python
"""Script para crear ZIP para deploy en servidor"""

import zipfile
import os
from datetime import datetime
from pathlib import Path

def crear_zip_deploy():
    print("\n" + "="*70)
    print("📦 CREANDO PAQUETE PARA SERVIDOR")
    print("="*70)
    
    # Nombre del archivo ZIP con fecha
    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_nombre = f'logistica_deploy_{fecha}.zip'
    
    # Archivos y carpetas a INCLUIR
    incluir = [
        'logistica/',           # Carpeta principal de la app
        'data.db',              # Base de datos actualizada
        'config.py',            # Configuración
        'run.py',               # Script de inicio
        'requirements.txt',     # Dependencias
        'instance/',            # Carpeta instance (si existe)
        'start.bat',            # Script de inicio Windows
        'start.ps1',            # Script de inicio PowerShell
    ]
    
    # Patrones a EXCLUIR
    excluir = [
        '__pycache__',
        '.pyc',
        '.pyo',
        '.git',
        '.venv',
        'venv',
        '.vscode',
        'data.db.backup',
        'sqlite-tools',
        'upgrade_database.py',
        'verificar_bd.py',
        'diagnostico_asignaciones.py',
        'actualizar_db_lluvia.py',
        'agregar_indices.py',
        'inicializar_comitentes.py',
        'migracion.sql',
    ]
    
    archivos_agregados = []
    
    with zipfile.ZipFile(zip_nombre, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in incluir:
            item_path = Path(item)
            
            if not item_path.exists():
                print(f"  ⚠ Saltando {item} (no existe)")
                continue
            
            if item_path.is_file():
                # Agregar archivo individual
                zipf.write(item, item)
                archivos_agregados.append(item)
                print(f"  ✓ {item}")
            
            elif item_path.is_dir():
                # Agregar carpeta recursivamente
                for root, dirs, files in os.walk(item):
                    # Filtrar directorios a excluir
                    dirs[:] = [d for d in dirs if not any(ex in d for ex in excluir)]
                    
                    for file in files:
                        # Filtrar archivos a excluir
                        if any(ex in file for ex in excluir):
                            continue
                        
                        file_path = os.path.join(root, file)
                        arcname = file_path
                        zipf.write(file_path, arcname)
                        archivos_agregados.append(arcname)
                        print(f"  ✓ {arcname}")
    
    # Estadísticas
    zip_size = os.path.getsize(zip_nombre) / (1024 * 1024)  # MB
    
    print("\n" + "="*70)
    print("✅ PAQUETE CREADO EXITOSAMENTE")
    print("="*70)
    print(f"\n📦 Archivo: {zip_nombre}")
    print(f"📊 Tamaño: {zip_size:.2f} MB")
    print(f"📁 Archivos incluidos: {len(archivos_agregados)}")
    
    print("\n📋 CONTENIDO PRINCIPAL:")
    print("  ✓ Código de la aplicación (logistica/)")
    print("  ✓ Base de datos actualizada (data.db)")
    print("  ✓ Configuración (config.py)")
    print("  ✓ Script de inicio (run.py)")
    print("  ✓ Dependencias (requirements.txt)")
    
    print("\n🚀 INSTRUCCIONES PARA DEPLOY:")
    print("  1. Subir el archivo al servidor")
    print("  2. Descomprimir en la carpeta deseada")
    print("  3. Instalar dependencias: pip install -r requirements.txt")
    print("  4. Iniciar: python run.py")
    
    print("\n⚠️  IMPORTANTE:")
    print("  - La BD ya está actualizada (con columna lluvia e índices)")
    print("  - NO incluye entorno virtual (.venv)")
    print("  - NO incluye scripts de migración (ya ejecutados)")
    
    print("\n" + "="*70 + "\n")
    
    return zip_nombre

if __name__ == "__main__":
    try:
        archivo = crear_zip_deploy()
        print(f"✅ Listo para subir: {archivo}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
