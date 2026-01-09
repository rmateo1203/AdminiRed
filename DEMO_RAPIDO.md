# ⚡ Demo Rápido: Mercado Pago y PayPal

Guía de referencia rápida para configurar y probar el demo.

## 🚀 Setup Rápido (5 minutos)

### 1. Instalar dependencias

```bash
pip install mercadopago>=2.2.0
```

### 2. Configurar .env

```env
SITE_URL=http://localhost:8000
MERCADOPAGO_ACCESS_TOKEN=TEST-tu_token_aqui
MERCADOPAGO_PUBLIC_KEY=TEST-tu_key_aqui
PAYPAL_CLIENT_ID=tu_client_id_aqui
PAYPAL_SECRET=tu_secret_aqui
PAYPAL_MODE=sandbox
```

### 3. Verificar configuración

```bash
python verificar_mercadopago.py
python verificar_paypal.py
```

### 4. Crear datos de prueba

```bash
python crear_datos_demo.py
```

### 5. Iniciar servidor

```bash
python manage.py runserver
```

### 6. Probar

Accede a: http://localhost:8000/pagos/{pago_id}/procesar-online/

---

## 📋 Obtener Credenciales

**📖 Guía completa paso a paso:** Ver `OBTENER_CREDENCIALES_PASO_A_PASO.md`

### Mercado Pago (Test) - Resumen
1. Ve a: https://www.mercadopago.com.mx/developers
2. Inicia sesión o crea cuenta
3. Ve a "Tus integraciones" → "Crear nueva aplicación"
4. Haz clic en "Credenciales de prueba"
5. Copia **Access Token** (TEST-...) y **Public Key** (TEST-...)

### PayPal (Sandbox) - Resumen
1. Ve a: https://developer.paypal.com/
2. Inicia sesión o crea cuenta
3. Dashboard → "My Apps & Credentials" → "Create App"
4. Selecciona **"Sandbox"** como environment
5. Copia **Client ID** y **Secret** (haz clic en "Show" para ver el Secret)

---

## 🧪 Tarjetas de Prueba

### Mercado Pago

**✅ Aprobada:**
- Visa: `4509 9535 6623 3704`
- CVV: `123`
- Nombre: `APRO`

**❌ Rechazada:**
- Mastercard: `5031 7557 3453 0604`
- CVV: `123`
- Nombre: `OTHE`

### PayPal

**✅ Visa:**
- `4111111111111111`
- CVV: `123`
- Fecha futura cualquiera

**✅ Mastercard:**
- `5555555555554444`
- CVV: `123`
- Fecha futura cualquiera

---

## 🔗 URLs Útiles

- Admin: http://localhost:8000/admin/
- Portal Cliente: http://localhost:8000/clientes/portal/
- Lista Pagos: http://localhost:8000/pagos/
- Verificación MP: `python verificar_mercadopago.py`
- Verificación PayPal: `python verificar_paypal.py`
- Crear datos: `python crear_datos_demo.py`

---

## 📖 Documentación Completa

Ver `DEMO_PAGOS_MERCADOPAGO_PAYPAL.md` para detalles completos.

---

**¡Listo para el demo!** 🎉

