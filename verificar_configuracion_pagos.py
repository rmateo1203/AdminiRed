#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script simple para verificar si las pasarelas de pago están configuradas
Ejecutar desde la raíz del proyecto
"""
import os

print("=" * 70)
print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE PASARELAS DE PAGO")
print("=" * 70)
print()

# Leer archivo .env directamente
env_path = '.env'
configuradas = []

if os.path.exists(env_path):
    print("📄 Archivo .env encontrado")
    print()
    
    with open(env_path, 'r') as f:
        contenido = f.read()
    
    # Verificar Mercado Pago
    tiene_mp_token = 'MERCADOPAGO_ACCESS_TOKEN=' in contenido
    tiene_mp_key = 'MERCADOPAGO_PUBLIC_KEY=' in contenido
    
    if tiene_mp_token:
        line = [l for l in contenido.split('\n') if 'MERCADOPAGO_ACCESS_TOKEN=' in l and not l.strip().startswith('#')][0] if any('MERCADOPAGO_ACCESS_TOKEN=' in l and not l.strip().startswith('#') for l in contenido.split('\n')) else None
        if line:
            valor = line.split('=', 1)[1].strip()
            if valor and valor not in ['', 'tu_access_token_aqui', 'TEST-', 'APP_USR-']:
                print("✅ MERCADOPAGO_ACCESS_TOKEN: Configurado")
                configuradas.append('Mercado Pago')
            else:
                print("⚠️  MERCADOPAGO_ACCESS_TOKEN: Variable existe pero está vacía o es un placeholder")
        else:
            print("⚠️  MERCADOPAGO_ACCESS_TOKEN: Variable encontrada pero comentada o sin valor")
    else:
        print("❌ MERCADOPAGO_ACCESS_TOKEN: NO configurado")
    
    # Verificar PayPal
    tiene_pp_client = 'PAYPAL_CLIENT_ID=' in contenido
    tiene_pp_secret = 'PAYPAL_SECRET=' in contenido
    
    if tiene_pp_client and tiene_pp_secret:
        client_line = [l for l in contenido.split('\n') if 'PAYPAL_CLIENT_ID=' in l and not l.strip().startswith('#')][0] if any('PAYPAL_CLIENT_ID=' in l and not l.strip().startswith('#') for l in contenido.split('\n')) else None
        secret_line = [l for l in contenido.split('\n') if 'PAYPAL_SECRET=' in l and not l.strip().startswith('#')][0] if any('PAYPAL_SECRET=' in l and not l.strip().startswith('#') for l in contenido.split('\n')) else None
        
        if client_line and secret_line:
            client_valor = client_line.split('=', 1)[1].strip()
            secret_valor = secret_line.split('=', 1)[1].strip()
            if client_valor and secret_valor and client_valor not in ['', 'tu_client_id_aqui'] and secret_valor not in ['', 'tu_secret_aqui']:
                print("✅ PAYPAL_CLIENT_ID y PAYPAL_SECRET: Configurados")
                configuradas.append('PayPal')
            else:
                print("⚠️  PAYPAL: Variables existen pero están vacías o son placeholders")
        else:
            print("⚠️  PAYPAL: Variables encontradas pero comentadas o sin valor")
    else:
        print("❌ PAYPAL: NO configurado (faltan CLIENT_ID o SECRET)")
    
    # Verificar Stripe
    tiene_stripe = 'STRIPE_SECRET_KEY=' in contenido
    if tiene_stripe:
        line = [l for l in contenido.split('\n') if 'STRIPE_SECRET_KEY=' in l and not l.strip().startswith('#')][0] if any('STRIPE_SECRET_KEY=' in l and not l.strip().startswith('#') for l in contenido.split('\n')) else None
        if line:
            valor = line.split('=', 1)[1].strip()
            if valor and valor not in ['', 'tu_secret_key_aqui', 'sk_test_', 'sk_live_']:
                print("✅ STRIPE_SECRET_KEY: Configurado")
                configuradas.append('Stripe')
            else:
                print("⚠️  STRIPE_SECRET_KEY: Variable existe pero está vacía o es un placeholder")
        else:
            print("⚠️  STRIPE_SECRET_KEY: Variable encontrada pero comentada o sin valor")
    else:
        print("❌ STRIPE_SECRET_KEY: NO configurado")
    
else:
    print("❌ Archivo .env NO encontrado")
    print("   Crea un archivo .env en la raíz del proyecto")

print()
print("=" * 70)
print("📊 RESUMEN")
print("=" * 70)

if configuradas:
    print(f"✅ Pasarelas configuradas: {', '.join(configuradas)}")
    print()
    print("💡 Si aún ves el mensaje 'no están configuradas':")
    print("   1. Reinicia el servidor de Django")
    print("   2. Verifica que las variables en .env no tengan espacios extras")
    print("   3. Asegúrate de que las credenciales sean válidas")
else:
    print("❌ Ninguna pasarela está configurada")
    print()
    print("📝 Pasos para configurar:")
    print()
    print("1. Edita el archivo .env en la raíz del proyecto")
    print()
    print("2. Agrega las credenciales (al menos una):")
    print()
    print("   Para Mercado Pago (Test):")
    print("   MERCADOPAGO_ACCESS_TOKEN=TEST-tu_token_aqui")
    print("   MERCADOPAGO_PUBLIC_KEY=TEST-tu_key_aqui")
    print()
    print("   Para PayPal (Sandbox):")
    print("   PAYPAL_CLIENT_ID=tu_client_id_aqui")
    print("   PAYPAL_SECRET=tu_secret_aqui")
    print("   PAYPAL_MODE=sandbox")
    print()
    print("3. Guarda el archivo .env")
    print()
    print("4. Reinicia el servidor Django")
    print()
    print("📖 Para más detalles, ver:")
    print("   - DEMO_PAGOS_MERCADOPAGO_PAYPAL.md")
    print("   - GUIA_CONFIGURACION_MERCADOPAGO.md")
    print("   - GUIA_CONFIGURACION_PAYPAL.md")

print()
print("=" * 70)


