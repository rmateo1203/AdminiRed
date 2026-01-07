# 🔧 Guía Completa: Configuración de PayPal y Flujo de Pago

## 📋 Índice
1. [Configuración de Credenciales de PayPal](#configuración-de-credenciales-de-paypal)
2. [Configuración en el Proyecto](#configuración-en-el-proyecto)
3. [Flujo de Pago para Usuarios](#flujo-de-pago-para-usuarios)
4. [Pruebas en Modo Sandbox](#pruebas-en-modo-sandbox)
5. [Pasar a Producción](#pasar-a-producción)
6. [Solución de Problemas](#solución-de-problemas)

---

## 🔑 Configuración de Credenciales de PayPal

### Paso 1: Crear Cuenta de Desarrollador

1. **Ir a PayPal Developer**
   - Visita: https://developer.paypal.com/
   - Haz clic en "Sign Up" o "Log In"

2. **Crear una Aplicación**
   - Una vez dentro, ve a "Dashboard" → "My Apps & Credentials"
   - Haz clic en "Create App"
   - Completa el formulario:
     - **App Name**: AdminiRed (o el nombre que prefieras)
     - **Merchant**: Selecciona tu cuenta de negocio
     - **Environment**: Selecciona "Sandbox" para pruebas

3. **Obtener las Credenciales**
   - Después de crear la app, verás:
     - **Client ID**: `Ae...` (copia este valor)
     - **Secret**: `EF...` (haz clic en "Show" y copia este valor)
   - ⚠️ **IMPORTANTE**: Guarda el Secret de forma segura, solo se muestra una vez

### Paso 2: Configurar Cuenta Sandbox (Para Pruebas)

1. **Crear Cuentas de Prueba**
   - En el Dashboard, ve a "Sandbox" → "Accounts"
   - Haz clic en "Create Account"
   - Crea dos cuentas:
     - **Cuenta Personal** (para simular compradores)
     - **Cuenta Business** (para tu negocio)

2. **Configurar Cuenta Business**
   - Selecciona la cuenta Business
   - Ve a "Profile" → "Funding"
   - Agrega métodos de pago de prueba (tarjetas, saldo, etc.)

---

## ⚙️ Configuración en el Proyecto

### Paso 1: Agregar Variables de Entorno

Edita tu archivo `.env` (en la raíz del proyecto):

```env
# PayPal Configuration
PAYPAL_CLIENT_ID=tu_client_id_aqui
PAYPAL_SECRET=tu_secret_aqui
PAYPAL_MODE=sandbox  # Cambia a 'live' para producción
```

**Ejemplo:**
```env
PAYPAL_CLIENT_ID=AeA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0
PAYPAL_SECRET=EF1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1
PAYPAL_MODE=sandbox
```

### Paso 2: Verificar Configuración en Settings

El archivo `adminired/settings/base.py` ya está configurado para leer estas variables:

```python
# Pasarela de Pago - PayPal
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID', default='')
PAYPAL_SECRET = config('PAYPAL_SECRET', default='')
PAYPAL_MODE = config('PAYPAL_MODE', default='sandbox')  # sandbox o live
```

### Paso 3: Verificar que Funciona

Ejecuta este comando para verificar la configuración:

```bash
python manage.py shell -c "
from django.conf import settings
print('PAYPAL_CLIENT_ID:', '✅ Configurado' if settings.PAYPAL_CLIENT_ID else '❌ NO configurado')
print('PAYPAL_SECRET:', '✅ Configurado' if settings.PAYPAL_SECRET else '❌ NO configurado')
print('PAYPAL_MODE:', settings.PAYPAL_MODE)
"
```

---

## 👥 Flujo de Pago para Usuarios

### Paso a Paso del Proceso

#### 1. **Usuario Accede al Detalle del Pago**

```
Usuario → Pagos → Ver Detalle de Pago
```

El usuario ve:
- Información del pago (monto, concepto, cliente)
- Estado del pago (Pendiente, Vencido, etc.)
- Botón "Pagar en Línea" (si el pago está pendiente)

#### 2. **Usuario Hace Clic en "Pagar en Línea"**

El sistema muestra un formulario con las pasarelas disponibles:
- ✅ Stripe (si está configurado)
- ✅ Mercado Pago (si está configurado)
- ✅ PayPal (si está configurado)

#### 3. **Usuario Selecciona PayPal**

El usuario:
- Selecciona la opción "PayPal"
- Hace clic en "Continuar con el Pago"

#### 4. **Redirección a PayPal**

El sistema:
- Crea una orden de pago en PayPal
- Obtiene la URL de aprobación
- Redirige al usuario a PayPal

**URL de PayPal:**
```
https://www.sandbox.paypal.com/checkoutnow?token=ORDER_ID
```

#### 5. **Usuario Aprueba el Pago en PayPal**

En PayPal, el usuario:
- Ve los detalles del pago (monto, concepto)
- Inicia sesión con su cuenta PayPal (o crea una)
- Selecciona método de pago (PayPal balance, tarjeta, etc.)
- Hace clic en "Pagar Ahora"

#### 6. **PayPal Redirige de Vuelta**

Después de aprobar:
- PayPal redirige al usuario de vuelta a tu sitio
- URL de retorno: `/pagos/{pago_id}/pago-exitoso/?token=ORDER_ID&PayerID=PAYER_ID`

#### 7. **Sistema Procesa el Pago**

El sistema automáticamente:
- Verifica el estado de la orden en PayPal
- Captura el pago (si está aprobado)
- Actualiza la transacción como "completada"
- Marca el pago como "pagado"
- Muestra mensaje de éxito al usuario

#### 8. **Confirmación Final**

El usuario ve:
- ✅ Mensaje: "¡Pago procesado exitosamente!"
- Detalles del pago actualizado
- Estado del pago: "Pagado"
- Información de la transacción

---

## 🧪 Pruebas en Modo Sandbox

### Cuentas de Prueba

PayPal proporciona cuentas de prueba para simular compradores:

1. **Ir a Sandbox Accounts**
   - Dashboard → Sandbox → Accounts
   - Verás cuentas predefinidas o crear nuevas

2. **Usar Cuenta Personal de Prueba**
   - Email: `buyer@personal.example.com` (ejemplo)
   - Contraseña: La que configuraste
   - Puedes usar esta cuenta para "comprar" en modo sandbox

### Probar el Flujo Completo

1. **Crear un Pago de Prueba**
   ```
   - Ir a: /pagos/nuevo/
   - Crear un pago con monto de prueba (ej: $100.00)
   - Guardar el pago
   ```

2. **Iniciar Pago con PayPal**
   ```
   - Ir al detalle del pago
   - Clic en "Pagar en Línea"
   - Seleccionar PayPal
   - Continuar
   ```

3. **Aprobar en PayPal Sandbox**
   ```
   - Serás redirigido a sandbox.paypal.com
   - Inicia sesión con cuenta de prueba
   - Aprobar el pago
   ```

4. **Verificar Resultado**
   ```
   - Serás redirigido de vuelta
   - Verás mensaje de éxito
   - El pago estará marcado como "Pagado"
   ```

### Tarjetas de Prueba

PayPal Sandbox acepta estas tarjetas de prueba:

**Visa:**
- Número: `4111111111111111`
- CVV: `123`
- Fecha: Cualquier fecha futura

**Mastercard:**
- Número: `5555555555554444`
- CVV: `123`
- Fecha: Cualquier fecha futura

---

## 🚀 Pasar a Producción

### Paso 1: Cambiar a Modo Live

1. **Crear Aplicación en Producción**
   - Dashboard → My Apps & Credentials
   - Clic en "Create App"
   - Selecciona "Live" en lugar de "Sandbox"
   - Obtén las credenciales de producción

2. **Actualizar Variables de Entorno**
   ```env
   PAYPAL_CLIENT_ID=tu_client_id_produccion
   PAYPAL_SECRET=tu_secret_produccion
   PAYPAL_MODE=live
   ```

3. **Verificar Configuración**
   - Asegúrate de que `SITE_URL` apunte a tu dominio real
   - Verifica que los webhooks estén configurados

### Paso 2: Configurar Webhooks (Opcional pero Recomendado)

1. **En PayPal Dashboard**
   - Ve a "My Apps & Credentials"
   - Selecciona tu app de producción
   - Ve a "Webhooks"
   - Clic en "Add Webhook"

2. **Configurar URL del Webhook**
   ```
   URL: https://tudominio.com/pagos/webhook/paypal/
   Eventos: payment.capture.completed, payment.capture.denied
   ```

3. **Verificar Webhook**
   - PayPal enviará un evento de prueba
   - Tu servidor debe responder con 200 OK

---

## 🔍 Solución de Problemas

### Error: "No se pudo obtener el access token"

**Causa:** Credenciales incorrectas o no configuradas

**Solución:**
1. Verifica que `PAYPAL_CLIENT_ID` y `PAYPAL_SECRET` estén en `.env`
2. Asegúrate de que no haya espacios extra
3. Verifica que estés usando las credenciales correctas (sandbox vs live)

### Error: "No se encontró la transacción"

**Causa:** El token de PayPal no coincide con la transacción guardada

**Solución:**
- El sistema ahora busca la transacción de forma más flexible
- Si persiste, verifica los logs para ver el token recibido

### El pago no se captura automáticamente

**Causa:** La orden puede estar en estado diferente

**Solución:**
- El sistema ahora verifica el estado antes de capturar
- Si la orden está `COMPLETED`, se actualiza automáticamente
- Si está `APPROVED`, se captura automáticamente

### Redirección incorrecta después del pago

**Causa:** `SITE_URL` no está configurado correctamente

**Solución:**
```env
# En .env
SITE_URL=https://tudominio.com  # Sin barra final
```

---

## 📝 Checklist de Configuración

Antes de usar PayPal en producción, verifica:

- [ ] Cuenta de PayPal Business creada
- [ ] Aplicación creada en PayPal Developer
- [ ] Credenciales (Client ID y Secret) obtenidas
- [ ] Variables agregadas en `.env`
- [ ] `PAYPAL_MODE` configurado (sandbox para pruebas, live para producción)
- [ ] `SITE_URL` configurado correctamente
- [ ] Probar flujo completo en sandbox
- [ ] Webhooks configurados (opcional pero recomendado)
- [ ] Documentación del flujo para usuarios finales

---

## 🎯 Resumen Rápido

### Para Configurar:
1. Crear cuenta en https://developer.paypal.com/
2. Crear aplicación y obtener credenciales
3. Agregar credenciales en `.env`
4. Probar en modo sandbox

### Para los Usuarios:
1. Acceder al detalle del pago
2. Clic en "Pagar en Línea"
3. Seleccionar PayPal
4. Aprobar en PayPal
5. Ver confirmación de pago

---

## 📞 Soporte Adicional

- **Documentación de PayPal**: https://developer.paypal.com/docs/
- **API Reference**: https://developer.paypal.com/docs/api/overview/
- **Sandbox Testing**: https://developer.paypal.com/docs/api-basics/sandbox/

---

**¡Configuración completada!** 🎉

Ahora los usuarios pueden pagar con PayPal de forma segura y sencilla.



