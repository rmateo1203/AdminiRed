# 🔧 Solución: Error al Procesar Pago con Mercado Pago

## ⚠️ Aclaración Importante

**Stripe NO es necesario** para el demo. El mensaje sobre `STRIPE_SECRET_KEY` es solo informativo.

Para el demo solo necesitas configurar:
- ✅ **Mercado Pago** O
- ✅ **PayPal** O
- ✅ **Ambos**

No necesitas Stripe a menos que quieras usarlo también.

---

## 🔴 Error Actual: "Error desconocido" con Mercado Pago

### Paso 1: Diagnosticar el Problema

Ejecuta este comando para ver el error exacto:

```bash
python3 diagnosticar_error_mercadopago.py
```

Este script te mostrará:
- ✅ Si las credenciales están configuradas
- ✅ Si el SDK está instalado
- ✅ El error específico de Mercado Pago
- ✅ Qué está fallando exactamente

---

## ✅ Soluciones Comunes

### Problema 1: Access Token Vacío o Inválido

**Síntoma**: Error al crear preferencia o "Error desconocido"

**Solución**:

1. Verifica que `MERCADOPAGO_ACCESS_TOKEN` esté en `.env`:
   ```bash
   grep MERCADOPAGO_ACCESS_TOKEN .env
   ```

2. Verifica que tenga un valor válido:
   ```env
   MERCADOPAGO_ACCESS_TOKEN=TEST-tu_token_completo_aqui
   ```

3. Asegúrate de que:
   - ✅ El token empiece con `TEST-` (modo test)
   - ✅ Esté completo (es muy largo)
   - ✅ No tenga espacios antes o después del `=`
   - ✅ No esté comentado (no empiece con `#`)

### Problema 2: Cliente Sin Email o Teléfono

**Síntoma**: Error al crear preferencia

**Solución**:

El código ya maneja esto, pero asegúrate de que el cliente tenga:
- Al menos un email O un teléfono

Si el cliente no tiene estos datos, puedes agregarlos desde el admin o editar el cliente.

### Problema 3: SDK No Instalado

**Síntoma**: ImportError al procesar pago

**Solución**:

```bash
pip install mercadopago>=2.2.0
```

O agregar a `requirements.txt`:
```
mercadopago>=2.2.0
```

### Problema 4: Monto Inválido

**Síntoma**: Error al crear preferencia

**Solución**:

Verifica que el pago tenga:
- Monto mayor a 0
- Formato válido (ej: 100.00, no "100,00" o "100.00 MXN")

### Problema 5: SITE_URL No Configurado

**Síntoma**: URLs de retorno inválidas

**Solución**:

Agrega en `.env`:
```env
SITE_URL=http://localhost:8000
```

---

## 🔍 Verificación Paso a Paso

### 1. Verificar Credenciales

```bash
python3 verificar_configuracion_pagos.py
```

Deberías ver:
```
✅ MERCADOPAGO_ACCESS_TOKEN: Configurado
```

Si no, agrega las credenciales en `.env`.

### 2. Verificar SDK

```bash
python -c "import mercadopago; print('✅ SDK instalado')"
```

Si sale error:
```bash
pip install mercadopago>=2.2.0
```

### 3. Diagnosticar el Error Específico

```bash
python3 diagnosticar_error_mercadopago.py
```

Este script te dirá exactamente qué está fallando.

---

## 📝 Ejemplo de .env Correcto

```env
# URL del sitio
SITE_URL=http://localhost:8000

# Mercado Pago - Credenciales de TEST
MERCADOPAGO_ACCESS_TOKEN=TEST-1234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk
MERCADOPAGO_PUBLIC_KEY=TEST-abcdefghijk-01234567890-abcdefghijk

# PayPal (opcional)
PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_SECRET=tu_secret
PAYPAL_MODE=sandbox

# Stripe (NO necesario para el demo)
# STRIPE_SECRET_KEY=opcional
```

---

## 🔄 Reiniciar Después de Cambios

**MUY IMPORTANTE**: Después de modificar `.env`:

1. Detén el servidor (Ctrl+C)
2. Reinicia:
   ```bash
   python manage.py runserver
   ```

---

## 🧪 Probar de Nuevo

1. Ve al portal: http://localhost:8000/clientes/portal/mis-pagos/
2. Haz clic en un pago pendiente/vencido
3. Haz clic en "Pagar en Línea"
4. Selecciona "Mercado Pago"
5. Haz clic en "Continuar con el Pago"

**Si aún hay error**, ejecuta `python3 diagnosticar_error_mercadopago.py` y comparte el resultado.

---

## 🆘 Si Aún No Funciona

1. **Ejecuta el diagnóstico**:
   ```bash
   python3 diagnosticar_error_mercadopago.py
   ```

2. **Revisa los logs del servidor** (en la consola donde corre Django):
   - Deberías ver mensajes de error detallados
   - Busca líneas que digan "Error de Mercado Pago" o "Error inesperado"

3. **Verifica las credenciales directamente**:
   - Ve a Mercado Pago Developers
   - Verifica que tu Access Token sea válido
   - Puedes crear uno nuevo si es necesario

---

## 📞 Recursos

- **Obtener credenciales**: `OBTENER_CREDENCIALES_PASO_A_PASO.md`
- **Configuración rápida**: `CONFIGURAR_PASARELAS_RAPIDO.md`
- **Demo completo**: `DEMO_PAGOS_MERCADOPAGO_PAYPAL.md`

---

**¡Recuerda: Stripe NO es necesario para el demo! Solo necesitas Mercado Pago o PayPal.** ✅


