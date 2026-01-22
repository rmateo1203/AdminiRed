#!/usr/bin/env python
"""Script para verificar si el campo pagos_online_habilitados existe."""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from core.models import ConfiguracionSistema
from django.db import connection

print("=" * 60)
print("VERIFICACIÓN DEL CAMPO pagos_online_habilitados")
print("=" * 60)

# 1. Verificar en el modelo
print("\n1. Verificando en el modelo Python...")
try:
    campo_existe = hasattr(ConfiguracionSistema(), 'pagos_online_habilitados')
    print(f"   ✓ Campo existe en el modelo: {campo_existe}")
    
    if campo_existe:
        campo = ConfiguracionSistema._meta.get_field('pagos_online_habilitados')
        print(f"   ✓ Tipo de campo: {campo.__class__.__name__}")
        print(f"   ✓ Valor por defecto: {campo.default}")
        print(f"   ✓ Nombre verbose: {campo.verbose_name}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# 2. Verificar en la base de datos
print("\n2. Verificando en la base de datos...")
try:
    with connection.cursor() as cursor:
        # Obtener el nombre de la tabla
        table_name = ConfiguracionSistema._meta.db_table
        
        # Verificar si la columna existe
        if 'sqlite' in connection.vendor:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]
        elif 'postgresql' in connection.vendor:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND column_name = 'pagos_online_habilitados'
            """, [table_name])
            columns = [row[0] for row in cursor.fetchall()]
        else:
            # MySQL
            cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'pagos_online_habilitados'")
            columns = [row[0] for row in cursor.fetchall()]
        
        if 'pagos_online_habilitados' in columns:
            print(f"   ✓ Columna existe en la base de datos")
        else:
            print(f"   ✗ Columna NO existe en la base de datos")
            print(f"   → Necesitas ejecutar: python manage.py migrate core")
except Exception as e:
    print(f"   ✗ Error al verificar BD: {e}")

# 3. Verificar configuración activa
print("\n3. Verificando configuración activa...")
try:
    config = ConfiguracionSistema.get_activa()
    if config:
        print(f"   ✓ Configuración activa encontrada: {config.nombre_empresa}")
        print(f"   ✓ ID: {config.pk}")
        print(f"   ✓ Pagos online habilitados: {config.pagos_online_habilitados}")
    else:
        print("   ✗ No hay configuración activa")
except Exception as e:
    print(f"   ✗ Error: {e}")

# 4. Verificar admin
print("\n4. Verificando configuración del admin...")
try:
    from core.admin import ConfiguracionSistemaAdmin
    admin_fields = ConfiguracionSistemaAdmin.fieldsets
    
    # Buscar el campo en los fieldsets
    campo_en_admin = False
    for name, options in admin_fields:
        if 'pagos_online_habilitados' in options.get('fields', []):
            campo_en_admin = True
            print(f"   ✓ Campo encontrado en el fieldset: '{name}'")
            break
    
    if not campo_en_admin:
        print("   ✗ Campo NO encontrado en los fieldsets del admin")
    
    # Verificar list_display
    if 'pagos_online_habilitados' in ConfiguracionSistemaAdmin.list_display:
        print(f"   ✓ Campo está en list_display")
    else:
        print(f"   ⚠ Campo NO está en list_display (pero puede estar en fieldsets)")
        
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("RESUMEN:")
print("=" * 60)
print("Si el campo NO existe en la BD, ejecuta:")
print("  python manage.py migrate core")
print("\nSi el campo existe pero no lo ves en el admin:")
print("  1. Reinicia el servidor Django")
print("  2. Limpia la caché del navegador (Ctrl+F5)")
print("  3. Verifica que estés logueado como administrador")
print("=" * 60)



