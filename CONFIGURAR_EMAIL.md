# Configuración de Email para Recuperación de Contraseña

## Problema Actual

Los correos no llegan porque está configurado el **backend de consola**, que solo muestra los emails en la terminal del servidor Django, no los envía realmente.

## Soluciones

### Opción 1: Usar Gmail (Recomendado para desarrollo)

1. **Crear una contraseña de aplicación en Gmail:**
   - Ve a: https://myaccount.google.com/apppasswords
   - Selecciona "Correo" y "Otro (nombre personalizado)"
   - Escribe "AdminiRed" y genera la contraseña
   - Copia la contraseña generada (16 caracteres)

2. **Configurar variables de entorno:**

   Crea un archivo `.env` en la raíz del proyecto (si no existe) y agrega:

   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=tu-email@gmail.com
   EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación-16-caracteres
   DEFAULT_FROM_EMAIL=AdminiRed <tu-email@gmail.com>
   ```

3. **Reiniciar el servidor Django**

### Opción 2: Usar otro proveedor SMTP

#### Outlook/Hotmail:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@outlook.com
EMAIL_HOST_PASSWORD=tu-contraseña
DEFAULT_FROM_EMAIL=AdminiRed <tu-email@outlook.com>
```

#### SendGrid (Gratis hasta 100 emails/día):
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu-api-key-de-sendgrid
DEFAULT_FROM_EMAIL=AdminiRed <noreply@tudominio.com>
```

#### Mailgun (Gratis hasta 5,000 emails/mes):
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=postmaster@tudominio.mailgun.org
EMAIL_HOST_PASSWORD=tu-contraseña-de-mailgun
DEFAULT_FROM_EMAIL=AdminiRed <noreply@tudominio.com>
```

### Opción 3: Mantener consola para desarrollo (actual)

Si solo quieres ver los emails en la consola para desarrollo, no necesitas cambiar nada. Los emails aparecerán en la terminal cuando ejecutes `python manage.py runserver`.

Para ver los emails:
1. Ejecuta el servidor: `python manage.py runserver`
2. Solicita recuperación de contraseña
3. Revisa la consola donde está corriendo el servidor - ahí verás el email completo

## Verificar Configuración

Para verificar que la configuración funciona, puedes usar el shell de Django:

```bash
python manage.py shell
```

Luego ejecuta:

```python
from django.core.mail import send_mail
from django.conf import settings

print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

# Enviar email de prueba
send_mail(
    'Prueba de Email',
    'Este es un email de prueba desde AdminiRed',
    settings.DEFAULT_FROM_EMAIL,
    ['tu-email-destino@gmail.com'],
    fail_silently=False,
)
```

## Notas Importantes

1. **Seguridad**: Nunca subas el archivo `.env` al repositorio. Agrégalo a `.gitignore`
2. **Gmail**: Si usas Gmail, necesitas una "Contraseña de aplicación", no tu contraseña normal
3. **Firewall**: Asegúrate de que el puerto 587 no esté bloqueado
4. **Spam**: Los emails pueden llegar a spam la primera vez

## Archivo .env de Ejemplo

```env
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=mi-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=AdminiRed <mi-email@gmail.com>
```

