# Alternativas para Envío de Emails (Sin Contraseña de Aplicación)

Si no puedes configurar la contraseña de aplicación de Gmail, aquí tienes alternativas:

## Opción 1: Usar Outlook/Hotmail (Más Fácil)

Outlook permite usar tu contraseña normal sin necesidad de contraseñas de aplicación.

### Configuración:

1. **Edita tu archivo `.env`** y cambia estas líneas:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@outlook.com
EMAIL_HOST_PASSWORD=tu-contraseña-normal
DEFAULT_FROM_EMAIL=AdminiRed <tu-email@outlook.com>
```

2. **Reinicia el servidor**

**Ventajas:**
- No necesitas contraseña de aplicación
- Puedes usar tu contraseña normal
- Funciona inmediatamente

## Opción 2: Usar Mailtrap (Para Desarrollo/Pruebas)

Mailtrap es un servicio gratuito que captura todos los emails en desarrollo sin enviarlos realmente.

### Configuración:

1. **Regístrate gratis en:** https://mailtrap.io/
2. **Obtén tus credenciales** del inbox de prueba
3. **Edita tu archivo `.env`:**

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-usuario-de-mailtrap
EMAIL_HOST_PASSWORD=tu-contraseña-de-mailtrap
DEFAULT_FROM_EMAIL=AdminiRed <noreply@adminired.com>
```

**Ventajas:**
- Gratis para desarrollo
- No envía emails reales (perfecto para pruebas)
- Ver los emails en el dashboard de Mailtrap

## Opción 3: Usar SendGrid (Gratis hasta 100 emails/día)

SendGrid es un servicio profesional de envío de emails.

### Configuración:

1. **Regístrate en:** https://sendgrid.com/ (plan gratuito)
2. **Crea una API Key** en el panel de SendGrid
3. **Edita tu archivo `.env`:**

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu-api-key-de-sendgrid
DEFAULT_FROM_EMAIL=AdminiRed <noreply@tudominio.com>
```

**Ventajas:**
- Gratis hasta 100 emails/día
- Muy confiable
- Bueno para producción

## Opción 4: Activar "Aplicaciones Menos Seguras" en Gmail (Temporal)

⚠️ **ADVERTENCIA:** Esta opción es menos segura y Google puede desactivarla.

### Si Gmail te lo permite:

1. **Ve a:** https://myaccount.google.com/lesssecureapps
2. **Activa** "Permitir el acceso de aplicaciones menos seguras"
3. **Usa tu contraseña normal** en `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=magesccafe@gmail.com
EMAIL_HOST_PASSWORD=mateo1991
DEFAULT_FROM_EMAIL=AdminiRed <magesccafe@gmail.com>
```

**Nota:** Google está eliminando esta opción, puede que no esté disponible.

## Opción 5: Usar Archivo de Email (Solo para Desarrollo)

Para desarrollo local, puedes guardar los emails en archivos en lugar de enviarlos.

### Configuración:

```env
EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
EMAIL_FILE_PATH=/home/rmateo/Documentos/otros/project/django/AdminiRed/emails
DEFAULT_FROM_EMAIL=AdminiRed <noreply@adminired.com>
```

Luego crea el directorio:
```bash
mkdir -p /home/rmateo/Documentos/otros/project/django/AdminiRed/emails
```

**Ventajas:**
- No necesitas configuración de servidor
- Los emails se guardan como archivos .txt
- Perfecto para desarrollo

## Recomendación

**Para desarrollo:** Usa **Mailtrap** (Opción 2) - es gratis y fácil
**Para producción:** Usa **SendGrid** (Opción 3) - es confiable y gratuito

## ¿Por qué no funciona la contraseña de aplicación?

Posibles razones:
1. No tienes verificación en 2 pasos activada
2. Tu cuenta de Google es corporativa (administrada por empresa)
3. Tu cuenta tiene restricciones de seguridad
4. Estás usando una cuenta antigua sin acceso a esta función

