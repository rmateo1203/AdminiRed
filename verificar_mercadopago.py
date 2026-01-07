#!/usr/bin/env python
"""
Script para verificar la configuración de Mercado Pago
Ejecutar: python verificar_mercadopago.py
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
    """Verifica la configuración de Mercado Pago."""
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN MERCADO PAGO")
    print("=" * 70)
    print()
    
    # Verificar variables de entorno
    print("1. VARIABLES DE CONFIGURACIÓN")
    print("-" * 70)
    
    mercadopago_token = getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', '')
    mercadopago_public = getattr(settings, 'MERCADOPAGO_PUBLIC_KEY', '')
    site_url = getattr(settings, 'SITE_URL', '')
    
    print(f"MERCADOPAGO_ACCESS_TOKEN: {'✅ Configurado' if mercadopago_token else '❌ NO CONFIGURADO'}")
    if mercadopago_token:
        modo = "TEST" if mercadopago_token.startswith("TEST-") else "PRODUCCIÓN" if mercadopago_token.startswith("APP_USR-") else "DESCONOCIDO"
        print(f"   Valor: {mercadopago_token[:15]}...{mercadopago_token[-5:]}")
        print(f"   Modo: {modo}")
    
    print(f"MERCADOPAGO_PUBLIC_KEY: {'✅ Configurado' if mercadopago_public else '❌ NO CONFIGURADO'}")
    if mercadopago_public:
        modo = "TEST" if mercadopago_public.startswith("TEST-") else "PRODUCCIÓN" if mercadopago_public.startswith("APP_USR-") else "DESCONOCIDO"
        print(f"   Valor: {mercadopago_public[:15]}...{mercadopago_public[-5:]}")
        print(f"   Modo: {modo}")
    
    print(f"SITE_URL: {'✅ Configurado' if site_url else '❌ NO CONFIGURADO'}")
    if site_url:
        print(f"   Valor: {site_url}")
    
    print()
    
    # Verificar SDK instalado
    print("2. VERIFICACIÓN DE SDK")
    print("-" * 70)
    
    try:
        import mercadopago
        print("✅ SDK de Mercado Pago instalado")
        print(f"   Versión: {mercadopago.__version__ if hasattr(mercadopago, '__version__') else 'Desconocida'}")
    except ImportError:
        print("❌ SDK de Mercado Pago NO instalado")
        print("   Ejecuta: pip install mercadopago>=2.2.0")
    
    print()
    
    # Verificar PaymentGateway
    print("3. VERIFICACIÓN DE PAYMENT GATEWAY")
    print("-" * 70)
    
    try:
        from pagos.payment_gateway import PaymentGateway, MERCADOPAGO_AVAILABLE
        
        if MERCADOPAGO_AVAILABLE:
            print("✅ Mercado Pago disponible en PaymentGateway")
        else:
            print("❌ Mercado Pago NO disponible (SDK no instalado)")
        
        try:
            gateway = PaymentGateway(pasarela='mercadopago')
            print("✅ PaymentGateway para Mercado Pago inicializado correctamente")
            
            # Verificar métodos
            metodos_requeridos = [
                '_crear_intento_mercadopago',
                '_procesar_reembolso_mercadopago'
            ]
            
            for metodo in metodos_requeridos:
                if hasattr(gateway, metodo):
                    print(f"✅ Método {metodo} existe")
                else:
                    print(f"❌ Método {metodo} NO existe")
            
        except Exception as e:
            print(f"❌ Error al inicializar PaymentGateway: {str(e)}")
            if "no está instalado" in str(e):
                print("   Solución: pip install mercadopago>=2.2.0")
            
    except ImportError as e:
        print(f"❌ Error al importar PaymentGateway: {str(e)}")
    
    print()
    
    # Verificar acceso a API (solo si hay credenciales)
    if mercadopago_token:
        print("4. VERIFICACIÓN DE CONEXIÓN CON MERCADO PAGO")
        print("-" * 70)
        
        try:
            import mercadopago
            sdk = mercadopago.SDK(mercadopago_token)
            
            # Intentar obtener información de la cuenta (método simple)
            try:
                # Verificar que el SDK se puede inicializar
                print("✅ SDK de Mercado Pago inicializado correctamente")
                print("   (No se realiza llamada a API para evitar consumo de recursos)")
            except Exception as e:
                print(f"❌ Error al inicializar SDK: {str(e)}")
                print("   Verifica tus credenciales")
                
        except ImportError:
            print("⚠️  Saltado: SDK no instalado")
        except Exception as e:
            print(f"❌ Error al conectar con Mercado Pago: {str(e)}")
    else:
        print("4. VERIFICACIÓN DE CONEXIÓN CON MERCADO PAGO")
        print("-" * 70)
        print("⚠️  Saltado: Credenciales no configuradas")
    
    print()
    
    # Resumen
    print("=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    
    sdk_instalado = False
    try:
        import mercadopago
        sdk_instalado = True
    except:
        pass
    
    configurado = bool(mercadopago_token and mercadopago_public and site_url and sdk_instalado)
    
    if configurado:
        print("✅ Configuración básica: COMPLETA")
        print()
        print("📝 Próximos pasos:")
        print("   1. Probar el flujo de pago en modo test")
        print("   2. Verificar que los usuarios pueden pagar")
        print("   3. Configurar webhooks (recomendado)")
        print("   4. Cuando estés listo, cambiar a credenciales de producción")
    else:
        print("❌ Configuración básica: INCOMPLETA")
        print()
        print("📝 Pasos para completar:")
        if not sdk_instalado:
            print("   - Instalar SDK: pip install mercadopago>=2.2.0")
        if not mercadopago_token:
            print("   - Agregar MERCADOPAGO_ACCESS_TOKEN en .env")
        if not mercadopago_public:
            print("   - Agregar MERCADOPAGO_PUBLIC_KEY en .env")
        if not site_url:
            print("   - Agregar SITE_URL en .env")
        print()
        print("📖 Ver GUIA_CONFIGURACION_MERCADOPAGO.md para más detalles")
    
    print()
    print("=" * 70)

if __name__ == '__main__':
    verificar_configuracion()



