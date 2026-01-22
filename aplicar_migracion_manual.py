#!/usr/bin/env python3
"""Script para aplicar la migración manualmente agregando la columna directamente."""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

if not os.path.exists(db_path):
    print(f"❌ No se encontró la base de datos en: {db_path}")
    print("   Si usas PostgreSQL, necesitas ejecutar la migración de otra forma.")
    exit(1)

print("=" * 60)
print("APLICANDO MIGRACIÓN MANUALMENTE")
print("=" * 60)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar específicamente la tabla de ConfiguracionSistema de core
    # Puede ser: core_configuracionsistema o core_configuracionsistema (con app_label)
    possible_names = [
        'core_configuracionsistema',
        'core_configuracionsistema',
    ]
    
    # Buscar todas las tablas que contengan 'config' y 'sistema'
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    all_tables = [row[0] for row in cursor.fetchall()]
    
    # Buscar la tabla correcta
    table_name = None
    for name in all_tables:
        if 'core' in name and 'config' in name.lower() and 'sistema' in name.lower():
            table_name = name
            break
    
    if not table_name:
        print("\n❌ No se encontró la tabla core_configuracionsistema")
        print("   Tablas disponibles que contienen 'config':")
        config_tables = [t for t in all_tables if 'config' in t.lower()]
        for table in config_tables:
            print(f"   - {table}")
        conn.close()
        exit(1)
    
    print(f"\n📋 Tabla encontrada: {table_name}")
    
    # Verificar si la columna ya existe
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    
    print(f"\n📊 Columnas actuales: {', '.join(columns)}")
    
    if 'pagos_online_habilitados' in columns:
        print("\n✅ El campo 'pagos_online_habilitados' ya existe en la BD")
        conn.close()
        exit(0)
    
    print("\n📝 Agregando columna 'pagos_online_habilitados'...")
    
    # Agregar la columna (SQLite usa INTEGER para booleanos: 0=False, 1=True)
    cursor.execute(f"""
        ALTER TABLE {table_name} 
        ADD COLUMN pagos_online_habilitados INTEGER NOT NULL DEFAULT 1
    """)
    
    # Actualizar el registro de migraciones de Django si existe la tabla
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO django_migrations (app, name, applied)
            VALUES ('core', '0007_configuracionsistema_pagos_online_habilitados', datetime('now'))
        """)
    except sqlite3.OperationalError:
        print("⚠️  No se pudo actualizar django_migrations (puede que no exista la tabla)")
    
    conn.commit()
    conn.close()
    
    print("✅ Columna agregada exitosamente")
    print("\n⚠️  IMPORTANTE: Reinicia el servidor Django para que los cambios surtan efecto")
    print("   python manage.py runserver")
    
except sqlite3.Error as e:
    print(f"\n❌ Error al aplicar la migración: {e}")
    conn.rollback()
    conn.close()
    exit(1)

