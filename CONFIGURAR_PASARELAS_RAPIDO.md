# ⚡ Configuración Rápida de Pasarelas de Pago

## 🔴 Problema Actual

Estás viendo el mensaje: **"Las pasarelas de pago no están configuradas"**

Esto significa que no hay credenciales de ninguna pasarela configuradas en tu archivo `.env`.

---

## ✅ Solución Rápida

### Paso 1: Editar el archivo .env

Abre el archivo `.env` que está en la raíz del proyecto y agrega las credenciales.

### Paso 2: Configurar Mercado Pago (Recomendado para demo)

Agrega estas líneas al final de tu archivo `.env`:

```env
# Mercado Pago - Credenciales de TEST
MERCADOPAGO_ACCESS_TOKEN=TEST-tu_access_token_aqui
MERCADOPAGO_PUBLIC_KEY=TEST-tu_public_key_aqui
```

**¿Dónde obtener las credenciales?**

1. Ve a: https://www.mercadopago.com.mx/developers
2. Inicia sesión o crea una cuenta
3. Ve a **"Tus integraciones"** → **"Crear nueva aplicación"**
4. Después de crear, ve a **"Credenciales de prueba"**
5. Copia el **Access Token** (empieza con `TEST-`)
6. Copia la **Public Key** (empieza con `TEST-`)

### Paso 3: Configurar PayPal (Opcional)

Agrega estas líneas al archivo `.env`:

```env
# PayPal - Credenciales de SANDBOX
PAYPAL_CLIENT_ID=tu_client_id_aqui
PAYPAL_SECRET=tu_secret_aqui
PAYPAL_MODE=sandbox
```

**¿Dónde obtener las credenciales?**

1. Ve a: https://developer.paypal.com/
2. Inicia sesión o crea una cuenta
3. Ve a **"Dashboard"** → **"My Apps & Credentials"**
4. Haz clic en **"Create App"**
5. Selecciona **"Sandbox"** como environment
6. Copia el **Client ID** y el **Secret**

---

## 📝 Ejemplo Completo de .env

Tu archivo `.env` debería verse así (con tus credenciales reales):

```env
# ... otras configuraciones existentes ...

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=TEST-1234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk
MERCADOPAGO_PUBLIC_KEY=TEST-abcdefghijk-01234567890-abcdefghijk

# PayPal
PAYPAL_CLIENT_ID=AeA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0
PAYPAL_SECRET=EF1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1
PAYPAL_MODE=sandbox

# URL del sitio (importante)
SITE_URL=http://localhost:8000
```

⚠️ **IMPORTANTE**: Reemplaza los valores de ejemplo con tus credenciales reales.

---

## ✅ Verificar Configuración

Después de agregar las credenciales, ejecuta:

```bash
python3 verificar_configuracion_pagos.py
```

Deberías ver:
```
✅ MERCADOPAGO_ACCESS_TOKEN: Configurado
✅ PAYPAL_CLIENT_ID y PAYPAL_SECRET: Configurados
```

---

## 🔄 Reiniciar el Servidor

**MUY IMPORTANTE**: Después de modificar el `.env`, debes reiniciar el servidor Django:

1. Si está corriendo, deténlo (Ctrl+C)
2. Inicia el servidor de nuevo:
   ```bash
   python manage.py runserver
   ```

---

## 🧪 Probar

1. Ve al portal del cliente: http://localhost:8000/clientes/portal/mis-pagos/
2. Haz clic en un pago pendiente o vencido
3. Ahora deberías ver el botón **"Pagar en Línea"** en lugar del mensaje de error

---

## 🆘 Si Aún No Funciona

### Problema: "Sigue apareciendo el mensaje de error"

**Soluciones:**

1. **Verifica que no haya espacios extras**:
   ```env
   # ✅ Correcto
   MERCADOPAGO_ACCESS_TOKEN=TEST-1234...
   
   # ❌ Incorrecto (tiene espacios)
   MERCADOPAGO_ACCESS_TOKEN = TEST-1234...
   ```

2. **Verifica que las líneas no estén comentadas**:
   ```env
   # ✅ Correcto
   MERCADOPAGO_ACCESS_TOKEN=TEST-1234...
   
   # ❌ Incorrecto (está comentado)
   # MERCADOPAGO_ACCESS_TOKEN=TEST-1234...
   ```

3. **Asegúrate de haber reiniciado el servidor**

4. **Verifica que las credenciales sean válidas**:
   - Mercado Pago: Deben empezar con `TEST-` (modo test) o `APP_USR-` (producción)
   - PayPal: Deben ser credenciales válidas del panel de PayPal

5. **Ejecuta la verificación nuevamente**:
   ```bash
   python3 verificar_configuracion_pagos.py
   ```

---

## 📖 Documentación Completa

Para más detalles sobre cómo obtener las credenciales:

- **Mercado Pago**: Ver `GUIA_CONFIGURACION_MERCADOPAGO.md`
- **PayPal**: Ver `GUIA_CONFIGURACION_PAYPAL.md`
- **Demo completo**: Ver `DEMO_PAGOS_MERCADOPAGO_PAYPAL.md`

---

## ✨ Resumen Rápido

1. ✏️ Edita `.env` y agrega las credenciales
2. 💾 Guarda el archivo
3. 🔄 Reinicia el servidor Django
4. ✅ Verifica con `python3 verificar_configuracion_pagos.py`
5. 🧪 Prueba en el portal del cliente

¡Listo! 🎉


