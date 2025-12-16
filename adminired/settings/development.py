"""
Development settings for adminired project.
"""
from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

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

