# 💳 Guía: Tarjetas de Prueba de Mercado Pago

Esta guía te mostrará cómo realizar pagos de prueba con Mercado Pago usando tarjetas de prueba.

---

## 🎯 Requisitos Previos

1. ✅ Mercado Pago configurado en tu `.env` con credenciales de **sandbox/test**
2. ✅ Servidor Django corriendo
3. ✅ Acceso al portal de cliente para realizar pagos

---

## 💳 Tarjetas de Prueba Disponibles

Mercado Pago proporciona tarjetas de prueba según el resultado que quieras simular:

### ✅ **Pago Aprobado**

| Tipo | Número de Tarjeta | CVV | Fecha de Vencimiento | Nombre | Documento | Nota |
|------|-------------------|-----|---------------------|--------|-----------|------|
| Visa Crédito | `4509 9535 6623 3704` | `123` | `11/25` (cualquier fecha futura) | `APRO` | `12345678` | ⭐ Más usada |
| Mastercard Crédito | `5031 7557 3453 0604` | `123` | `11/25` | `APRO` | `12345678` | |
| American Express Crédito | `3711 803032 57522` | `1234` | `11/25` | `APRO` | `12345678` | CVV de 4 dígitos |

### ⏳ **Pago Pendiente**

| Tipo | Número de Tarjeta | CVV | Resultado |
|------|-------------------|-----|-----------|
| Visa | `4013 5406 8274 6260` | `123` | Pendiente de revisión |
| Mastercard | `5031 4332 1540 6351` | `123` | Pendiente de revisión |

### ❌ **Pago Rechazado**

| Tipo | Número de Tarjeta | CVV | Motivo de Rechazo |
|------|-------------------|-----|-------------------|
| Visa | `4014 7003 1562 8291` | `123` | Fondos insuficientes |
| Mastercard | `5031 8789 9990 5883` | `123` | Tarjeta rechazada |
| Visa | `4013 5406 8274 6260` | `123` | Tarjeta vencida (usar fecha pasada) |

### 🔄 **Pago en Proceso**

| Tipo | Número de Tarjeta | CVV | Resultado |
|------|-------------------|-----|-----------|
| Visa | `4509 9535 6623 3704` | `123` | Procesando |

---

## 📝 Paso a Paso: Realizar un Pago de Prueba

### Paso 1: Acceder al Portal del Cliente

1. Inicia sesión en el portal del cliente:
   ```
   http://localhost:8000/clientes/portal/
   ```

2. Navega a **"Mis Pagos"** en el menú lateral

3. Selecciona un pago pendiente haciendo clic en él

### Paso 2: Seleccionar Mercado Pago

1. Haz clic en el botón **"Pagar en Línea"** o **"Pagar con Mercado Pago"**

2. En la página de selección de pasarela, elige **"Mercado Pago"**

3. Haz clic en **"Continuar con el pago"**

### Paso 3: Serás Redirigido a Mercado Pago

Serás redirigido a la página de pago de Mercado Pago (sandbox).

**URLs esperadas:**
- Sandbox: `https://sandbox.mercadopago.com.mx/checkout/v1/redirect?pref_id=...`
- O: `https://www.mercadopago.com.mx/checkout/v1/redirect?pref_id=...`

### Paso 4: Ingresar Datos de la Tarjeta de Prueba

#### Para Pago Aprobado:

```
Número de Tarjeta: 4509 9535 6623 3704
Tipo: Crédito (Visa) ← Selecciona "Crédito" en Mercado Pago
Nombre en la Tarjeta: APRO
Fecha de Vencimiento: 11/25 (o cualquier fecha futura)
CVV: 123
Tipo de Documento: DNI / CURP / RFC
Número de Documento: 12345678
Email: (cualquier email válido, ej: test@example.com)
```

**Nota importante:** 
- Esta tarjeta (`4509 9535 6623 3704`) es una **tarjeta de CRÉDITO Visa**
- En Mercado Pago, selecciona **"Crédito"** cuando te pregunte el tipo
- Funciona tanto si seleccionas "Crédito" como "Débito", pero está diseñada como crédito

#### Para Pago Rechazado:

```
Número de Tarjeta: 4014 7003 1562 8291
Nombre en la Tarjeta: OTHE
Fecha de Vencimiento: 11/25
CVV: 123
Tipo de Documento: DNI
Número de Documento: 12345678
Email: test@example.com
```

### Paso 5: Confirmar el Pago

1. Revisa los datos ingresados
2. Haz clic en **"Pagar"** o **"Confirmar"**
3. Mercado Pago procesará el pago

### Paso 6: Verificar el Resultado

#### Si el Pago fue Aprobado:

- Serás redirigido a la página de éxito: `/pagos/{id}/pago-exitoso/`
- Verás un mensaje: "¡Pago procesado exitosamente!"
- El estado del pago cambiará a "Pagado" en el sistema

#### Si el Pago fue Rechazado:

- Serás redirigido a la página de cancelación: `/pagos/{id}/pago-cancelado/`
- Verás un mensaje informativo sobre el rechazo
- El estado del pago permanecerá como "Pendiente"

---

## 🔍 Verificar el Pago en el Sistema

### Desde el Portal del Cliente:

1. Ve a **"Mis Pagos"**
2. Busca el pago que acabas de procesar
3. Verifica el estado (debería ser "Pagado" si fue aprobado)

