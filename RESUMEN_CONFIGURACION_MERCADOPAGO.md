# 🚀 Resumen Rápido: Configuración de Mercado Pago

## ⚡ Configuración en 4 Pasos

### 1️⃣ Instalar SDK

```bash
pip install mercadopago>=2.2.0
```

### 2️⃣ Obtener Credenciales de Mercado Pago

1. Ve a: https://www.mercadopago.com.mx/developers
2. Inicia sesión o crea cuenta
3. "Tus integraciones" → "Crear nueva aplicación"
4. Copia el **Access Token** y **Public Key**

### 3️⃣ Agregar al Proyecto

Edita el archivo `.env` en la raíz del proyecto:

```env
MERCADOPAGO_ACCESS_TOKEN=tu_access_token_aqui
MERCADOPAGO_PUBLIC_KEY=tu_public_key_aqui
SITE_URL=http://localhost:8000
```

**Para pruebas (Test):**
```env
MERCADOPAGO_ACCESS_TOKEN=TEST-tu_access_token_test
MERCADOPAGO_PUBLIC_KEY=TEST-tu_public_key_test
```

### 4️⃣ Verificar Configuración

Ejecuta:

```bash
python verificar_mercadopago.py
```

O:

```bash
python manage.py shell -c "
from django.conf import settings
print('Access Token:', '✅' if settings.MERCADOPAGO_ACCESS_TOKEN else '❌')
print('Public Key:', '✅' if settings.MERCADOPAGO_PUBLIC_KEY else '❌')
"
```

---

## 👥 Cómo Pagan los Usuarios

### Flujo Simple:

1. **Usuario** → Ve al detalle del pago
2. **Clic** en "Pagar en Línea"
3. **Selecciona** Mercado Pago
4. **Redirige** a Mercado Pago
5. **Elige** método de pago (tarjeta, efectivo, etc.)
6. **Completa** el pago
7. **Regresa** automáticamente
8. **✅ Pago completado**

### Métodos de Pago Disponibles:

- 💳 **Tarjetas de crédito/débito**
- 💰 **Efectivo** (OXXO, 7-Eleven, etc.)
- 🏦 **Transferencia bancaria**
- 📱 **Saldo de Mercado Pago**

---

## 🧪 Tarjetas de Prueba

**Visa Aprobada:**
- Número: `4509 9535 6623 3704`
- CVV: `123`
- Fecha: Cualquier fecha futura
- Nombre: APRO

---

## 📚 Documentación Completa

- **Configuración detallada**: Ver `GUIA_CONFIGURACION_MERCADOPAGO.md`
- **Flujo para usuarios**: Ver `FLUJO_PAGO_USUARIOS.md`

---

## ✅ Checklist Rápido

- [ ] SDK instalado (`pip install mercadopago`)
- [ ] Credenciales obtenidas de Mercado Pago Developers
- [ ] Variables agregadas en `.env`
- [ ] Configuración verificada
- [ ] Probar pago en modo test
- [ ] Listo para usar

---

**¡Listo!** 🎉 Ahora los usuarios pueden pagar con Mercado Pago usando múltiples métodos.



