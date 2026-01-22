#!/usr/bin/env python3
"""Script de diagnóstico para verificar por qué no aparece el campo en el admin."""
import os
import sys

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')

try:
    import django
    django.setup()
    
    from core.models import ConfiguracionSistema
    from core.admin import ConfiguracionSistemaAdmin
    from django.contrib import admin
    
    print("=" * 60)
    print("DIAGNÓSTICO DEL ADMIN")
    print("=" * 60)
    
    # 1. Verificar modelo
    print("\n1. Verificando modelo...")
    try:
        campo = ConfiguracionSistema._meta.get_field('pagos_online_habilitados')
        print(f"   ✅ Campo existe en el modelo: {campo.name}")
        print(f"   ✅ Tipo: {campo.__class__.__name__}")
        print(f"   ✅ Default: {campo.default}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Verificar admin
    print("\n2. Verificando admin...")
    try:
        admin_class = admin.site._registry.get(ConfiguracionSistema)
        if admin_class:
            print(f"   ✅ ConfiguracionSistema está registrado en el admin")
            print(f"   ✅ Clase: {admin_class.__class__.__name__}")
            
            # Verificar fieldsets
            if hasattr(admin_class, 'fieldsets'):
                print(f"   ✅ Tiene fieldsets: {len(admin_class.fieldsets)} secciones")
                for name, options in admin_class.fieldsets:
                    fields = options.get('fields', [])
                    if 'pagos_online_habilitados' in fields:
                        print(f"   ✅ Campo encontrado en fieldset: '{name}'")
                    else:
                        print(f"   ⚠️  Campo NO en fieldset: '{name}'")
            
            # Verificar fields
            if hasattr(admin_class, 'fields'):
                print(f"   ✅ Tiene fields: {admin_class.fields}")
                if 'pagos_online_habilitados' in admin_class.fields:
                    print(f"   ✅ Campo está en la lista 'fields'")
                else:
                    print(f"   ❌ Campo NO está en la lista 'fields'")
        else:
            print(f"   ❌ ConfiguracionSistema NO está registrado en el admin")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. Verificar base de datos
    print("\n3. Verificando base de datos...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            if 'sqlite' in connection.vendor:
                cursor.execute("PRAGMA table_info(core_configuracionsistema)")
                columns = [row[1] for row in cursor.fetchall()]
            elif 'postgresql' in connection.vendor:
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'core_configuracionsistema'
                """)
                columns = [row[0] for row in cursor.fetchall()]
            else:
                cursor.execute("SHOW COLUMNS FROM core_configuracionsistema")
                columns = [row[0] for row in cursor.fetchall()]
            
            if 'pagos_online_habilitados' in columns:
                print(f"   ✅ Campo existe en la BD")
            else:
                print(f"   ❌ Campo NO existe en la BD")
                print(f"   Columnas encontradas: {columns}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Probar crear un formulario
    print("\n4. Probando crear formulario del admin...")
    try:
        admin_instance = ConfiguracionSistemaAdmin(ConfiguracionSistema, admin.site)
        form_class = admin_instance.get_form(None)
        form = form_class()
        
        if 'pagos_online_habilitados' in form.fields:
            print(f"   ✅ Campo está en el formulario")
        else:
            print(f"   ❌ Campo NO está en el formulario")
            print(f"   Campos disponibles: {list(form.fields.keys())}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("RECOMENDACIONES:")
    print("=" * 60)
    print("1. Reinicia el servidor Django completamente")
    print("2. Limpia archivos .pyc: find . -name '*.pyc' -delete")
    print("3. Limpia __pycache__: find . -type d -name __pycache__ -exec rm -r {} +")
    print("4. Recarga el admin con Ctrl+F5")
    print("=" * 60)
    
except ImportError as e:
    print(f"❌ Error al importar Django: {e}")
    print("   Ejecuta este script desde el entorno virtual correcto")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()



