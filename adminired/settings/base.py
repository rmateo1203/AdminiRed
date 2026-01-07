"""
Base settings for adminired project.

These settings are shared across all environments.
"""
from pathlib import Path
from decouple import config
import secrets
import string

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECRET_KEY
# Generar uno seguro si no existe (solo para desarrollo)
# En producción, DEBE estar en .env con al menos 50 caracteres
SECRET_KEY = config('SECRET_KEY', default=None)
if SECRET_KEY is None:
    # Generar clave temporal para desarrollo (NO usar en producción)
    alphabet = string.ascii_letters + string.digits + string.punctuation
    SECRET_KEY = ''.join(secrets.choice(alphabet) for i in range(50))
    print("⚠️  ADVERTENCIA: SECRET_KEY generado automáticamente. NO usar en producción!")
else:
    # Validar que la clave tenga al menos 50 caracteres
    if len(SECRET_KEY) < 50:
        raise ValueError(
            "SECRET_KEY debe tener al menos 50 caracteres. "
            "Ejecuta: python generate_secret_key.py para generar uno seguro."
        )


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'simple_history',
    # Aplicaciones locales
    'core',
    'clientes',
    'instalaciones',
    'pagos',
    'inventario',
    'notificaciones',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'adminired.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.sidebar_config',
                'core.context_processors.sistema_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'adminired.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# PostgreSQL configuration (can be overridden in development.py or production.py)
# If DB_NAME is not set, falls back to SQLite for compatibility
DB_NAME = config('DB_NAME', default=None)
if DB_NAME:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            'OPTIONS': {
                'connect_timeout': 10,
            },
        }
    }
else:
    # Fallback to SQLite if PostgreSQL is not configured
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Pasarela de Pago - Stripe
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')

# Pasarela de Pago - Mercado Pago
MERCADOPAGO_ACCESS_TOKEN = config('MERCADOPAGO_ACCESS_TOKEN', default='')
MERCADOPAGO_PUBLIC_KEY = config('MERCADOPAGO_PUBLIC_KEY', default='')

# Pasarela de Pago - PayPal
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID', default='')
PAYPAL_SECRET = config('PAYPAL_SECRET', default='')
PAYPAL_MODE = config('PAYPAL_MODE', default='sandbox')  # sandbox o live

# URL del sitio (para webhooks y redirects)
SITE_URL = config('SITE_URL', default='http://localhost:8000')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Email configuration (para recuperación de contraseña)
# Por defecto usa consola (muestra emails en terminal)
# Para enviar emails reales, configura las variables en .env o development.py
# Ver CONFIGURAR_EMAIL.md para más detalles

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='AdminiRed <noreply@adminired.com>')

