#!/usr/bin/env python
"""Script para diagnosticar visualización de asignaciones"""

from logistica import create_app
from logistica.models import db, Asignacion
from sqlalchemy import func

def diagnostico():
    app = create_app()
    with app.app_context():
        print("\n" + "="*70)
        print("🔍 DIAGNOSTICO DE VISUALIZACION DE ASIGNACIONES")
        print("="*70)
        
        # Total de asignaciones
        total = Asignacion.query.count()
        print(f"\n📊 Total de asignaciones en BD: {total}")
        print(f"📄 Páginas (50 por página): {(total + 49) // 50}")
        
        # Primera página (lo que ve el usuario)
        primera_pag = Asignacion.query.order_by(
            Asignacion.fecha.desc(), 
            Asignacion.hora_inicio.desc()
        ).limit(50).all()
        
        print(f"\n👁️  Primera página muestra: {len(primera_pag)} asignaciones")
        
        if primera_pag:
            print(f"  📅 Fecha más reciente: {primera_pag[0].fecha}")
            print(f"  📅 Fecha más antigua (pag 1): {primera_pag[-1].fecha}")
        
        # Distribución por año
        print("\n📅 DISTRIBUCIÓN POR AÑO:")
        result = db.session.query(
            func.strftime('%Y', Asignacion.fecha).label('anio'),
            func.count(Asignacion.id).label('cantidad')
        ).group_by('anio').order_by('anio').all()
        
        for anio, cantidad in result:
            print(f"  {anio}: {cantidad} asignaciones")
        
        # Últimas 10 fechas
        print("\n🕒 ÚLTIMAS 10 ASIGNACIONES (lo que ve primero):")
        ultimas = Asignacion.query.order_by(
            Asignacion.fecha.desc(),
            Asignacion.hora_inicio.desc()
        ).limit(10).all()
        
        for i, asig in enumerate(ultimas, 1):
            cliente_nombre = asig.cliente.nombre if asig.cliente else "Sin cliente"
            print(f"  {i}. {asig.fecha} {asig.hora_inicio} - {cliente_nombre}")
        
        print("\n" + "="*70)
        print("✅ DIAGNÓSTICO COMPLETADO")
        print("\nNOTA: La primera página muestra solo las 50 asignaciones más recientes.")
        print("Use los botones de paginación en la web para ver todas las demás.\n")
        print("="*70 + "\n")

if __name__ == "__main__":
    diagnostico()
