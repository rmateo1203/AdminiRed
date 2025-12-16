# Configuración de Gmail para AdminiRed

## Pasos para Configurar Gmail

### 1. Obtener Contraseña de Aplicación de Gmail

**IMPORTANTE:** Gmail no permite usar tu contraseña normal. Necesitas crear una "Contraseña de aplicación".

#### Pasos:

1. **Ve a tu cuenta de Google:**
   - Abre: https://myaccount.google.com/apppasswords
   - O ve a: Google Account → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones

2. **Si no tienes verificación en 2 pasos activada:**
   - Primero debes activarla en: https://myaccount.google.com/security
   - Es necesario para generar contraseñas de aplicación

3. **Generar la contraseña:**
   - En "Contraseñas de aplicaciones", selecciona:
     - **Aplicación:** Correo
     - **Dispositivo:** Otro (nombre personalizado)
     - **Nombre:** AdminiRed
   - Haz clic en "Generar"

4. **Copia la contraseña:**
   - Google te mostrará una contraseña de 16 caracteres
   - Ejemplo: `abcd efgh ijkl mnop`
   - **Copia esta contraseña completa** (puedes quitar los espacios)

### 2. Configurar el archivo .env

1. **Abre el archivo `.env`** en la raíz del proyecto

2. **Reemplaza estos valores:**
   ```env
   EMAIL_HOST_USER=tu-email@gmail.com
   EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
   DEFAULT_FROM_EMAIL=AdminiRed <tu-email@gmail.com>
   ```

   **Ejemplo real:**
   ```env
   EMAIL_HOST_USER=miempresa@gmail.com
   EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
   DEFAULT_FROM_EMAIL=AdminiRed <miempresa@gmail.com>
   ```

3. **Guarda el archivo**

### 3. Reiniciar el Servidor

```bash
# Detén el servidor (Ctrl+C si está corriendo)
# Luego inicia de nuevo:
python manage.py runserver
```

### 4. Probar el Envío

1. Ve a: http://localhost:8000/password-reset/
2. Ingresa un email de usuario que exista en el sistema
3. Revisa tu correo (y la carpeta de spam si no aparece)

## Solución de Problemas

### Error: "Username and Password not accepted"

**Causa:** Estás usando tu contraseña normal en lugar de la contraseña de aplicación.

**Solución:** 
- Asegúrate de usar la contraseña de aplicación de 16 caracteres
- Verifica que no tenga espacios o córtalos si los tiene

### Error: "Please log in via your web browser"

**Causa:** Gmail bloquea el acceso porque no tienes verificación en 2 pasos activada.

**Solución:**
- Activa la verificación en 2 pasos en tu cuenta de Google
- Luego genera una nueva contraseña de aplicación

### El email no llega

**Verifica:**
1. Revisa la carpeta de spam/correo no deseado
2. Verifica que el email del usuario exista en la base de datos
3. Revisa la consola del servidor por errores
4. Verifica que la contraseña de aplicación sea correcta

### Probar desde la consola de Django

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

# Ver configuración actual
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

# Enviar email de prueba
try:
    send_mail(
        'Prueba de Email - AdminiRed',
        'Este es un email de prueba. Si recibes esto, la configuración funciona correctamente.',
        settings.DEFAULT_FROM_EMAIL,
        ['tu-email-destino@gmail.com'],  # Cambia por tu email
        fail_silently=False,
    )
    print("✅ Email enviado exitosamente!")
except Exception as e:
    print(f"❌ Error: {e}")
```

## Notas Importantes

1. **Seguridad:** El archivo `.env` ya está en `.gitignore`, así que no se subirá al repositorio
2. **Espacios:** La contraseña de aplicación puede tener espacios, pero puedes quitarlos
3. **Expiración:** Las contraseñas de aplicación no expiran, pero puedes revocarlas cuando quieras
4. **Múltiples aplicaciones:** Puedes crear diferentes contraseñas para diferentes aplicaciones

## Configuración Alternativa (Sin verificación en 2 pasos)

Si no puedes activar la verificación en 2 pasos, puedes usar:

1. **"Permitir el acceso de aplicaciones menos seguras"** (no recomendado por seguridad)
   - Ve a: https://myaccount.google.com/lesssecureapps
   - Actívalo temporalmente
   - Usa tu contraseña normal en `EMAIL_HOST_PASSWORD`

⚠️ **Advertencia:** Esta opción es menos segura y Google puede desactivarla automáticamente.

