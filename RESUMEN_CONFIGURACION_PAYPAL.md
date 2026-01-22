# 🚀 Resumen Rápido: Configuración de PayPal

## ⚡ Configuración en 3 Pasos

### 1️⃣ Obtener Credenciales de PayPal

1. Ve a: https://developer.paypal.com/
2. Inicia sesión o crea cuenta
3. Dashboard → "My Apps & Credentials"
4. Clic en "Create App"
5. Selecciona "Sandbox" para pruebas
6. Copia el **Client ID** y **Secret**

### 2️⃣ Agregar al Proyecto

Edita el archivo `.env` en la raíz del proyecto:

```env
PAYPAL_CLIENT_ID=tu_client_id_aqui
PAYPAL_SECRET=tu_secret_aqui
PAYPAL_MODE=sandbox
SITE_URL=http://localhost:8000
```

### 3️⃣ Verificar Configuración

Ejecuta:

```bash
python verificar_paypal.py
```

O:

```bash
python manage.py shell -c "
from django.conf import settings
print('Client ID:', '✅' if settings.PAYPAL_CLIENT_ID else '❌')
print('Secret:', '✅' if settings.PAYPAL_SECRET else '❌')
print('Mode:', settings.PAYPAL_MODE)
"
```

---

## 👥 Cómo Pagan los Usuarios

### Flujo Simple:

1. **Usuario** → Ve al detalle del pago
2. **Clic** en "Pagar en Línea"
3. **Selecciona** PayPal
4. **Redirige** a PayPal
5. **Aprueba** el pago
6. **Regresa** automáticamente
7. **✅ Pago completado**

### Visual:

```
Usuario → Detalle Pago → Pagar en Línea → Seleccionar PayPal 
    → PayPal (aprobar) → Regreso → ✅ Completado
```

---

## 📚 Documentación Completa

- **Configuración detallada**: Ver `GUIA_CONFIGURACION_PAYPAL.md`
- **Flujo para usuarios**: Ver `FLUJO_PAGO_USUARIOS.md`

---

## ✅ Checklist Rápido

- [ ] Credenciales obtenidas de PayPal Developer
- [ ] Variables agregadas en `.env`
- [ ] Configuración verificada
- [ ] Probar pago en sandbox
- [ ] Listo para usar

---

**¡Listo!** 🎉 Ahora los usuarios pueden pagar con PayPal.













