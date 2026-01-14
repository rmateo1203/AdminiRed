en# 🔧 Solución: Error 404 "Not found 'card_token_id'"

## ❌ Error Completo

```json
{
    "message": "Error produced trying to parse async response from: [AssociateCard], error[card-token apicall failed]",
    "reason": "pool[AssociateCard]_external_api_error [method:parseResponse]",
    "status": 404,
    "details": {
        "cause": [
            {
                "code": 204,
                "description": "Not found 'card_token_id' with id: ba26928619492436a39dccab138657b8"
            }
        ]
    }
}
```

---

## 🔍 ¿Qué Significa Este Error?

Mercado Pago está intentando usar un **token de tarjeta** que:
- ❌ Ya no existe en el sistema
- ❌ Ha expirado (los tokens tienen duración limitada)
- ❌ Fue invalidado
- ❌ Pertenece a una sesión anterior

---

## ✅ Solución Definitiva

### Paso 1: Cerrar y Reiniciar

1. **Cierra completamente** la página de Mercado Pago
2. **Cierra la pestaña** del navegador
3. **Vuelve al portal** de tu sitio web

### Paso 2: Limpiar Caché y Cookies

1. **Abre las herramientas de desarrollador** (F12)
2. **Ve a la pestaña "Application"** (o "Aplicación")
3. **En el menú izquierdo, expande "Cookies"**
4. **Selecciona** `https://sandbox.mercadopago.com.mx`
5. **Haz clic derecho → "Clear"** (Limpiar)
6. **Repite** con `https://www.mercadopago.com.mx` si aparece

### Paso 3: Iniciar Nuevo Proceso de Pago

1. **Ve al portal del cliente**: `/clientes/portal/`
2. **Selecciona un pago** en "Mis Pagos"
3. **Haz clic en "Pagar en Línea"**
4. **Elige "Mercado Pago"**

Esto creará una **nueva preferencia de pago** con tokens frescos.

### Paso 4: Ingresar Tarjeta DESDE CERO

**⚠️ IMPORTANTE:** No uses tarjetas guardadas.

1. Si aparece una tarjeta guardada:
   - Haz clic en **"Modificar"** o **"Eliminar"**
   - O simplemente ignórala

2. **Ingresa la tarjeta completa desde cero:**

```
Número: 4509 9535 6623 3704
Tipo: Crédito
Nombre: APRO
Vencimiento: 11/25
CVV: 123
Tipo de Documento: DNI
Número de Documento: 12345678
Email: test@example.com
```

3. **NO marques** la casilla de "Guardar tarjeta" (si aparece)

4. **Haz clic en "Pagar" INMEDIATAMENTE** después de ingresar los datos

### Paso 5: Si el Error Persiste

**Usa modo incógnito:**

1. Abre una **ventana de incógnito**:
   - Chrome/Edge: `Ctrl + Shift + N`
   - Firefox: `Ctrl + Shift + P`

2. Accede al portal en modo incógnito

3. Realiza el pago

Esto evita cualquier conflicto con cookies o tokens antiguos.

---

## 🎯 Método Alternativo: Limpiar Todo

Si ninguna solución funciona, haz un "reset completo":

### Opción A: Navegador Limpio

1. Cierra **todas las pestañas** relacionadas con Mercado Pago
2. Cierra el navegador completamente
3. Abre el navegador de nuevo
4. Inicia el proceso de pago desde cero

### Opción B: Usar Otro Navegador

1. Si estás usando Chrome, prueba con Firefox o Edge
2. O viceversa
3. Esto evitará cualquier problema de caché persistente

---

## 🔐 Datos de Tarjeta Correctos

Asegúrate de usar estos datos **exactos**:

```
Número: 4509 9535 6623 3704
Tipo: Crédito (Visa)
Nombre: APRO
Vencimiento: 11/25 (mes/año)
CVV: 123
Tipo de Documento: DNI
Número de Documento: 12345678
Email: test@example.com
```

**Puntos críticos:**
- ✅ **Sin espacios** en el número de tarjeta
- ✅ **CVV exactamente:** `123`
- ✅ **Fecha futura:** `11/25` o cualquier fecha futura
- ✅ **Documento:** Al menos 8 dígitos

---

## 🔄 Tarjetas Alternativas

Si la Visa no funciona, prueba con Mastercard:

```
Número: 5031 7557 3453 0604
Tipo: Crédito (Mastercard)
Nombre: APRO
Vencimiento: 11/25
CVV: 123
Tipo de Documento: DNI
Número de Documento: 12345678
```

---

## 🐛 Verificación en Logs

Revisa los logs del servidor Django. Deberías ver:

```
Creando preferencia de Mercado Pago para pago X
Datos de preferencia - back_urls: {...}
Auto_return deshabilitado (localhost detectado)
URL success completa: http://localhost:8000/pagos/X/pago-exitoso/
Preference ID: (un ID nuevo cada vez)
```

**Importante:** El Preference ID debe ser **diferente cada vez** que inicias un nuevo pago. Si ves el mismo ID repetido, eso podría causar problemas.

---

## 📋 Checklist de Solución

Sigue estos pasos en orden:

- [ ] Paso 1: Cerré la página de Mercado Pago completamente
- [ ] Paso 2: Limpié cookies de Mercado Pago (F12 → Application → Cookies)
- [ ] Paso 3: Cerré y reabrí el navegador
- [ ] Paso 4: Inicié un NUEVO proceso de pago desde el portal
- [ ] Paso 5: NO usé tarjetas guardadas
- [ ] Paso 6: Ingresé la tarjeta desde cero con los datos exactos
- [ ] Paso 7: NO marqué "Guardar tarjeta"
- [ ] Paso 8: Hice clic en "Pagar" inmediatamente después de ingresar

---

## 💡 Por Qué Ocurre Este Error

### Causas Comunes:

1. **Token Expirado:**
   - Los tokens de Mercado Pago tienen duración limitada
   - Si tardas mucho entre ingresar la tarjeta y hacer clic en "Pagar", el token puede expirar

2. **Reutilización de Tokens:**
   - Intentar usar una tarjeta guardada de una sesión anterior
   - Los tokens no se pueden reutilizar entre sesiones

3. **Interrupciones:**
   - Si recargas la página después de ingresar la tarjeta
   - Si cierras y vuelves a abrir la pestaña

4. **Caché del Navegador:**
   - Cookies o localStorage con tokens antiguos

---

## ✅ Prevención

Para evitar este error en el futuro:

1. **Siempre ingresa la tarjeta desde cero** (no uses guardadas)
2. **No guardes la tarjeta** durante las pruebas
3. **Haz clic en "Pagar" inmediatamente** después de ingresar los datos
4. **No recargues la página** durante el proceso de pago
5. **No cierres la pestaña** mientras procesas el pago

---

## 🚨 Si Nada Funciona

Si después de seguir todos los pasos el error persiste:

1. **Verifica las credenciales:**
   ```bash
   # Verifica que tengas credenciales de sandbox
   grep MERCADOPAGO .env
   ```
   Deben empezar con `TEST-`

2. **Reinicia el servidor Django:**
   ```bash
   # Ctrl+C para detener
   python manage.py runserver
   ```

3. **Verifica la versión del SDK:**
   ```bash
   pip show mercadopago
   ```
   Debe estar actualizado

4. **Contacta soporte:**
   - Comparte el error completo
   - Menciona que estás usando credenciales de sandbox
   - Incluye los logs del servidor Django

---

**¡Sigue los pasos del checklist y el error debería resolverse!** 🎉

La clave es: **limpiar todo y empezar desde cero con una tarjeta nueva**.




