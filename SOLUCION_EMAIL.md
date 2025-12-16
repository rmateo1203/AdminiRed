# 🔧 Solución: Correos No Llegan

## ❌ Problema Detectado

Estás usando tu **contraseña normal de Gmail** (`mateo1991`) en el archivo `.env`.

Gmail **NO permite** usar contraseñas normales para aplicaciones de terceros por seguridad.

## ✅ Solución: Usar Contraseña de Aplicación

### Paso 1: Activar Verificación en 2 Pasos (si no la tienes)

1. Ve a: https://myaccount.google.com/security
2. Busca "Verificación en 2 pasos"
3. Actívala si no está activada
4. Sigue las instrucciones para configurarla

### Paso 2: Generar Contraseña de Aplicación

1. **Ve a:** https://myaccount.google.com/apppasswords
   - O desde: Google Account → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones

2. **Genera la contraseña:**
   - **Aplicación:** Selecciona "Correo"
   - **Dispositivo:** Selecciona "Otro (nombre personalizado)"
   - **Nombre:** Escribe "AdminiRed"
   - Haz clic en **"Generar"**

3. **Copia la contraseña:**
   - Google te mostrará una contraseña de **16 caracteres**
   - Ejemplo: `abcd efgh ijkl mnop`
   - **Copia esta contraseña completa** (puedes quitar los espacios)

### Paso 3: Actualizar el archivo .env

Abre el archivo `.env` y **reemplaza** esta línea:

```env
EMAIL_HOST_PASSWORD=mateo1991
```

Por:

```env
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

**Reemplaza `abcd efgh ijkl mnop` con la contraseña de aplicación que copiaste.**

### Paso 4: Verificar que EMAIL_BACKEND esté configurado

Asegúrate de que en tu `.env` también tengas:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

Si no está, agrégalo.

### Paso 5: Reiniciar el Servidor

```bash
# Detén el servidor (Ctrl+C)
# Reinicia:
python manage.py runserver
```

### Paso 6: Probar

1. Ve a: http://localhost:8000/password-reset/
2. Ingresa un email de usuario que exista en el sistema
3. Revisa tu correo (y la carpeta de spam)

## 🔍 Verificar Configuración

Ejecuta este comando para ver tu configuración actual:

```bash
cd /home/rmateo/Documentos/otros/project/django/AdminiRed
source venv/bin/activate
python probar_email.py
```

## ⚠️ Errores Comunes

### Error: "Username and Password not accepted"

**Causa:** Estás usando tu contraseña normal.

**Solución:** Usa una contraseña de aplicación (ver Paso 2).

### Error: "Please log in via your web browser"

**Causa:** No tienes verificación en 2 pasos activada.

**Solución:** Actívala primero (ver Paso 1).

### El email no aparece

1. Revisa la carpeta de **spam/correo no deseado**
2. Verifica que el email del usuario **exista en la base de datos**
3. Revisa la consola del servidor por errores

## 📝 Ejemplo de .env Correcto

```env
# Email Configuration - Gmail
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=magesccafe@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=AdminiRed <magesccafe@gmail.com>
```

**Importante:** Reemplaza `abcd efgh ijkl mnop` con tu contraseña de aplicación real.

