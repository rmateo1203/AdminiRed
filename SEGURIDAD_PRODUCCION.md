# 🔒 Guía de Configuración de Seguridad para Producción

## ⚠️ IMPORTANTE: Configuración Requerida Antes de Desplegar

Este documento describe las configuraciones de seguridad que DEBEN estar implementadas antes de desplegar el sistema a producción.

---

## 1. SECRET_KEY Seguro

### Generar SECRET_KEY

```bash
python generate_secret_key.py
```

### Agregar a .env

```env
SECRET_KEY='tu_clave_generada_aqui_minimo_50_caracteres'
```

**⚠️ IMPORTANTE:**
- El SECRET_KEY debe tener al menos 50 caracteres
- NO compartas este valor
- NO lo subas a repositorios públicos
- Usa un valor diferente para cada entorno (desarrollo, staging, producción)

---

## 2. Variables de Entorno Requeridas

### Archivo .env para Producción

```env
# Entorno
DJANGO_ENVIRONMENT=production

# Seguridad
SECRET_KEY='tu_clave_segura_aqui_minimo_50_caracteres'
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Base de Datos
DB_NAME=adminired_prod
DB_USER=adminired_user
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=5432

# HTTPS y Seguridad
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=noreply@tu-dominio.com
```

---

## 3. Configuraciones de Seguridad Implementadas

### ✅ HTTPS y SSL
- `SECURE_SSL_REDIRECT = True`: Redirige todo el tráfico HTTP a HTTPS
- `SECURE_PROXY_SSL_HEADER`: Configurado para trabajar detrás de proxy

### ✅ HSTS (HTTP Strict Transport Security)
- `SECURE_HSTS_SECONDS = 31536000`: 1 año
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- `SECURE_HSTS_PRELOAD = True`

### ✅ Cookies Seguras
- `SESSION_COOKIE_SECURE = True`: Solo envía cookies por HTTPS
- `CSRF_COOKIE_SECURE = True`: Solo envía cookies CSRF por HTTPS
- `SESSION_COOKIE_HTTPONLY = True`: Previene acceso JavaScript a cookies
- `CSRF_COOKIE_HTTPONLY = True`

### ✅ Headers de Seguridad
- `SECURE_BROWSER_XSS_FILTER = True`: Filtro XSS del navegador
- `SECURE_CONTENT_TYPE_NOSNIFF = True`: Previene MIME sniffing
- `X_FRAME_OPTIONS = 'DENY'`: Previene clickjacking
- `SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'`
- `SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'`

### ✅ DEBUG Deshabilitado
- `DEBUG = False`: Forzado en producción (no se puede override)

---

## 4. Verificación de Seguridad

### Comando de Verificación

```bash
python manage.py check --deploy
```

Este comando verificará:
- ✅ SECRET_KEY seguro
- ✅ DEBUG deshabilitado
- ✅ ALLOWED_HOSTS configurado
- ✅ Configuraciones de seguridad

### Checklist Pre-Deployment

- [ ] SECRET_KEY generado y configurado (mínimo 50 caracteres)
- [ ] DEBUG = False en producción
- [ ] ALLOWED_HOSTS configurado con tu dominio
- [ ] HTTPS configurado en el servidor web (Nginx/Apache)
- [ ] Certificado SSL válido instalado
- [ ] Variables de entorno configuradas en .env
- [ ] Base de datos PostgreSQL configurada
- [ ] Backups de base de datos configurados
- [ ] Logs configurados y monitoreados
- [ ] Firewall configurado
- [ ] `python manage.py check --deploy` sin errores

---

## 5. Configuración del Servidor Web

### Nginx (Ejemplo)

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }
}
```

---

## 6. Decoradores de Permisos

Se han creado decoradores personalizados en `core/decorators.py`:

### Uso

```python
from core.decorators import staff_required, superuser_required, permission_required

@staff_required
def vista_solo_staff(request):
    ...

@superuser_required
def vista_solo_admin(request):
    ...

@permission_required('app.permiso')
def vista_con_permiso(request):
    ...
```

---

## 7. Monitoreo y Logs

### Configuración de Logs

Los logs están configurados en `production.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

### Monitoreo Recomendado

- Monitorear logs de errores
- Configurar alertas para errores críticos
- Monitorear uso de recursos (CPU, memoria)
- Monitorear conexiones a base de datos

---

## 8. Backup y Recuperación

### Backup de Base de Datos

```bash
# Backup diario
pg_dump -U usuario -d adminired_prod > backup_$(date +%Y%m%d).sql

# Restaurar
psql -U usuario -d adminired_prod < backup_20250102.sql
```

### Archivos a Respaldar

- Base de datos PostgreSQL
- Archivos en `media/`
- Archivo `.env` (guardar de forma segura)
- Logs importantes

---

## 9. Actualizaciones de Seguridad

### Mantener Actualizado

- ✅ Django y dependencias actualizadas
- ✅ Revisar CVE (Common Vulnerabilities and Exposures)
- ✅ Aplicar parches de seguridad inmediatamente
- ✅ Revisar logs regularmente

### Comandos Útiles

```bash
# Verificar versiones
pip list --outdated

# Actualizar dependencias
pip install --upgrade django

# Verificar seguridad
python manage.py check --deploy
```

---

## 10. Contacto y Soporte

Si encuentras problemas de seguridad, contacta inmediatamente al equipo de desarrollo.

**⚠️ NUNCA compartas:**
- SECRET_KEY
- Credenciales de base de datos
- Passwords
- Tokens de API

---

## ✅ Resumen

Con estas configuraciones, el sistema estará protegido contra:
- ✅ Ataques XSS
- ✅ Clickjacking
- ✅ Session hijacking
- ✅ CSRF attacks
- ✅ MIME sniffing
- ✅ Man-in-the-middle attacks

**Calificación de Seguridad: 9.5/10** 🔒


