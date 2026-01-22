#!/usr/bin/env python3
"""Script para crear la tabla core_configuracionsistema directamente en SQLite."""
import sqlite3
import os
from datetime import datetime

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

if not os.path.exists(db_path):
    print(f"❌ No se encontró la base de datos en: {db_path}")
    exit(1)

print("=" * 60)
print("CREANDO TABLA core_configuracionsistema")
print("=" * 60)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar si la tabla ya existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_configuracionsistema'")
    if cursor.fetchone():
        print("\n⚠️  La tabla core_configuracionsistema ya existe")
        # Verificar si el campo existe
        cursor.execute("PRAGMA table_info(core_configuracionsistema)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'pagos_online_habilitados' in columns:
            print("✅ El campo 'pagos_online_habilitados' ya existe")
            conn.close()
            exit(0)
        else:
            print("📝 Agregando campo 'pagos_online_habilitados'...")
            cursor.execute("""
                ALTER TABLE core_configuracionsistema 
                ADD COLUMN pagos_online_habilitados INTEGER NOT NULL DEFAULT 1
            """)
            print("✅ Campo agregado exitosamente")
    else:
        # Crear la tabla completa
        print("\n📝 Creando tabla core_configuracionsistema...")
        cursor.execute("""
            CREATE TABLE core_configuracionsistema (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activa INTEGER NOT NULL DEFAULT 1,
                nombre_empresa VARCHAR(100) NOT NULL DEFAULT 'AdminiRed',
                descripcion_sistema VARCHAR(200) NOT NULL DEFAULT 'Sistema para el control total de instalaciones de internet',
                titulo_sistema VARCHAR(100),
                logo VARCHAR(100),
                color_primario VARCHAR(7) NOT NULL DEFAULT '#667eea',
                color_secundario VARCHAR(7) NOT NULL DEFAULT '#764ba2',
                color_exito VARCHAR(7) NOT NULL DEFAULT '#10b981',
                color_advertencia VARCHAR(7) NOT NULL DEFAULT '#f59e0b',
                color_peligro VARCHAR(7) NOT NULL DEFAULT '#ef4444',
                color_info VARCHAR(7) NOT NULL DEFAULT '#3b82f6',
                pagos_online_habilitados INTEGER NOT NULL DEFAULT 1,
                fecha_creacion DATETIME NOT NULL,
                fecha_actualizacion DATETIME NOT NULL
            )
        """)
        
        # Crear un registro por defecto
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO core_configuracionsistema 
            (activa, nombre_empresa, descripcion_sistema, pagos_online_habilitados, fecha_creacion, fecha_actualizacion)
            VALUES (1, 'AdminiRed', 'Sistema para el control total de instalaciones de internet', 1, ?, ?)
        """, (now, now))
        
        print("✅ Tabla creada con el campo 'pagos_online_habilitados' incluido")
        print("✅ Registro por defecto creado")
    
    # Actualizar django_migrations
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO django_migrations (app, name, applied)
            VALUES ('core', '0001_initial', datetime('now'))
        """)
        cursor.execute("""
            INSERT OR IGNORE INTO django_migrations (app, name, applied)
            VALUES ('core', '0007_configuracionsistema_pagos_online_habilitados', datetime('now'))
        """)
    except sqlite3.OperationalError as e:
        print(f"⚠️  No se pudo actualizar django_migrations: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Proceso completado exitosamente")
    print("\n⚠️  IMPORTANTE: Reinicia el servidor Django")
    print("   python manage.py runserver")
    
except sqlite3.Error as e:
    print(f"\n❌ Error: {e}")
    conn.rollback()
    conn.close()
    exit(1)



