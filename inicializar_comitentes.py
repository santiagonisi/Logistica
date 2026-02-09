from logistica import create_app
from logistica.models import db, Comitente

def inicializar_comitentes():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        comitentes_default = [
            "DVBA",
            "DNV",
            "Municipalidad San Nicolas",
            "Municipalidad Ramallo",
            "Municipalidad San Pedro",
            "Municipalidad Pergamino",
            "Municipalidad Baradero",
            "Municipalidad Rojas",
            "Alloco",
            "IARSA",
            "Saj Construcciones",
            "Arenera Villa Ramallo SA",
            "Edeca S.A",
            "Marbuy",
            "Caso Jorge",
            "Unidad Ejecutora Corredor Vial N°4",
            "Autovía Construcciones y Servicios SA"
        ]
        
        agregados = 0
        existentes = 0
        
        for nombre in comitentes_default:
            existe = Comitente.query.filter_by(nombre=nombre).first()
            if not existe:
                nuevo = Comitente(nombre=nombre, estado="Activo")
                db.session.add(nuevo)
                agregados += 1
                print(f"✓ Agregado: {nombre}")
            else:
                existentes += 1
                print(f"• Ya existe: {nombre}")
        
        db.session.commit()
        print(f"\n{'='*50}")
        print(f"Comitentes agregados: {agregados}")
        print(f"Comitentes existentes: {existentes}")
        print(f"Total: {agregados + existentes}")
        print(f"{'='*50}")

if __name__ == "__main__":
    print("Inicializando comitentes...")
    print("="*50)
    inicializar_comitentes()
    print("\n¡Proceso completado!")
