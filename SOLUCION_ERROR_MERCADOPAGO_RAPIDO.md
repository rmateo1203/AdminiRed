# ⚡ Solución Rápida: Error con Mercado Pago

## ✅ Estado Actual

Según la verificación:
- ✅ **Mercado Pago está configurado** (Access Token presente)
- ⚠️ PayPal tiene variables pero están vacías
- ❌ Stripe no configurado (NO es necesario para el demo)

---

## 🔴 El Problema: "Error desconocido"

El error ocurre cuando intentas procesar un pago. Las causas más comunes son:

### **Causa 1: Access Token Inválido o Vacío** (Más Común)

Aunque la verificación dice que está configurado, puede que:
- El token esté vacío o sea un placeholder
- El token sea inválido o haya expirado
- El token no sea de prueba (no empieza con TEST-)

**Solución**:

1. Abre el archivo `.env`
2. Verifica la línea `MERCADOPAGO_ACCESS_TOKEN=`
3. Asegúrate de que tenga un valor válido que empiece con `TEST-`
4. No debe tener espacios antes o después del `=`

Ejemplo correcto:
```env
MERCADOPAGO_ACCESS_TOKEN=TEST-1234567890123456-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk-01234567890-abcdefghijk
```

Ejemplo incorrecto:
```env
MERCADOPAGO_ACCESS_TOKEN = TEST-...  # Espacios alrededor del =
MERCADOPAGO_ACCESS_TOKEN=TEST-tu_token_aqui  # Placeholder, no valor real
```

---

### **Causa 2: SDK No Instalado**

**Solución**:

```bash
# Activa tu entorno virtual primero
source venv/bin/activate  # o el comando que uses

# Instala el SDK
pip install mercadopago>=2.2.0
```

---

### **Causa 3: No Has Reiniciado el Servidor**

**MUY IMPORTANTE**: Después de modificar `.env`, debes reiniciar:

```bash
# Detén el servidor (Ctrl+C)
# Inicia de nuevo
python manage.py runserver
```

---

### **Causa 4: Access Token Incorrecto**

El token debe ser:
- ✅ De **prueba** (empieza con `TEST-`)
- ✅ Completo (es muy largo, ~100 caracteres)
- ✅ Válido (obtenido desde Mercado Pago Developers)

**Si no tienes un token válido**:

1. Ve a: https://www.mercadopago.com.mx/developers
2. Inicia sesión
3. Ve a "Tus integraciones" → Tu aplicación
4. Haz clic en "Credenciales de prueba"
5. Copia el **Access Token** completo (el que empieza con TEST-)
6. Pégalo en `.env`

---

## 🔍 Verificar el Problema Específico

### Opción 1: Ver los Logs del Servidor

Cuando intentas pagar, mira la consola donde corre `python manage.py runserver`. Deberías ver mensajes como:

```
ERROR Error de Mercado Pago: [mensaje del error]
```

Este mensaje te dirá exactamente qué está fallando.

### Opción 2: Activar Entorno Virtual y Ejecutar Diagnóstico

```bash
# Activa el entorno virtual
source venv/bin/activate  # o como lo actives tú

# Ejecuta el diagnóstico
python diagnosticar_error_mercadopago.py
```

---

## ✅ Checklist Rápido

Antes de intentar de nuevo, verifica:

- [ ] El `MERCADOPAGO_ACCESS_TOKEN` en `.env` tiene un valor real (no placeholder)
- [ ] El token empieza con `TEST-`
- [ ] No hay espacios antes/después del `=` en `.env`
- [ ] `SITE_URL=http://localhost:8000` está en `.env`
- [ ] El SDK está instalado: `pip install mercadopago>=2.2.0`
- [ ] Reiniciaste el servidor después de modificar `.env`
- [ ] El cliente tiene email o teléfono (el código ya lo maneja, pero verifica)

---

## 🧪 Prueba Rápida

1. **Modifica `.env`** si es necesario
2. **Guarda el archivo**
3. **Reinicia el servidor**:
   ```bash
   # Ctrl+C para detener
   python manage.py runserver
   ```
4. **Intenta pagar de nuevo**

---

## 🆘 Si Aún No Funciona

Comparte esta información:

1. **El mensaje exacto de error** (de la consola del servidor o de la página)
2. **Las primeras 10 y últimas 10 caracteres** de tu `MERCADOPAGO_ACCESS_TOKEN` (sin mostrar todo por seguridad)
   - Ejemplo: `TEST-1234...xyz789`
3. **Si el servidor muestra algún error** en la consola cuando intentas pagar

Con esta información podré ayudarte mejor.

---

## 💡 Recordatorio

- ✅ **Mercado Pago configurado** = Puedes usarlo
- ❌ **Stripe no configurado** = NO es problema (no lo necesitas)
- ⚠️ **PayPal vacío** = NO es problema (puedes usar solo Mercado Pago)

**Enfócate en que Mercado Pago funcione primero.**

