# 🔑 Guía Paso a Paso: Obtener Credenciales de Mercado Pago y PayPal

## 📋 Índice

1. [Obtener Credenciales de Mercado Pago](#mercado-pago)
2. [Obtener Credenciales de PayPal](#paypal)
3. [Configurar en el Proyecto](#configurar-en-el-proyecto)

---

## 🔵 Mercado Pago

### Paso 1: Crear Cuenta o Iniciar Sesión

1. Ve a: **https://www.mercadopago.com.mx/developers**
2. Haz clic en **"Iniciar sesión"** o **"Crear cuenta"**
3. Si no tienes cuenta, completa el registro

### Paso 2: Crear una Aplicación

1. Una vez dentro del panel, busca el menú lateral izquierdo
2. Haz clic en **"Tus integraciones"** o busca en el menú superior
3. Haz clic en el botón **"Crear nueva aplicación"** o **"Nueva aplicación"**

### Paso 3: Completar el Formulario

Completa los siguientes campos:

- **Nombre de la aplicación**: `AdminiRed` (o el nombre que prefieras)
- **Sitio web**: `http://localhost:8000` (para desarrollo) o tu dominio
- **Categoría**: Selecciona "Otros servicios" o la más apropiada
- **Plataforma**: Selecciona **"Web"**

4. Haz clic en **"Crear aplicación"**

### Paso 4: Obtener Credenciales de Prueba (TEST)

1. Una vez creada la aplicación, verás una página con dos pestañas:
   - **"Credenciales de producción"** (No usar todavía)
   - **"Credenciales de prueba"** ← **Usa esta**

2. Haz clic en la pestaña **"Credenciales de prueba"**

3. Verás dos campos importantes:
   - **Access Token**: Empieza con `TEST-...` (Largo, cópialo completo)
   - **Public Key**: Empieza con `TEST-...` (También cópialo)

4. **Copia ambos valores** y guárdalos en un lugar seguro

### Paso 5: Verificar las Credenciales

Las credenciales de prueba deben tener este formato:

```
Access Token: TEST-1234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk
Public Key: TEST-abcdefghijk-01234567890-abcdefghijk
```

✅ **Listo para Mercado Pago!** Ya tienes las credenciales de prueba.

---

## 🟠 PayPal

### Paso 1: Crear Cuenta de Desarrollador

1. Ve a: **https://developer.paypal.com/**
2. Haz clic en **"Sign Up"** (Registrarse) o **"Log In"** (Iniciar sesión)
3. Si no tienes cuenta:
   - Puedes usar tu cuenta de PayPal existente
   - O crear una cuenta nueva

### Paso 2: Acceder al Dashboard

1. Una vez dentro, verás el **Dashboard** de PayPal Developer
2. En el menú superior, busca **"Dashboard"** o ve directamente a:
   - **https://developer.paypal.com/dashboard**

### Paso 3: Crear una Aplicación Sandbox

1. En el Dashboard, busca la sección **"My Apps & Credentials"**
2. Haz clic en el botón **"Create App"** (Crear aplicación)

### Paso 4: Completar el Formulario

Completa los siguientes campos:

- **App Name**: `AdminiRed` (o el nombre que prefieras)
- **Merchant**: Selecciona tu cuenta (si tienes varias)
- **Environment**: ⚠️ **Selecciona "Sandbox"** (NO "Live" todavía)
- **Webhooks**: Puedes dejarlo vacío por ahora

4. Haz clic en **"Create App"**

### Paso 5: Obtener las Credenciales

1. Después de crear la aplicación, verás una página con:
   - **Client ID**: Cadena larga que empieza con letras (ej: `AeA1B2C3...`)
   - **Secret**: Cadena larga (haz clic en **"Show"** para verla)

2. **IMPORTANTE**: El Secret solo se muestra una vez, cópialo inmediatamente

3. **Copia ambos valores**:
   - **Client ID**: Ejemplo `AeA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0`
   - **Secret**: Ejemplo `EF1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1`

### Paso 6: Verificar las Credenciales

Las credenciales de PayPal deben tener este formato:

```
Client ID: AeA1B2C3D4E5... (Largo, solo letras y números)
Secret: EF1G2H3I4J5K6... (Largo, solo letras y números)
```

✅ **Listo para PayPal!** Ya tienes las credenciales de Sandbox.

---

## ⚙️ Configurar en el Proyecto

### Paso 1: Abrir el archivo .env

1. Ve a la raíz de tu proyecto Django
2. Abre el archivo `.env` con tu editor de texto favorito
3. Si no existe, créalo en la raíz del proyecto

### Paso 2: Agregar Credenciales de Mercado Pago

Agrega estas líneas al final del archivo `.env`:

```env
# Mercado Pago - Credenciales de TEST
MERCADOPAGO_ACCESS_TOKEN=TEST-1234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk
MERCADOPAGO_PUBLIC_KEY=TEST-abcdefghijk-01234567890-abcdefghijk
```

⚠️ **Reemplaza** los valores de ejemplo con tus credenciales reales copiadas de Mercado Pago.

### Paso 3: Agregar Credenciales de PayPal

Agrega estas líneas al archivo `.env`:

```env
# PayPal - Credenciales de SANDBOX
PAYPAL_CLIENT_ID=AeA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0
PAYPAL_SECRET=EF1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1
PAYPAL_MODE=sandbox
```

⚠️ **Reemplaza** los valores de ejemplo con tus credenciales reales copiadas de PayPal.

### Paso 4: Agregar URL del Sitio (Importante)

Asegúrate de tener esta línea en tu `.env`:

```env
SITE_URL=http://localhost:8000
```

Si ya existe, verifica que esté correcta.

### Paso 5: Ejemplo Completo de .env

Tu archivo `.env` debería verse así (con tus credenciales reales):

```env
# Otras configuraciones que ya tengas...
SECRET_KEY=tu_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ... más configuraciones ...

# URL del sitio
SITE_URL=http://localhost:8000

# Mercado Pago - Credenciales de TEST
MERCADOPAGO_ACCESS_TOKEN=TEST-tu_access_token_real_aqui
MERCADOPAGO_PUBLIC_KEY=TEST-tu_public_key_real_aqui

# PayPal - Credenciales de SANDBOX
PAYPAL_CLIENT_ID=tu_client_id_real_aqui
PAYPAL_SECRET=tu_secret_real_aqui
PAYPAL_MODE=sandbox
```

### Paso 6: Guardar el Archivo

1. Guarda el archivo `.env`
2. Asegúrate de que no haya espacios antes o después del signo `=`
3. Verifica que las credenciales estén completas (sin cortes)

---

## ✅ Verificar que Funciona

### Paso 1: Verificar Configuración

Ejecuta este comando en la terminal (desde la raíz del proyecto):

```bash
python3 verificar_configuracion_pagos.py
```

Deberías ver algo como:

```
✅ MERCADOPAGO_ACCESS_TOKEN: Configurado
✅ PAYPAL_CLIENT_ID y PAYPAL_SECRET: Configurados
✅ Pasarelas configuradas: Mercado Pago, PayPal
```

### Paso 2: Reiniciar el Servidor

**MUY IMPORTANTE**: Después de modificar `.env`, reinicia el servidor:

1. Si el servidor está corriendo, deténlo con `Ctrl+C`
2. Inicia el servidor de nuevo:
   ```bash
   python manage.py runserver
   ```

### Paso 3: Probar en el Portal

1. Ve al portal del cliente: http://localhost:8000/clientes/portal/mis-pagos/
2. Haz clic en un pago pendiente o vencido
3. Ahora deberías ver el botón **"Pagar en Línea"** 🎉

---

## 🆘 Solución de Problemas

### Problema: No puedo crear cuenta en Mercado Pago

**Solución:**
- Puedes usar cualquier cuenta de correo
- Si ya tienes cuenta de Mercado Pago, usa esa
- El registro es gratuito

### Problema: No veo "Credenciales de prueba" en Mercado Pago

**Solución:**
- Asegúrate de estar en la sección correcta: "Tus integraciones"
- Haz clic en la aplicación que creaste
- Busca las pestañas "Producción" y "Prueba"
- Haz clic en "Prueba"

### Problema: No puedo ver el Secret de PayPal

**Solución:**
- El Secret solo se muestra una vez cuando creas la aplicación
- Si lo perdiste, debes crear una nueva aplicación
- O generar nuevas credenciales desde el dashboard

### Problema: Las credenciales no funcionan

**Soluciones:**
1. Verifica que copiaste las credenciales completas (sin cortes)
2. Verifica que no hay espacios extras en el `.env`
3. Asegúrate de que las líneas no estén comentadas (no empiecen con `#`)
4. Verifica que reiniciaste el servidor después de modificar `.env`
5. Ejecuta `python3 verificar_configuracion_pagos.py` para diagnosticar

### Problema: El archivo .env no existe

**Solución:**
1. Crea un nuevo archivo llamado `.env` en la raíz del proyecto
2. Puedes copiar de `.env.example` si existe:
   ```bash
   cp .env.example .env
   ```
3. Edita el archivo `.env` y agrega las credenciales

---

## 📞 Enlaces Directos

### Mercado Pago
- **Panel de desarrolladores**: https://www.mercadopago.com.mx/developers
- **Tus integraciones**: https://www.mercadopago.com.mx/developers/panel/app
- **Documentación**: https://www.mercadopago.com.mx/developers/es/docs

### PayPal
- **Developer Dashboard**: https://developer.paypal.com/dashboard
- **Crear App**: https://developer.paypal.com/dashboard/applications/create
- **Documentación**: https://developer.paypal.com/docs/

---

## ✨ Checklist Final

Antes de probar, verifica:

- [ ] Creé cuenta en Mercado Pago Developers
- [ ] Creé una aplicación en Mercado Pago
- [ ] Copié el Access Token de prueba (empieza con TEST-)
- [ ] Copié la Public Key de prueba (empieza con TEST-)
- [ ] Creé cuenta en PayPal Developer
- [ ] Creé una aplicación Sandbox en PayPal
- [ ] Copié el Client ID de PayPal
- [ ] Copié el Secret de PayPal (hice clic en "Show")
- [ ] Agregué todas las credenciales al archivo .env
- [ ] Guardé el archivo .env
- [ ] Verifiqué con `python3 verificar_configuracion_pagos.py`
- [ ] Reinicié el servidor Django
- [ ] Probé en el portal del cliente

---

## 🎯 Próximos Pasos

Una vez configuradas las credenciales:

1. **Probar el demo**: Sigue las instrucciones en `DEMO_PAGOS_MERCADOPAGO_PAYPAL.md`
2. **Crear datos de prueba**: Ejecuta `python crear_datos_demo.py`
3. **Probar pagos**: Usa las tarjetas de prueba documentadas

---

**¡Ahora tienes todo lo necesario para obtener las credenciales!** 🚀

Si encuentras algún problema durante el proceso, revisa la sección "Solución de Problemas" o las guías detalladas en:
- `GUIA_CONFIGURACION_MERCADOPAGO.md`
- `GUIA_CONFIGURACION_PAYPAL.md`

