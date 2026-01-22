#!/usr/bin/env python
"""Script simple para verificar si el campo existe en la BD."""
import sqlite3
import os

# Buscar el archivo de base de datos
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar si la columna existe
    cursor.execute("PRAGMA table_info(core_configuracionsistema)")
    columns = [row[1] for row in cursor.fetchall()]
    
    print("=" * 60)
    print("VERIFICACIÓN DEL CAMPO EN LA BASE DE DATOS")
    print("=" * 60)
    print(f"\nBase de datos: {db_path}")
    print(f"\nColumnas en core_configuracionsistema:")
    for col in columns:
        print(f"  - {col}")
    
    if 'pagos_online_habilitados' in columns:
        print("\n✅ El campo 'pagos_online_habilitados' EXISTE en la BD")
    else:
        print("\n❌ El campo 'pagos_online_habilitados' NO EXISTE en la BD")
        print("\n   Necesitas ejecutar:")
        print("   python manage.py migrate core")
    
    conn.close()
else:
    print(f"❌ No se encontró la base de datos en: {db_path}")
    print("   Si usas PostgreSQL, este script no funcionará.")
    print("   Ejecuta: python manage.py migrate core")



