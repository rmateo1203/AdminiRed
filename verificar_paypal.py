#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar la configuración de PayPal
Ejecutar: python verificar_paypal.py
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from django.conf import settings

def verificar_configuracion():
    """Verifica la configuración de PayPal."""
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN PAYPAL")
    print("=" * 70)
    print()
    
    # Verificar variables de entorno
    print("1. VARIABLES DE CONFIGURACIÓN")
    print("-" * 70)
    
    paypal_client_id = getattr(settings, 'PAYPAL_CLIENT_ID', '')
    paypal_secret = getattr(settings, 'PAYPAL_SECRET', '')
    paypal_mode = getattr(settings, 'PAYPAL_MODE', 'sandbox')
    site_url = getattr(settings, 'SITE_URL', '')
    
    print(f"PAYPAL_CLIENT_ID: {'✅ Configurado' if paypal_client_id else '❌ NO CONFIGURADO'}")
    if paypal_client_id:
        print(f"   Valor: {paypal_client_id[:10]}...{paypal_client_id[-5:]}")
    
    print(f"PAYPAL_SECRET: {'✅ Configurado' if paypal_secret else '❌ NO CONFIGURADO'}")
    if paypal_secret:
        print(f"   Valor: {paypal_secret[:10]}...{paypal_secret[-5:]}")
    
    print(f"PAYPAL_MODE: {paypal_mode}")
    print(f"   {'⚠️  Modo de pruebas (Sandbox)' if paypal_mode == 'sandbox' else '✅ Modo de producción (Live)'}")
    
    print(f"SITE_URL: {'✅ Configurado' if site_url else '❌ NO CONFIGURADO'}")
    if site_url:
        print(f"   Valor: {site_url}")
    
    print()
    
    # Verificar PaymentGateway
    print("2. VERIFICACIÓN DE PAYMENT GATEWAY")
    print("-" * 70)
    
    try:
        from pagos.payment_gateway import PaymentGateway
        
        try:
            gateway = PaymentGateway(pasarela='paypal')
            print("✅ PaymentGateway para PayPal inicializado correctamente")
            
            # Verificar métodos
            metodos_requeridos = [
                '_crear_intento_paypal',
                '_obtener_paypal_access_token',
                '_procesar_reembolso_paypal'
            ]
            
            for metodo in metodos_requeridos:
                if hasattr(gateway, metodo):
                    print(f"✅ Método {metodo} existe")
                else:
                    print(f"❌ Método {metodo} NO existe")
            
        except Exception as e:
            print(f"❌ Error al inicializar PaymentGateway: {str(e)}")
            
    except ImportError as e:
        print(f"❌ Error al importar PaymentGateway: {str(e)}")
    
    print()
    
    # Verificar acceso a API (solo si hay credenciales)
    if paypal_client_id and paypal_secret:
        print("3. VERIFICACIÓN DE CONEXIÓN CON PAYPAL")
        print("-" * 70)
        
        try:
            gateway = PaymentGateway(pasarela='paypal')
            access_token = gateway._obtener_paypal_access_token()
            
            if access_token:
                print("✅ Conexión exitosa con PayPal API")
                print(f"   Token obtenido: {access_token[:20]}...")
            else:
                print("❌ No se pudo obtener access token")
                print("   Verifica tus credenciales")
                
        except Exception as e:
            print(f"❌ Error al conectar con PayPal: {str(e)}")
    else:
        print("3. VERIFICACIÓN DE CONEXIÓN CON PAYPAL")
        print("-" * 70)
        print("⚠️  Saltado: Credenciales no configuradas")
    
    print()
    
    # Resumen
    print("=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    
    configurado = bool(paypal_client_id and paypal_secret and site_url)
    
    if configurado:
        print("✅ Configuración básica: COMPLETA")
        print()
        print("📝 Próximos pasos:")
        print("   1. Probar el flujo de pago en modo sandbox")
        print("   2. Verificar que los usuarios pueden pagar")
        print("   3. Cuando estés listo, cambiar a modo 'live'")
    else:
        print("❌ Configuración básica: INCOMPLETA")
        print()
        print("📝 Pasos para completar:")
        if not paypal_client_id:
            print("   - Agregar PAYPAL_CLIENT_ID en .env")
        if not paypal_secret:
            print("   - Agregar PAYPAL_SECRET en .env")
        if not site_url:
            print("   - Agregar SITE_URL en .env")
        print()
        print("📖 Ver GUIA_CONFIGURACION_PAYPAL.md para más detalles")
    
    print()
    print("=" * 70)

if __name__ == '__main__':
    verificar_configuracion()




