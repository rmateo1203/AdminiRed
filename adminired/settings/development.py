"""
Development settings for adminired project.
"""
from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS para desarrollo
# Incluye localhost, 127.0.0.1 y cualquier dominio de ngrok detectado en SITE_URL
default_hosts = 'localhost,127.0.0.1'
allowed_hosts_from_env = config('ALLOWED_HOSTS', default=default_hosts, cast=lambda v: [s.strip() for s in v.split(',')])

# Agregar automáticamente el dominio de ngrok desde SITE_URL si está configurado
ALLOWED_HOSTS = list(allowed_hosts_from_env)

# Extraer dominio de ngrok de SITE_URL y agregarlo a ALLOWED_HOSTS
site_url = config('SITE_URL', default='')
if site_url:
    from urllib.parse import urlparse
    try:
        parsed = urlparse(site_url)
        if parsed.hostname:
            # Agregar el dominio si no está ya en ALLOWED_HOSTS
            if parsed.hostname not in ALLOWED_HOSTS:
                ALLOWED_HOSTS.append(parsed.hostname)
                print(f"✅ Dominio agregado a ALLOWED_HOSTS: {parsed.hostname}")
    except Exception as e:
        print(f"⚠️  Error al procesar SITE_URL para ALLOWED_HOSTS: {e}")

# Database
# PostgreSQL configuration for development
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': config('DB_NAME', default='adminired_dev'),
    'USER': config('DB_USER', default='postgres'),
    'PASSWORD': config('DB_PASSWORD', default='postgres'),
    'HOST': config('DB_HOST', default='localhost'),
    'PORT': config('DB_PORT', default='5432'),
    'OPTIONS': {
        'connect_timeout': 10,
    },
}

# Email configuration for development
# Opción 1: Mostrar emails en consola (por defecto)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Opción 2: Enviar emails reales (descomentar y configurar)
# Para usar Gmail:
# 1. Activa "Permitir el acceso de aplicaciones menos seguras" o usa "Contraseña de aplicación"
# 2. Genera una contraseña de aplicación en: https://myaccount.google.com/apppasswords
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='AdminiRed <noreply@adminired.com>')

# Django Debug Toolbar (opcional, descomentar si lo instalas)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INTERNAL_IPS = ['127.0.0.1']

# Middleware para saltar la advertencia de ngrok en desarrollo
# Agregar al principio del middleware stack para que se ejecute primero
MIDDLEWARE = [
    'core.middleware.NgrokSkipBrowserWarningMiddleware',
] + MIDDLEWARE

