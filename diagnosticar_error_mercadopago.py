#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para diagnosticar errores con Mercado Pago
Ejecutar: python3 diagnosticar_error_mercadopago.py
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from django.conf import settings
from pagos.models import Pago
from pagos.payment_gateway import PaymentGateway

def diagnosticar():
    print("=" * 70)
    print("🔍 DIAGNÓSTICO DE ERRORES CON MERCADO PAGO")
    print("=" * 70)
    print()
    
    # 1. Verificar configuración
    print("1. VERIFICACIÓN DE CONFIGURACIÓN")
    print("-" * 70)
    
    access_token = getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', '')
    site_url = getattr(settings, 'SITE_URL', '')
    
    if not access_token:
        print("❌ MERCADOPAGO_ACCESS_TOKEN: NO configurado")
        print("   Solución: Agrega MERCADOPAGO_ACCESS_TOKEN en .env")
        return
    else:
        print(f"✅ MERCADOPAGO_ACCESS_TOKEN: Configurado")
        print(f"   Valor: {access_token[:20]}...{access_token[-10:]}")
    
    if not site_url:
        print("⚠️  SITE_URL: NO configurado (usando localhost:8000)")
    else:
        print(f"✅ SITE_URL: {site_url}")
    
    print()
    
    # 2. Verificar SDK
    print("2. VERIFICACIÓN DEL SDK")
    print("-" * 70)
    
    try:
        import mercadopago
        print("✅ SDK de Mercado Pago instalado")
        
        # Intentar inicializar
        try:
            sdk = mercadopago.SDK(access_token)
            print("✅ SDK inicializado correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar SDK: {str(e)}")
            print("   Verifica que tu Access Token sea válido")
            return
    except ImportError:
        print("❌ SDK de Mercado Pago NO instalado")
        print("   Ejecuta: pip install mercadopago>=2.2.0")
        return
    
    print()
    
    # 3. Obtener un pago de prueba
    print("3. VERIFICACIÓN DE DATOS DEL PAGO")
    print("-" * 70)
    
    try:
        pago = Pago.objects.filter(estado__in=['pendiente', 'vencido']).first()
        if not pago:
            print("⚠️  No hay pagos pendientes o vencidos para probar")
            print("   Crea un pago de prueba o ejecuta: python crear_datos_demo.py")
            return
        
        print(f"✅ Pago encontrado: ID {pago.id}")
        print(f"   Monto: ${pago.monto}")
        print(f"   Concepto: {pago.concepto}")
        print(f"   Cliente: {pago.cliente.nombre_completo}")
        
        # Verificar datos del cliente
        print(f"   Email cliente: {pago.cliente.email if hasattr(pago.cliente, 'email') and pago.cliente.email else 'NO tiene'}")
        print(f"   Teléfono cliente: {pago.cliente.telefono if hasattr(pago.cliente, 'telefono') and pago.cliente.telefono else 'NO tiene'}")
        
        # Verificar que el monto sea válido
        if float(pago.monto) <= 0:
            print("❌ El monto del pago debe ser mayor a 0")
            return
        
    except Exception as e:
        print(f"❌ Error al obtener pago: {str(e)}")
        return
    
    print()
    
    # 4. Probar creación de preferencia
    print("4. PRUEBA DE CREACIÓN DE PREFERENCIA")
    print("-" * 70)
    
    try:
        gateway = PaymentGateway(pasarela='mercadopago')
        print("✅ PaymentGateway inicializado")
        
        # Preparar URLs
        base_url = site_url or 'http://localhost:8000'
        return_url = f"{base_url}/pagos/{pago.pk}/pago-exitoso/?payment_id={{payment_id}}"
        cancel_url = f"{base_url}/pagos/{pago.pk}/pago-cancelado/"
        
        print(f"   Return URL: {return_url}")
        print(f"   Cancel URL: {cancel_url}")
        print()
        print("   Intentando crear preferencia...")
        
        resultado = gateway.crear_intento_pago(pago, return_url, cancel_url)
        
        if resultado.get('success'):
            print("✅ Preferencia creada exitosamente!")
            print(f"   Preference ID: {resultado.get('preference_id')}")
            print(f"   URL: {resultado.get('url')}")
        else:
            print("❌ Error al crear preferencia:")
            error = resultado.get('error', 'Error desconocido')
            print(f"   Error: {error}")
            print()
            print("   Posibles causas:")
            print("   1. Access Token inválido o expirado")
            print("   2. Datos del pago incompletos (falta email o teléfono)")
            print("   3. Monto inválido")
            print("   4. URLs de retorno inválidas")
            print("   5. Cuenta de Mercado Pago no activa")
            
    except ValueError as e:
        print(f"❌ Error de configuración: {str(e)}")
        print()
        print("   Solución: Verifica que MERCADOPAGO_ACCESS_TOKEN esté correctamente configurado en .env")
    except ImportError as e:
        print(f"❌ Error de importación: {str(e)}")
        print()
        print("   Solución: pip install mercadopago>=2.2.0")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)
    print("📝 PRÓXIMOS PASOS")
    print("=" * 70)
    print()
    print("Si el diagnóstico muestra errores:")
    print("1. Verifica que las credenciales en .env sean correctas")
    print("2. Asegúrate de usar credenciales de TEST (empiezan con TEST-)")
    print("3. Verifica que el cliente tenga email o teléfono")
    print("4. Reinicia el servidor Django después de modificar .env")
    print()
    print("Para más ayuda, revisa:")
    print("  - OBTENER_CREDENCIALES_PASO_A_PASO.md")
    print("  - CONFIGURAR_PASARELAS_RAPIDO.md")

if __name__ == '__main__':
    diagnosticar()