### Desde el Panel de Administración:

1. Accede a `/admin/pagos/pago/`
2. Busca el pago por cliente o ID
3. Verifica:
   - **Estado**: Debería cambiar a "Pagado"
   - **Fecha de pago**: Debería estar registrada
   - **Transacciones**: Deberías ver una transacción con estado "completada"

### Ver Transacciones de Pago:

1. En el detalle del pago, busca la sección **"Transacciones"**
2. Verifica que aparezca una transacción con:
   - **Pasarela**: Mercado Pago
   - **Estado**: Completada
   - **ID de Transacción**: El `payment_id` de Mercado Pago

---

## 📊 Tabla de Tarjetas por Caso de Uso

### Casos Comunes de Prueba:

| Caso | Tarjeta | CVV | Resultado Esperado |
|------|---------|-----|-------------------|
| Pago exitoso rápido | `4509 9535 6623 3704` | `123` | ✅ Aprobado inmediatamente |
| Fondos insuficientes | `4014 7003 1562 8291` | `123` | ❌ Rechazado |
| Tarjeta inválida | `4013 5406 8274 6260` | `123` | ❌ Rechazado |
| Pago pendiente | `4013 5406 8274 6260` | `123` | ⏳ Pendiente de revisión |

---

## 🛠️ Verificar que Mercado Pago Está en Modo Sandbox

### En tu Código:

Los logs del servidor deberían mostrar URLs que contengan `sandbox`:

```
Creando preferencia de Mercado Pago para pago 4
URLs de retorno validadas: success=http://localhost:8000/pagos/4/pago-exitoso/, ...
```

### En la URL de Redirección:

Cuando te redirija a Mercado Pago, la URL debería contener:
- `sandbox.mercadopago.com.mx` (modo sandbox/test)

**Si ves `www.mercadopago.com.mx` sin "sandbox":**
- Estás usando credenciales de producción (⚠️ cuidado)
- Las tarjetas de prueba NO funcionarán

---

## ⚙️ Configuración en .env

Asegúrate de tener configurado:

```env
# Mercado Pago - CREDENCIALES DE SANDBOX/TEST
MERCADOPAGO_ACCESS_TOKEN=TEST-tu_access_token_aqui
MERCADOPAGO_PUBLIC_KEY=TEST-tu_public_key_aqui

# URL del sitio (para webhooks y redirects)
SITE_URL=http://localhost:8000
```

**Importante:** Los tokens de prueba deben empezar con `TEST-`

---

## 🔐 Obtener Credenciales de Sandbox

Si no tienes credenciales de sandbox:

1. Ve a: https://www.mercadopago.com.mx/developers/panel/app
2. Inicia sesión con tu cuenta de Mercado Pago
3. Selecciona o crea una aplicación
4. Ve a la sección **"Credenciales de prueba"**
5. Copia:
   - **Access Token** (debe empezar con `TEST-`)
   - **Public Key** (debe empezar con `TEST-`)

---

## ❓ Preguntas Frecuentes

### ¿Las tarjetas de prueba funcionan en producción?

**NO**. Las tarjetas de prueba solo funcionan con credenciales de sandbox (`TEST-...`).

### ¿Puedo usar cualquier nombre en la tarjeta?

Sí, puedes usar cualquier nombre. Sin embargo, Mercado Pago recomienda usar:
- `APRO` para pagos aprobados
- `OTHE` para otros casos

### ¿El CVV importa?

Para las tarjetas de prueba, el CVV debe ser:
- `123` para Visa y Mastercard
- `1234` para American Express

### ¿Qué pasa si uso una fecha de vencimiento pasada?

Algunas tarjetas de prueba simulan errores de tarjeta vencida, pero para la mayoría, cualquier fecha futura funciona.

### ¿Los pagos de prueba se procesan realmente?

**NO**. Los pagos de prueba son simulados. No se realiza ningún cargo real.

### ¿Puedo probar reembolsos?

Sí, una vez que un pago de prueba está aprobado, puedes probar reembolsos desde el panel de administración.

---

## 🐛 Solución de Problemas

### Error: "Tarjeta inválida"

- Verifica que estés usando credenciales de **sandbox** (que empiecen con `TEST-`)
- Asegúrate de usar una de las tarjetas de prueba listadas arriba
- Verifica que el CVV sea correcto (`123` o `1234`)

### Error: "No se puede procesar el pago"

- Verifica que `MERCADOPAGO_ACCESS_TOKEN` esté configurado en `.env`
- Reinicia el servidor Django después de cambiar `.env`
- Revisa los logs del servidor para ver el error específico

### La página de Mercado Pago no carga

- Verifica que tu conexión a internet funcione
- Verifica que las credenciales sean correctas
- Revisa los logs del servidor para errores de API

---

## 📚 Recursos Adicionales

- [Documentación oficial de Mercado Pago](https://www.mercadopago.com.mx/developers/es/docs)
- [Tarjetas de prueba de Mercado Pago](https://www.mercadopago.com.mx/developers/es/docs/checkout-pro/testing)
- [Simulador de casos de pago](https://www.mercadopago.com.mx/developers/es/docs/checkout-pro/testing/test-cards)

---

**¡Listo para probar!** 💳✨

Usa las tarjetas de prueba listadas arriba y verifica que todo funcione correctamente.

