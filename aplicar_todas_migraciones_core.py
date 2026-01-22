#!/usr/bin/env python3
"""Script para aplicar todas las migraciones de core, creando la tabla si no existe."""
import sqlite3
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')

try:
    import django
    django.setup()
    
    from django.core.management import call_command
    from django.db import connection
    
    print("=" * 60)
    print("APLICANDO MIGRACIONES DE CORE")
    print("=" * 60)
    
    # Aplicar todas las migraciones de core
    print("\n📝 Ejecutando migraciones de core...")
    call_command('migrate', 'core', verbosity=2, interactive=False)
    
    # Verificar que la tabla existe ahora
    with connection.cursor() as cursor:
        if 'sqlite' in connection.vendor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'core_%'")
        elif 'postgresql' in connection.vendor:
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name LIKE 'core_%'
            """)
        else:
            cursor.execute("SHOW TABLES LIKE 'core_%'")
        
        tables = [row[0] for row in cursor.fetchall()]
        
        if 'core_configuracionsistema' in tables or any('configuracionsistema' in t.lower() for t in tables):
            print("\n✅ Tabla core_configuracionsistema creada exitosamente")
            
            # Verificar si el campo existe
            table_name = next((t for t in tables if 'configuracionsistema' in t.lower()), None)
            if table_name:
                if 'sqlite' in connection.vendor:
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = [row[1] for row in cursor.fetchall()]
                elif 'postgresql' in connection.vendor:
                    cursor.execute("""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name = %s AND column_name = 'pagos_online_habilitados'
                    """, [table_name])
                    columns = [row[0] for row in cursor.fetchall()]
                
                if 'pagos_online_habilitados' in columns:
                    print("✅ Campo 'pagos_online_habilitados' existe en la tabla")
                else:
                    print("⚠️  Campo 'pagos_online_habilitados' NO existe, aplicando migración 0007...")
                    call_command('migrate', 'core', '0007', verbosity=2, interactive=False)
        else:
            print("\n❌ La tabla core_configuracionsistema no se creó")
            print("   Tablas de core encontradas:", tables)
    
    print("\n✅ Migraciones aplicadas")
    print("\n⚠️  IMPORTANTE: Reinicia el servidor Django")
    print("   python manage.py runserver")
    
except ImportError as e:
    print(f"\n❌ Error al importar Django: {e}")
    print("   Asegúrate de estar en el entorno virtual correcto")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)



