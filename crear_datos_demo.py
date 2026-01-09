#!/usr/bin/env python
"""
Script para crear datos de prueba para el demo de pagos
Ejecutar: python crear_datos_demo.py
"""
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from clientes.models import Cliente
from pagos.models import Pago
from instalaciones.models import Instalacion, Plan, TipoInstalacion


def crear_datos_demo():
    """Crea datos de prueba para el demo."""
    print("=" * 70)
    print("🎬 CREACIÓN DE DATOS PARA DEMO DE PAGOS")
    print("=" * 70)
    print()
    
    # Crear cliente de prueba
    print("1. Creando cliente de prueba...")
    cliente, created = Cliente.objects.get_or_create(
        telefono="1234567890",
        defaults={
            'nombre': "Juan",
            'apellido1': "Pérez",
            'apellido2': "Demo",
            'email': "juan.perez.demo@example.com",
            'ciudad': "Ciudad de México",
            'estado_cliente': 'activo'
        }
    )
    
    if created:
        print(f"   ✅ Cliente creado: {cliente.nombre_completo}")
    else:
        print(f"   ℹ️  Cliente ya existía: {cliente.nombre_completo}")
    
    print()
    
    # Crear plan de prueba (si no existe)
    print("2. Creando plan de prueba (opcional)...")
    plan, plan_created = Plan.objects.get_or_create(
        nombre="Plan Demo 100 Mbps",
        defaults={
            'velocidad_descarga': 100,
            'velocidad_subida': 50,
            'precio_mensual': Decimal('299.00'),
            'descripcion': 'Plan de prueba para demo'
        }
    )
    
    if plan_created:
        print(f"   ✅ Plan creado: {plan.nombre}")
    else:
        print(f"   ℹ️  Plan ya existía: {plan.nombre}")
    
    print()
    
    # Crear tipo de instalación (si no existe)
    print("3. Creando tipo de instalación (opcional)...")
    tipo_instalacion, tipo_created = TipoInstalacion.objects.get_or_create(
        nombre="Residencial",
        defaults={
            'descripcion': 'Instalación residencial'
        }
    )
    
    if tipo_created:
        print(f"   ✅ Tipo de instalación creado: {tipo_instalacion.nombre}")
    else:
        print(f"   ℹ️  Tipo ya existía: {tipo_instalacion.nombre}")
    
    print()
    
    # Crear instalación de prueba (opcional)
    print("4. Creando instalación de prueba (opcional)...")
    instalacion, inst_created = Instalacion.objects.get_or_create(
        cliente=cliente,
        plan=plan,
        defaults={
            'tipo_instalacion': tipo_instalacion,
            'estado': 'activa',
            'fecha_activacion': date.today(),
            'direccion': 'Calle Demo #123'
        }
    )
    
    if inst_created:
        print(f"   ✅ Instalación creada: {instalacion.plan_nombre}")
    else:
        print(f"   ℹ️  Instalación ya existía: {instalacion.plan_nombre}")
    
    print()
    
    # Crear pagos de prueba
    print("5. Creando pagos de prueba...")
    
    pagos_creados = []
    hoy = date.today()
    
    # Pago pendiente (para probar)
    pago1, p1_created = Pago.objects.get_or_create(
        cliente=cliente,
        instalacion=instalacion,
        concepto="Pago mensual - Demo",
        periodo_mes=hoy.month,
        periodo_anio=hoy.year,
        defaults={
            'monto': Decimal('100.00'),
            'fecha_vencimiento': hoy + timedelta(days=7),
            'estado': 'pendiente'
        }
    )
    
    if p1_created:
        pagos_creados.append(pago1)
        print(f"   ✅ Pago pendiente creado: ${pago1.monto} (ID: {pago1.id})")
        print(f"      URL: http://localhost:8000/pagos/{pago1.id}/")
    else:
        print(f"   ℹ️  Pago pendiente ya existía: ${pago1.monto} (ID: {pago1.id})")
        pagos_creados.append(pago1)
    
    # Pago vencido (para mostrar diferentes estados)
    pago2, p2_created = Pago.objects.get_or_create(
        cliente=cliente,
        instalacion=instalacion,
        concepto="Pago mensual - Demo Vencido",
        periodo_mes=(hoy - timedelta(days=30)).month,
        periodo_anio=(hoy - timedelta(days=30)).year,
        defaults={
            'monto': Decimal('150.00'),
            'fecha_vencimiento': hoy - timedelta(days=5),
            'estado': 'vencido'
        }
    )
    
    if p2_created:
        pagos_creados.append(pago2)
        print(f"   ✅ Pago vencido creado: ${pago2.monto} (ID: {pago2.id})")
    else:
        print(f"   ℹ️  Pago vencido ya existía: ${pago2.monto} (ID: {pago2.id})")
        pagos_creados.append(pago2)
    
    # Pago sin instalación (para mostrar flexibilidad)
    pago3, p3_created = Pago.objects.get_or_create(
        cliente=cliente,
        instalacion=None,
        concepto="Pago adicional - Demo",
        periodo_mes=hoy.month,
        periodo_anio=hoy.year,
        defaults={
            'monto': Decimal('50.00'),
            'fecha_vencimiento': hoy + timedelta(days=15),
            'estado': 'pendiente'
        }
    )
    
    if p3_created:
        pagos_creados.append(pago3)
        print(f"   ✅ Pago sin instalación creado: ${pago3.monto} (ID: {pago3.id})")
    else:
        print(f"   ℹ️  Pago sin instalación ya existía: ${pago3.monto} (ID: {pago3.id})")
        pagos_creados.append(pago3)
    
    print()
    
    # Resumen
    print("=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print()
    print(f"Cliente: {cliente.nombre_completo}")
    print(f"  Email: {cliente.email}")
    print(f"  Teléfono: {cliente.telefono}")
    print()
    print(f"Instalación: {instalacion.plan_nombre if instalacion else 'N/A'}")
    print()
    print("Pagos creados/encontrados:")
    for pago in pagos_creados:
        estado_color = {
            'pendiente': '🟡',
            'vencido': '🔴',
            'pagado': '🟢',
            'cancelado': '⚪'
        }
        icon = estado_color.get(pago.estado, '⚪')
        print(f"  {icon} ${pago.monto} - {pago.get_estado_display()} (ID: {pago.id})")
        print(f"     URL: http://localhost:8000/pagos/{pago.id}/")
        if pago.estado in ['pendiente', 'vencido']:
            print(f"     Pagar: http://localhost:8000/pagos/{pago.id}/procesar-online/")
    
    print()
    print("=" * 70)
    print("✅ DATOS DE DEMO LISTOS")
    print("=" * 70)
    print()
    print("📝 Próximos pasos:")
    print("   1. Inicia el servidor: python manage.py runserver")
    print("   2. Accede a uno de los pagos pendientes o vencidos")
    print("   3. Haz clic en 'Pagar en Línea'")
    print("   4. Selecciona Mercado Pago o PayPal")
    print("   5. Prueba el flujo completo")
    print()
    print("📖 Para más detalles, ver: DEMO_PAGOS_MERCADOPAGO_PAYPAL.md")
    print()


if __name__ == '__main__':
    try:
        crear_datos_demo()
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR")
        print("=" * 70)
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)

