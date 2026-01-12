# 🔧 Guía Completa: Configuración de Mercado Pago

## 📋 Índice
1. [Configuración de Credenciales de Mercado Pago](#configuración-de-credenciales-de-mercado-pago)
2. [Configuración en el Proyecto](#configuración-en-el-proyecto)
3. [Flujo de Pago para Usuarios](#flujo-de-pago-para-usuarios)
4. [Pruebas en Modo Test](#pruebas-en-modo-test)
5. [Pasar a Producción](#pasar-a-producción)
6. [Solución de Problemas](#solución-de-problemas)

---

## 🔑 Configuración de Credenciales de Mercado Pago

### Paso 1: Crear Cuenta de Desarrollador

1. **Ir a Mercado Pago Developers**
   - Visita: https://www.mercadopago.com.mx/developers
   - Haz clic en "Crear cuenta" o "Iniciar sesión"

2. **Crear una Aplicación**
   - Una vez dentro, ve a "Tus integraciones" → "Crear nueva aplicación"
   - Completa el formulario:
     - **Nombre de la aplicación**: AdminiRed (o el nombre que prefieras)
     - **Sitio web**: URL de tu sitio
     - **Categoría**: Selecciona la más apropiada
     - **Plataforma**: Web

3. **Obtener las Credenciales**
   - Después de crear la app, verás:
     - **Access Token**: `APP_USR-...` (copia este valor)
     - **Public Key**: `APP_USR-...` (copia este valor)
   - ⚠️ **IMPORTANTE**: Guarda el Access Token de forma segura

### Paso 2: Configurar Credenciales de Prueba

1. **Credenciales de Test**
   - En el panel, ve a "Credenciales de prueba"
   - Verás:
     - **Access Token de prueba**: `TEST-...`
     - **Public Key de prueba**: `TEST-...`
   - Estas credenciales son para pruebas sin cobrar reales

2. **Usuarios de Prueba**
   - Mercado Pago proporciona usuarios de prueba
   - Puedes crear usuarios de prueba en el panel
   - Estos usuarios pueden "comprar" sin usar dinero real

---

## ⚙️ Configuración en el Proyecto

### Paso 1: Instalar SDK de Mercado Pago

```bash
pip install mercadopago>=2.2.0
```

O agregar a `requirements.txt`:
```
mercadopago>=2.2.0
```

### Paso 2: Agregar Variables de Entorno

Edita tu archivo `.env` (en la raíz del proyecto):

```env
# Mercado Pago Configuration
MERCADOPAGO_ACCESS_TOKEN=tu_access_token_aqui
MERCADOPAGO_PUBLIC_KEY=tu_public_key_aqui
```

**Para pruebas (Test):**
```env
MERCADOPAGO_ACCESS_TOKEN=TEST-tu_access_token_test
MERCADOPAGO_PUBLIC_KEY=TEST-tu_public_key_test
```

**Para producción:**
```env
MERCADOPAGO_ACCESS_TOKEN=APP_USR-tu_access_token_produccion
MERCADOPAGO_PUBLIC_KEY=APP_USR-tu_public_key_produccion
```

### Paso 3: Verificar Configuración en Settings

El archivo `adminired/settings/base.py` ya está configurado para leer estas variables:

```python
# Pasarela de Pago - Mercado Pago
MERCADOPAGO_ACCESS_TOKEN = config('MERCADOPAGO_ACCESS_TOKEN', default='')
MERCADOPAGO_PUBLIC_KEY = config('MERCADOPAGO_PUBLIC_KEY', default='')
```

### Paso 4: Verificar que Funciona

Ejecuta este comando para verificar la configuración:

```bash
python manage.py shell -c "
from django.conf import settings
print('MERCADOPAGO_ACCESS_TOKEN:', '✅ Configurado' if settings.MERCADOPAGO_ACCESS_TOKEN else '❌ NO configurado')
print('MERCADOPAGO_PUBLIC_KEY:', '✅ Configurado' if settings.MERCADOPAGO_PUBLIC_KEY else '❌ NO configurado')
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

#### 3. **Usuario Selecciona Mercado Pago**

El usuario:
- Selecciona la opción "Mercado Pago"
- Hace clic en "Continuar con el Pago"

#### 4. **Redirección a Mercado Pago**

El sistema:
- Crea una preferencia de pago en Mercado Pago
- Obtiene la URL de pago
- Redirige al usuario a Mercado Pago

**URL de Mercado Pago:**
```
https://www.mercadopago.com.mx/checkout/v1/redirect?pref_id=PREFERENCE_ID
```

#### 5. **Usuario Selecciona Método de Pago en Mercado Pago**

En Mercado Pago, el usuario puede elegir:
- 💳 **Tarjeta de crédito/débito**
- 💰 **Efectivo** (OXXO, 7-Eleven, etc.)
- 🏦 **Transferencia bancaria**
- 📱 **Saldo de Mercado Pago**
- Y más opciones según el país

#### 6. **Usuario Completa el Pago**

- Si usa tarjeta: Ingresa datos de la tarjeta
- Si usa efectivo: Obtiene código para pagar en tienda
- Si usa transferencia: Obtiene datos bancarios

#### 7. **Mercado Pago Redirige de Vuelta**

Después de aprobar:
- Mercado Pago redirige al usuario de vuelta a tu sitio
- URL de retorno: `/pagos/{pago_id}/pago-exitoso/?payment_id=PAYMENT_ID`

#### 8. **Sistema Procesa el Pago**

El sistema automáticamente:
- Recibe notificación del webhook (si está configurado)
- Verifica el estado del pago en Mercado Pago
- Actualiza la transacción como "completada"
- Marca el pago como "pagado"
- Muestra mensaje de éxito al usuario

#### 9. **Confirmación Final**

El usuario ve:
- ✅ Mensaje: "¡Pago procesado exitosamente!"
- Detalles del pago actualizado
- Estado del pago: "Pagado"
- Información de la transacción

---

## 🧪 Pruebas en Modo Test

### Credenciales de Prueba

Mercado Pago proporciona credenciales de prueba:

1. **Obtener Credenciales de Test**
   - Panel → "Tus integraciones" → Tu aplicación
   - Ve a "Credenciales de prueba"
   - Copia el Access Token y Public Key de prueba

2. **Usar Credenciales de Test**
   ```env
   MERCADOPAGO_ACCESS_TOKEN=TEST-1234567890-...
   MERCADOPAGO_PUBLIC_KEY=TEST-1234567890-...
   ```

### Tarjetas de Prueba

Mercado Pago acepta estas tarjetas de prueba:

**Visa Aprobada:**
- Número: `4509 9535 6623 3704`
- CVV: `123`
- Fecha: Cualquier fecha futura
- Nombre: APRO

**Mastercard Rechazada:**
- Número: `5031 7557 3453 0604`
- CVV: `123`
- Fecha: Cualquier fecha futura
- Nombre: OTHE

**Visa en Proceso:**
- Número: `4013 5406 8274 6260`
- CVV: `123`
- Fecha: Cualquier fecha futura
- Nombre: CONT

### Probar el Flujo Completo

1. **Crear un Pago de Prueba**
   ```
   - Ir a: /pagos/nuevo/
   - Crear un pago con monto de prueba (ej: $100.00)
   - Guardar el pago
   ```

2. **Iniciar Pago con Mercado Pago**
   ```
   - Ir al detalle del pago
   - Clic en "Pagar en Línea"
   - Seleccionar Mercado Pago
   - Continuar
   ```

3. **Aprobar en Mercado Pago**
   ```
   - Serás redirigido a Mercado Pago
   - Selecciona método de pago (tarjeta de prueba)
   - Usa una tarjeta de prueba
   - Completa el pago
   ```

4. **Verificar Resultado**
   ```
   - Serás redirigido de vuelta
   - Verás mensaje de éxito
   - El pago estará marcado como "Pagado"
   ```

---

## 🚀 Pasar a Producción

### Paso 1: Obtener Credenciales de Producción

1. **En el Panel de Mercado Pago**
   - Ve a "Tus integraciones" → Tu aplicación
   - Ve a "Credenciales de producción"
   - Copia el Access Token y Public Key de producción

2. **Actualizar Variables de Entorno**
   ```env
   MERCADOPAGO_ACCESS_TOKEN=APP_USR-tu_access_token_produccion
   MERCADOPAGO_PUBLIC_KEY=APP_USR-tu_public_key_produccion
   ```

### Paso 2: Configurar Webhooks (Recomendado)

1. **En Mercado Pago Dashboard**
   - Ve a "Tus integraciones" → Tu aplicación
   - Ve a "Webhooks"
   - Clic en "Configurar webhooks"

2. **Configurar URL del Webhook**
   ```
   URL: https://tudominio.com/pagos/webhook/mercadopago/
   Eventos: payment, payment.created, payment.updated
   ```

3. **Verificar Webhook**
   - Mercado Pago enviará un evento de prueba
   - Tu servidor debe responder con 200 OK

### Paso 3: Verificar Configuración

- Asegúrate de que `SITE_URL` apunte a tu dominio real
- Verifica que los webhooks estén configurados
- Prueba un pago real con monto pequeño

---

## 🔍 Solución de Problemas

### Error: "mercadopago no está instalado"

**Causa:** El SDK de Mercado Pago no está instalado

**Solución:**
```bash
pip install mercadopago>=2.2.0
```

### Error: "MERCADOPAGO_ACCESS_TOKEN no configurada"

**Causa:** Credenciales no configuradas o incorrectas

**Solución:**
1. Verifica que `MERCADOPAGO_ACCESS_TOKEN` esté en `.env`
2. Asegúrate de que no haya espacios extra
3. Verifica que estés usando las credenciales correctas (test vs producción)

### Error: "No se pudo crear la preferencia"

**Causa:** Datos inválidos en la preferencia o credenciales incorrectas

**Solución:**
- Verifica que el monto sea válido (mayor a 0)
- Verifica que las URLs de retorno sean válidas
- Revisa los logs para ver el error específico

### El pago no se actualiza automáticamente

**Causa:** Webhook no configurado o no funcionando

**Solución:**
1. Verifica que el webhook esté configurado en Mercado Pago
2. Verifica que la URL del webhook sea accesible
3. Revisa los logs del servidor para ver si llegan los webhooks

### Redirección incorrecta después del pago

**Causa:** `SITE_URL` no está configurado correctamente

**Solución:**
```env
# En .env
SITE_URL=https://tudominio.com  # Sin barra final
```

---

## 📝 Checklist de Configuración

Antes de usar Mercado Pago en producción, verifica:

- [ ] Cuenta de Mercado Pago creada
- [ ] Aplicación creada en Mercado Pago Developers
- [ ] Credenciales (Access Token y Public Key) obtenidas
- [ ] SDK de Mercado Pago instalado (`pip install mercadopago`)
- [ ] Variables agregadas en `.env`
- [ ] Probar flujo completo en modo test
- [ ] Webhooks configurados (opcional pero recomendado)
- [ ] `SITE_URL` configurado correctamente
- [ ] Documentación del flujo para usuarios finales

---

## 🎯 Resumen Rápido

### Para Configurar:
1. Crear cuenta en https://www.mercadopago.com.mx/developers
2. Crear aplicación y obtener credenciales
3. Instalar SDK: `pip install mercadopago`
4. Agregar credenciales en `.env`
5. Probar en modo test

### Para los Usuarios:
1. Acceder al detalle del pago
2. Clic en "Pagar en Línea"
3. Seleccionar Mercado Pago
4. Elegir método de pago en Mercado Pago
5. Completar el pago
6. Ver confirmación de pago

---

## 📞 Soporte Adicional

- **Documentación de Mercado Pago**: https://www.mercadopago.com.mx/developers/es/docs
- **API Reference**: https://www.mercadopago.com.mx/developers/es/reference
- **SDK Python**: https://github.com/mercadopago/sdk-python

---

## 💡 Ventajas de Mercado Pago

- ✅ **Múltiples métodos de pago**: Tarjetas, efectivo, transferencias
- ✅ **Aceptado en Latinoamérica**: Amplia cobertura regional
- ✅ **Pagos en efectivo**: OXXO, 7-Eleven, y más
- ✅ **Webhooks confiables**: Notificaciones automáticas
- ✅ **SDK oficial**: Fácil integración

---

**¡Configuración completada!** 🎉

Ahora los usuarios pueden pagar con Mercado Pago usando múltiples métodos de pago.






