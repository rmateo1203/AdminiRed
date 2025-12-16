# ⚡ Configuración Rápida de Email (Sin Contraseña de Aplicación)

## 🎯 Opción Más Rápida: Guardar Emails en Archivos

Esta opción guarda los emails como archivos `.txt` en lugar de enviarlos. Perfecto para desarrollo.

### Paso 1: Editar archivo `.env`

Abre tu archivo `.env` y **agrega o cambia** estas líneas:

```env
EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
EMAIL_FILE_PATH=/home/rmateo/Documentos/otros/project/django/AdminiRed/emails
DEFAULT_FROM_EMAIL=AdminiRed <noreply@adminired.com>
```

### Paso 2: Crear directorio (si no existe)

```bash
mkdir -p /home/rmateo/Documentos/otros/project/django/AdminiRed/emails
```

### Paso 3: Reiniciar servidor

```bash
python manage.py runserver
```

### Paso 4: Probar

1. Ve a: http://localhost:8000/password-reset/
2. Solicita recuperación de contraseña
3. Revisa la carpeta `emails/` - ahí estará el email guardado

**Ventajas:**
- ✅ No necesitas configuración de servidor
- ✅ No necesitas contraseñas de aplicación
- ✅ Funciona inmediatamente
- ✅ Puedes ver el contenido completo del email

**Desventajas:**
- ❌ No envía emails reales (solo para desarrollo)

---

## 📧 Si Quieres Enviar Emails Reales

### Opción A: Usar Outlook/Hotmail

Si tienes cuenta de Outlook o Hotmail, puedes usar tu contraseña normal:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@outlook.com
EMAIL_HOST_PASSWORD=tu-contraseña-normal
DEFAULT_FROM_EMAIL=AdminiRed <tu-email@outlook.com>
```

### Opción B: Usar Mailtrap (Gratis)

1. Regístrate en: https://mailtrap.io/ (gratis)
2. Copia las credenciales de tu inbox
3. Configura en `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-usuario-de-mailtrap
EMAIL_HOST_PASSWORD=tu-contraseña-de-mailtrap
DEFAULT_FROM_EMAIL=AdminiRed <noreply@adminired.com>
```

Los emails aparecerán en el dashboard de Mailtrap (no se envían realmente).

---

## 🔍 Verificar Configuración

Después de configurar, ejecuta:

```bash
source venv/bin/activate
python probar_email.py
```

Esto te mostrará si la configuración está correcta.

