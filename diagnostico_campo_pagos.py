#!/usr/bin/env python3
"""Script de diagnóstico para verificar el campo pagos_online_habilitados."""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from core.models import ConfiguracionSistema
from core.admin import ConfiguracionSistemaAdmin, ConfiguracionSistemaForm
from django.contrib import admin
from django.test import RequestFactory
from django.contrib.auth import get_user_model

print("=" * 70)
print("DIAGNÓSTICO: Campo pagos_online_habilitados")
print("=" * 70)

# 1. Verificar modelo
print("\n1. VERIFICANDO MODELO...")
try:
    field = ConfiguracionSistema._meta.get_field('pagos_online_habilitados')
    print(f"   ✅ Campo existe en el modelo: {field.name}")
    print(f"      Tipo: {type(field).__name__}")
    print(f"      Default: {field.default}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Verificar instancia
print("\n2. VERIFICANDO INSTANCIA...")
try:
    config = ConfiguracionSistema.objects.first()
    if config:
        print(f"   ✅ Instancia encontrada: {config.nombre_empresa}")
        try:
            valor = getattr(config, 'pagos_online_habilitados', None)
            print(f"   ✅ Valor del campo: {valor}")
        except Exception as e:
            print(f"   ❌ Error al leer el campo: {e}")
    else:
        print("   ⚠️  No hay instancias de ConfiguracionSistema")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Verificar formulario
print("\n3. VERIFICANDO FORMULARIO...")
try:
    form = ConfiguracionSistemaForm()
    if 'pagos_online_habilitados' in form.fields:
        print(f"   ✅ Campo está en el formulario")
        print(f"      Label: {form.fields['pagos_online_habilitados'].label}")
        print(f"      Help text: {form.fields['pagos_online_habilitados'].help_text}")
    else:
        print(f"   ❌ Campo NO está en el formulario")
        print(f"      Campos disponibles: {list(form.fields.keys())}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# 4. Verificar admin
print("\n4. VERIFICANDO ADMIN...")
try:
    admin_class = admin.site._registry.get(ConfiguracionSistema)
    if admin_class:
        print(f"   ✅ Admin registrado: {type(admin_class).__name__}")
        
        # Crear request mock
        factory = RequestFactory()
        request = factory.get('/admin/core/configuracionsistema/1/change/')
        User = get_user_model()
        user = User.objects.filter(is_superuser=True).first()
        if user:
            request.user = user
            
            # Obtener formulario del admin
            admin_instance = admin_class(ConfiguracionSistema, admin.site)
            form = admin_instance.get_form(request)()
            
            if 'pagos_online_habilitados' in form.fields:
                print(f"   ✅ Campo está en el formulario del admin")
            else:
                print(f"   ❌ Campo NO está en el formulario del admin")
                print(f"      Campos disponibles: {list(form.fields.keys())}")
            
            # Verificar fieldsets
            fieldsets = admin_instance.get_fieldsets(request)
            print(f"\n   Fieldsets encontrados: {len(fieldsets)}")
            for name, options in fieldsets:
                fields_in_set = options.get('fields', [])
                print(f"      - {name}: {fields_in_set}")
                if 'pagos_online_habilitados' in fields_in_set:
                    print(f"        ✅ Campo encontrado en este fieldset")
        else:
            print("   ⚠️  No hay superusuario para crear request mock")
    else:
        print(f"   ❌ Admin no registrado")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# 5. Verificar base de datos
print("\n5. VERIFICANDO BASE DE DATOS...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        if 'sqlite' in connection.vendor:
            cursor.execute("SELECT pagos_online_habilitados FROM core_configuracionsistema LIMIT 1")
        else:
            cursor.execute("SELECT pagos_online_habilitados FROM core_configuracionsistema LIMIT 1")
        result = cursor.fetchone()
        if result:
            print(f"   ✅ Campo existe en BD, valor: {result[0]}")
        else:
            print(f"   ⚠️  No hay registros en la tabla")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("FIN DEL DIAGNÓSTICO")
print("=" * 70)



