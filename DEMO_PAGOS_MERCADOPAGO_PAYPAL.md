# 🎬 Demo: Mercado Pago y PayPal

Guía práctica para configurar y probar pagos en línea con Mercado Pago y PayPal.

## 📋 Índice

1. [Configuración Inicial](#configuración-inicial)
2. [Configurar Mercado Pago (Test)](#configurar-mercado-pago-test)
3. [Configurar PayPal (Sandbox)](#configurar-paypal-sandbox)
4. [Verificar Configuración](#verificar-configuración)
5. [Crear Datos de Prueba](#crear-datos-de-prueba)
6. [Probar Flujo de Pago](#probar-flujo-de-pago)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Configuración Inicial

### Paso 1: Instalar Dependencias

```bash
# Instalar SDK de Mercado Pago
pip install mercadopago>=2.2.0

# Requests ya debería estar instalado (para PayPal)
pip install requests>=2.31.0
```

O agregar a `requirements.txt`:
```
mercadopago>=2.2.0
requests>=2.31.0
```

### Paso 2: Configurar Variables de Entorno

Edita tu archivo `.env` (en la raíz del proyecto):

```env
# URL del sitio (importante para las URLs de retorno)
SITE_URL=http://localhost:8000

# Mercado Pago - Credenciales de TEST
MERCADOPAGO_ACCESS_TOKEN=TEST-tu_access_token_aqui
MERCADOPAGO_PUBLIC_KEY=TEST-tu_public_key_aqui

# PayPal - Credenciales de SANDBOX
PAYPAL_CLIENT_ID=tu_client_id_aqui
PAYPAL_SECRET=tu_secret_aqui
PAYPAL_MODE=sandbox
```

---

## 🔵 Configurar Mercado Pago (Test)

### Paso 1: Crear Cuenta de Desarrollador

1. Ve a: https://www.mercadopago.com.mx/developers
2. Crea una cuenta o inicia sesión
3. Ve a **"Tus integraciones"** → **"Crear nueva aplicación"**
4. Completa:
   - **Nombre**: AdminiRed Demo
   - **Plataforma**: Web
   - **Categoría**: Selecciona la apropiada

### Paso 2: Obtener Credenciales de Test

1. En el panel de tu aplicación, ve a **"Credenciales de prueba"**
2. Copia:
   - **Access Token de prueba**: `TEST-...`
   - **Public Key de prueba**: `TEST-...`
3. Agrega estas credenciales a tu `.env`:

```env
MERCADOPAGO_ACCESS_TOKEN=TEST-1234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk
MERCADOPAGO_PUBLIC_KEY=TEST-abcdefghijk-01234567890-abcdefghijk
```

### Paso 3: Usuarios de Prueba

Mercado Pago proporciona usuarios de prueba automáticamente. Puedes crear usuarios de prueba en:
- Panel → **"Tus integraciones"** → **"Usuarios de prueba"**

---

## 🟠 Configurar PayPal (Sandbox)

### Paso 1: Crear Cuenta de Desarrollador

1. Ve a: https://developer.paypal.com/
2. Crea una cuenta o inicia sesión
3. Ve a **"Dashboard"** → **"My Apps & Credentials"**

### Paso 2: Crear Aplicación Sandbox

1. Haz clic en **"Create App"**
2. Completa:
   - **App Name**: AdminiRed Demo
   - **Merchant**: Tu cuenta
   - **Environment**: **Sandbox** (importante para pruebas)
3. Copia las credenciales:
   - **Client ID**: `Ae...`
   - **Secret**: Haz clic en "Show" y copia

### Paso 3: Configurar en .env

```env
PAYPAL_CLIENT_ID=AeA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0
PAYPAL_SECRET=EF1G2H3I4J5K6L7M8N9O0P1Q2R3S4T5U6V7W8X9Y0Z1
PAYPAL_MODE=sandbox
```

### Paso 4: Crear Cuentas de Prueba

1. En el Dashboard, ve a **"Sandbox"** → **"Accounts"**
2. Haz clic en **"Create Account"**
3. Crea dos cuentas:
   - **Personal** (para simular comprador)
   - **Business** (para tu negocio)

---

## ✅ Verificar Configuración

### Verificar Mercado Pago

```bash
python verificar_mercadopago.py
```

Deberías ver:
```
✅ Configuración básica: COMPLETA
```

### Verificar PayPal

```bash
python verificar_paypal.py
```

Deberías ver:
```
✅ Configuración básica: COMPLETA
✅ Conexión exitosa con PayPal API
```

---

## 📝 Crear Datos de Prueba

### Opción 1: Desde el Admin de Django

1. Inicia el servidor:
   ```bash
   python manage.py runserver
   ```

2. Accede al admin: http://localhost:8000/admin/

3. Crea los datos necesarios:
   - **Cliente**: Crear un cliente de prueba
   - **Instalación** (opcional): Crear una instalación para el cliente
   - **Pago**: Crear un pago pendiente con:
     - Cliente: El cliente creado
     - Monto: $100.00 (o cualquier monto)
     - Estado: Pendiente
     - Fecha de vencimiento: Fecha futura

### Opción 2: Desde el Shell de Django

```bash
python manage.py shell
```

```python
from clientes.models import Cliente
from pagos.models import Pago
from datetime import date, timedelta
from decimal import Decimal

# Crear cliente de prueba
cliente, created = Cliente.objects.get_or_create(
    nombre="Juan",
    apellido1="Pérez",
    apellido2="Demo",
    telefono="1234567890",
    email="juan.perez.demo@example.com",
    defaults={
        'estado_cliente': 'activo'
    }
)

print(f"Cliente: {cliente.nombre_completo} ({'Creado' if created else 'Ya existía'})")

# Crear pago de prueba
pago, created = Pago.objects.get_or_create(
    cliente=cliente,
    concepto="Pago mensual - Demo",
    periodo_mes=date.today().month,
    periodo_anio=date.today().year,
    defaults={
        'monto': Decimal('100.00'),
        'fecha_vencimiento': date.today() + timedelta(days=7),
        'estado': 'pendiente'
    }
)

print(f"Pago: ${pago.monto} - Estado: {pago.get_estado_display()} ({'Creado' if created else 'Ya existía'})")
print(f"ID del pago: {pago.id}")
print(f"URL del detalle: http://localhost:8000/pagos/{pago.id}/")
```

---

## 🧪 Probar Flujo de Pago

### Prueba 1: Mercado Pago

#### Paso 1: Acceder al Pago (Portal del Cliente)

**Opción A: Desde el Portal del Cliente**
1. Inicia sesión como cliente en: http://localhost:8000/clientes/portal/login/
2. Ve a "Mis Pagos": http://localhost:8000/clientes/portal/mis-pagos/
3. Haz clic en el botón **"Pagar"** o **"Ver"** del pago que quieres pagar
4. Esto te llevará al detalle del pago: `/clientes/portal/mis-pagos/{pago_id}/`

**Opción B: Acceso Directo**
1. Abre directamente: http://localhost:8000/clientes/portal/mis-pagos/{pago_id}/
   (Reemplaza `{pago_id}` con el ID del pago creado)

**En el Detalle del Pago deberías ver:**
   - Información completa del pago (monto, concepto, estado, fechas)
   - Si el pago está **pendiente** o **vencido**, aparecerá el botón **"Pagar en Línea"**

#### Paso 2: Iniciar Pago

1. En la página de detalle del pago, haz clic en el botón **"Pagar en Línea"**
   - Este botón solo aparece si el pago está **pendiente** o **vencido**
   - El botón te redirigirá a: `/pagos/{pago_id}/pagar-online/`

2. En la página de selección de pasarela:
   - Verás las opciones disponibles (Mercado Pago, PayPal, etc.)
   - Selecciona **"Mercado Pago"**
   - Haz clic en **"Continuar con el Pago"**

#### Paso 3: Probar en Mercado Pago

Serás redirigido a Mercado Pago. Usa estas tarjetas de prueba:

**✅ Tarjeta Aprobada (Visa):**
- Número: `4509 9535 6623 3704`
- CVV: `123`
- Fecha: Cualquier fecha futura (ej: 12/25)
- Nombre: `APRO`

**❌ Tarjeta Rechazada (Mastercard):**
- Número: `5031 7557 3453 0604`
- CVV: `123`
- Fecha: Cualquier fecha futura
- Nombre: `OTHE`

#### Paso 4: Verificar Resultado

Después de aprobar el pago:
- Serás redirigido a: `/pagos/{pago_id}/pago-exitoso/`
- Deberías ver: "¡Pago procesado exitosamente!"
- El pago estará marcado como "Pagado"

---

### Prueba 2: PayPal

#### Paso 1: Acceder al Pago

1. Crea otro pago de prueba (o usa el mismo)
2. Accede a: http://localhost:8000/pagos/{pago_id}/

#### Paso 2: Iniciar Pago

1. Haz clic en **"Pagar en Línea"**
2. Selecciona **"PayPal"**
3. Haz clic en **"Continuar con el Pago"**

#### Paso 3: Probar en PayPal Sandbox

Serás redirigido a `sandbox.paypal.com`. 

**Opciones de prueba:**

**Opción A: Usar cuenta de prueba**
1. Inicia sesión con una cuenta Sandbox que creaste
2. Aprobar el pago
3. Completar el flujo

**Opción B: Pagar como invitado**
1. Selecciona "Pagar como invitado"
2. Usa tarjetas de prueba:
   - **Visa**: `4111111111111111`
   - **Mastercard**: `5555555555554444`
   - CVV: `123`
   - Fecha: Cualquier fecha futura
   - Cualquier código postal

#### Paso 4: Verificar Resultado

- Serás redirigido a: `/pagos/{pago_id}/pago-exitoso/`
- Deberías ver: "¡Pago procesado exitosamente!"
- El pago estará marcado como "Pagado"

---

## 🔍 Verificar Transacciones

### Desde el Admin

1. Ve a: http://localhost:8000/admin/pagos/transaccionpago/
2. Deberías ver las transacciones creadas con:
   - Pasarela usada (Mercado Pago o PayPal)
   - Estado (completada)
   - ID de transacción
   - Datos de respuesta

### Desde el Shell

```bash
python manage.py shell
```

```python
from pagos.models import TransaccionPago

# Ver todas las transacciones
transacciones = TransaccionPago.objects.all().order_by('-fecha_creacion')[:10]

for t in transacciones:
    print(f"Pago: ${t.pago.monto} - Pasarela: {t.pasarela} - Estado: {t.estado}")
    print(f"  ID Transacción: {t.id_transaccion_pasarela}")
    print(f"  Fecha: {t.fecha_creacion}")
    print()
```

---

## 🐛 Troubleshooting

### Problema: "No se pudo crear la preferencia de Mercado Pago"

**Causas posibles:**
1. Access Token incorrecto o inválido
2. Monto inválido (debe ser > 0)
3. URL de retorno inválida

**Solución:**
```bash
# Verificar credenciales
python verificar_mercadopago.py

# Verificar que SITE_URL esté configurado
python manage.py shell -c "from django.conf import settings; print('SITE_URL:', settings.SITE_URL)"
```

### Problema: "No se pudo obtener el access token de PayPal"

**Causas posibles:**
1. Client ID o Secret incorrectos
2. Credenciales de producción en modo sandbox (o viceversa)

**Solución:**
```bash
# Verificar credenciales
python verificar_paypal.py

# Verificar que PAYPAL_MODE sea 'sandbox'
python manage.py shell -c "from django.conf import settings; print('PAYPAL_MODE:', settings.PAYPAL_MODE)"
```

### Problema: El pago no se marca como "Pagado" automáticamente

**Causa:** Los webhooks no están configurados (normal en desarrollo local)

**Solución:**
1. El sistema verifica el pago cuando el usuario regresa de la pasarela
2. Si no funciona, verifica manualmente en el admin
3. Para producción, configura los webhooks:
   - Mercado Pago: URL del webhook en el panel
   - PayPal: Configurar webhooks en el dashboard

### Problema: "Transacción no encontrada"

**Causa:** El ID de retorno no coincide con la transacción guardada

**Solución:**
- Normalmente se resuelve automáticamente
- Si persiste, revisa los logs:
  ```bash
  tail -f logs/django.log  # o donde estén tus logs
  ```

---

## 📊 Checklist de Demo

Antes de presentar el demo, verifica:

- [ ] Mercado Pago configurado y verificado
- [ ] PayPal configurado y verificado
- [ ] Al menos un pago de prueba creado
- [ ] Probar flujo completo de Mercado Pago
- [ ] Probar flujo completo de PayPal
- [ ] Verificar que las transacciones se guardan correctamente
- [ ] Verificar que los pagos se marcan como "Pagados"

---

## 🎯 Próximos Pasos

Después de probar el demo:

1. **Para Producción:**
   - Cambiar credenciales a producción
   - Cambiar `PAYPAL_MODE` a `live`
   - Configurar webhooks
   - Probar con montos pequeños primero

2. **Mejoras Opcionales:**
   - Agregar más métodos de pago
   - Mejorar la UI del proceso de pago
   - Agregar notificaciones por email
   - Implementar reembolsos automáticos

---

## 📞 Recursos Adicionales

- **Mercado Pago:**
  - Docs: https://www.mercadopago.com.mx/developers/es/docs
  - Tarjetas de prueba: https://www.mercadopago.com.mx/developers/es/docs/checkout-pro/test-cards

- **PayPal:**
  - Docs: https://developer.paypal.com/docs/
  - Sandbox Testing: https://developer.paypal.com/docs/api-basics/sandbox/

---

**¡Demo listo!** 🎉

Ahora puedes probar y presentar los pagos en línea con Mercado Pago y PayPal.

