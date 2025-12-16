# 📧 Guía Paso a Paso: Configurar Gmail para AdminiRed

## ⚠️ Requisito Previo: Verificación en 2 Pasos

Gmail requiere que tengas **verificación en 2 pasos activada** para generar contraseñas de aplicación.

---

## 📋 PASO 1: Activar Verificación en 2 Pasos

### Si NO tienes verificación en 2 pasos activada:

1. **Ve a tu cuenta de Google:**
   - Abre: https://myaccount.google.com/security
   - O ve directamente a: https://myaccount.google.com/signinoptions/two-step-verification

2. **Activa la verificación en 2 pasos:**
   - Haz clic en "Verificación en 2 pasos" o "2-Step Verification"
   - Haz clic en "Comenzar" o "Get Started"
   - Sigue las instrucciones:
     - Ingresa tu contraseña
     - Elige un método de verificación (teléfono, app de autenticación)
     - Verifica tu teléfono o configura la app
   - Completa el proceso

3. **Confirma que está activada:**
   - Deberías ver "Verificación en 2 pasos: Activada"

### Si YA tienes verificación en 2 pasos activada:
✅ Puedes pasar directamente al Paso 2.

---

## 🔑 PASO 2: Generar Contraseña de Aplicación

1. **Ve a la página de contraseñas de aplicación:**
   - Abre: https://myaccount.google.com/apppasswords
   - O desde: Google Account → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones

2. **Si te pide verificar tu identidad:**
   - Ingresa tu contraseña de Google
   - Completa la verificación en 2 pasos (código del teléfono o app)

3. **Genera la contraseña:**
   - En "Seleccionar app": Elige **"Correo"**
   - En "Seleccionar dispositivo": Elige **"Otro (nombre personalizado)"**
   - Escribe: **"AdminiRed"**
   - Haz clic en **"Generar"**

4. **Copia la contraseña:**
   - Google te mostrará una contraseña de **16 caracteres**
   - Ejemplo: `abcd efgh ijkl mnop`
   - **IMPORTANTE:** Copia esta contraseña completa
   - Puedes quitar los espacios si quieres: `abcdefghijklmnop`

---

## ⚙️ PASO 3: Configurar el archivo .env

1. **Abre el archivo `.env`** en la raíz del proyecto

2. **Agrega o actualiza estas líneas:**

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=magesccafe@gmail.com
EMAIL_HOST_PASSWORD=TU_CONTRASEÑA_DE_APLICACION_AQUI
DEFAULT_FROM_EMAIL=AdminiRed <magesccafe@gmail.com>
```

3. **Reemplaza:**
   - `TU_CONTRASEÑA_DE_APLICACION_AQUI` → La contraseña de 16 caracteres que copiaste
   - Puedes ponerla con o sin espacios, ambos funcionan

**Ejemplo real:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=magesccafe@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=AdminiRed <magesccafe@gmail.com>
```

---

## 🔄 PASO 4: Reiniciar el Servidor

1. **Detén el servidor Django** (si está corriendo):
   - Presiona `Ctrl + C` en la terminal

2. **Inicia el servidor de nuevo:**
   ```bash
   python manage.py runserver
   ```

---

## ✅ PASO 5: Probar que Funciona

### Opción A: Probar desde el script

```bash
source venv/bin/activate
python probar_email.py
```

Deberías ver: `✅ Email enviado exitosamente!`

### Opción B: Probar desde la aplicación

1. Ve a: http://localhost:8000/password-reset/
2. Ingresa un email de usuario que exista en tu sistema
3. Revisa tu correo (y la carpeta de spam)

---

## ❌ Solución de Problemas

### Error: "No puedo acceder a apppasswords"

**Causa:** No tienes verificación en 2 pasos activada.

**Solución:** 
1. Activa verificación en 2 pasos primero (Paso 1)
2. Espera unos minutos
3. Intenta acceder de nuevo a apppasswords

### Error: "Username and Password not accepted"

**Causa:** Estás usando la contraseña incorrecta.

**Solución:**
1. Verifica que copiaste la contraseña de aplicación completa (16 caracteres)
2. Asegúrate de que no haya espacios extra al inicio o final
3. Intenta sin espacios: `abcdefghijklmnop` en lugar de `abcd efgh ijkl mnop`

### Error: "Please log in via your web browser"

**Causa:** Gmail detectó un intento de acceso sospechoso.

**Solución:**
1. Ve a: https://myaccount.google.com/security
2. Revisa "Actividad reciente de seguridad"
3. Si hay alertas, confírmalas
4. Intenta de nuevo

### No aparece la opción "Contraseñas de aplicaciones"

**Causa:** Tu cuenta puede tener restricciones.

**Solución:**
1. Verifica que la verificación en 2 pasos esté realmente activada
2. Intenta desde otro navegador
3. Si usas cuenta de Google Workspace (empresa), contacta al administrador

---

## 📝 Checklist Final

Antes de probar, verifica:

- [ ] Verificación en 2 pasos está activada
- [ ] Generaste la contraseña de aplicación
- [ ] Copiaste la contraseña de 16 caracteres
- [ ] Agregaste `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` en .env
- [ ] Actualizaste `EMAIL_HOST_PASSWORD` con la contraseña de aplicación
- [ ] Reiniciaste el servidor Django

---

## 🆘 Si Aún No Funciona

Si después de seguir todos los pasos no funciona, puedes:

1. **Usar Outlook/Hotmail** (más fácil, no necesita contraseña de aplicación)
2. **Usar Mailtrap** (para desarrollo, captura emails sin enviarlos)
3. **Guardar emails en archivos** (para desarrollo local)

Ver `ALTERNATIVAS_EMAIL.md` para más opciones.

