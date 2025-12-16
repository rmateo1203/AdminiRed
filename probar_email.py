#!/usr/bin/env python
"""
Script para probar la configuración de email
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings.development')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

def probar_email():
    print("=" * 60)
    print("CONFIGURACIÓN ACTUAL DE EMAIL")
    print("=" * 60)
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    password_display = '*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NO CONFIGURADA'
    print(f"EMAIL_HOST_PASSWORD: {password_display}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 60)
    
    # Verificar si está usando consola
    if 'console' in settings.EMAIL_BACKEND:
        print("\n⚠️  ADVERTENCIA: Estás usando el backend de consola.")
        print("   Los emails solo se mostrarán en la terminal, no se enviarán.")
        print("   Para enviar emails reales, configura EMAIL_BACKEND en .env:")
        print("   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
        return
    
    # Intentar enviar email de prueba
    print("\n📧 Intentando enviar email de prueba...")
    try:
        send_mail(
            'Prueba de Email - AdminiRed',
            'Este es un email de prueba. Si recibes esto, la configuración funciona correctamente.\n\n'
            'Este email fue enviado desde el sistema AdminiRed para verificar la configuración.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],  # Enviar a sí mismo
            fail_silently=False,
        )
        print("✅ Email enviado exitosamente!")
        print(f"📬 Revisa tu correo: {settings.EMAIL_HOST_USER}")
        print("   (También revisa la carpeta de spam)")
    except Exception as e:
        print(f"\n❌ ERROR al enviar email:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        print("\n" + "=" * 60)
        print("💡 SOLUCIÓN:")
        print("=" * 60)
        
        error_msg = str(e).lower()
        
        if "username and password not accepted" in error_msg or "invalid credentials" in error_msg or "535" in error_msg:
            print("\n🔐 PROBLEMA: Credenciales inválidas")
            print("\n   Estás usando tu contraseña normal de Gmail.")
            print("   Gmail NO permite usar contraseñas normales para aplicaciones.")
            print("\n   SOLUCIÓN:")
            print("   1. Ve a: https://myaccount.google.com/apppasswords")
            print("   2. Si no tienes verificación en 2 pasos, actívala primero:")
            print("      https://myaccount.google.com/security")
            print("   3. Genera una 'Contraseña de aplicación':")
            print("      - Aplicación: Correo")
            print("      - Dispositivo: Otro (nombre personalizado)")
            print("      - Nombre: AdminiRed")
            print("   4. Copia la contraseña de 16 caracteres")
            print("   5. Actualiza .env con:")
            print(f"      EMAIL_HOST_PASSWORD=la_contraseña_de_16_caracteres")
            
        elif "please log in via your web browser" in error_msg or "web browser" in error_msg:
            print("\n🔐 PROBLEMA: Verificación requerida")
            print("\n   Gmail requiere verificación en 2 pasos activada.")
            print("\n   SOLUCIÓN:")
            print("   1. Activa verificación en 2 pasos:")
            print("      https://myaccount.google.com/security")
            print("   2. Luego genera una contraseña de aplicación:")
            print("      https://myaccount.google.com/apppasswords")
            
        elif "connection" in error_msg or "timeout" in error_msg:
            print("\n🌐 PROBLEMA: Error de conexión")
            print("\n   No se puede conectar al servidor SMTP de Gmail.")
            print("\n   SOLUCIÓN:")
            print("   1. Verifica tu conexión a internet")
            print("   2. Verifica que el puerto 587 no esté bloqueado")
            print("   3. Prueba con otro proveedor de email")
            
        else:
            print(f"\n   Error desconocido: {e}")
            print("\n   Verifica:")
            print("   1. Que EMAIL_BACKEND esté configurado correctamente")
            print("   2. Que todas las variables de EMAIL estén en .env")
            print("   3. Que estés usando una contraseña de aplicación, no tu contraseña normal")

if __name__ == '__main__':
    probar_email()

