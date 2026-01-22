#!/usr/bin/env python3
"""Script para forzar que Django reconozca el campo pagos_online_habilitados."""
import os
import sys
import sqlite3

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')

try:
    import django
    django.setup()
    
    from core.models import ConfiguracionSistema
    from django.db import connection
    
    print("=" * 60)
    print("FORZANDO RECONOCIMIENTO DEL CAMPO")
    print("=" * 60)
    
    # 1. Verificar que el campo existe en el modelo
    print("\n1. Verificando modelo...")
    try:
        field = ConfiguracionSistema._meta.get_field('pagos_online_habilitados')
        print(f"   ✅ Campo existe en el modelo: {field.name}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)
    
    # 2. Forzar recarga del modelo
    print("\n2. Forzando recarga del modelo...")
    # Limpiar cualquier caché del modelo
    if hasattr(ConfiguracionSistema._meta, '_expire_cache'):
        ConfiguracionSistema._meta._expire_cache()
    
    # 3. Verificar acceso al campo
    print("\n3. Probando acceso al campo...")
    try:
        config = ConfiguracionSistema.objects.first()
        if config:
            # Intentar leer el campo
            valor = getattr(config, 'pagos_online_habilitados', None)
            print(f"   ✅ Valor actual: {valor}")
            
            # Intentar escribir el campo
            config.pagos_online_habilitados = True
            config.save(update_fields=['pagos_online_habilitados'])
            print(f"   ✅ Campo se puede leer y escribir")
        else:
            print("   ⚠️  No hay registros de configuración")
    except Exception as e:
        print(f"   ❌ Error al acceder al campo: {e}")
        import traceback
        traceback.print_exc()
    
    # 4. Verificar admin
    print("\n4. Verificando admin...")
    try:
        from core.admin import ConfiguracionSistemaAdmin
        from django.contrib import admin
        
        admin_class = admin.site._registry.get(ConfiguracionSistema)
        if admin_class:
            print(f"   ✅ Admin registrado")
            
            # Probar crear formulario
            admin_instance = ConfiguracionSistemaAdmin(ConfiguracionSistema, admin.site)
            form = admin_instance.get_form(None)()
            
            if 'pagos_online_habilitados' in form.fields:
                print(f"   ✅ Campo está en el formulario del admin")
            else:
                print(f"   ❌ Campo NO está en el formulario")
                print(f"   Campos disponibles: {list(form.fields.keys())}")
        else:
            print(f"   ❌ Admin no registrado")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Si el campo aparece en el formulario, reinicia el servidor")
    print("y recarga el admin con Ctrl+F5")
    print("=" * 60)
    
except ImportError as e:
    print(f"❌ Error al importar Django: {e}")
    print("   Ejecuta desde el entorno virtual correcto")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()



