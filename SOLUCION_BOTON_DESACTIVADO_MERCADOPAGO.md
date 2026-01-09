# Solución: Botón de Pagar Desactivado en Mercado Pago

## ✅ Diagnóstico Realizado

La preferencia se está creando correctamente con:
- ✅ Email válido: `isc.rmateo@gmail.com`
- ✅ Nombre del pagador: `OSCAR GONZALEZ RIVERA`
- ✅ Teléfono válido: área code `88`, número `74512554`
- ✅ SITE_URL público (ngrok): `https://unpunctually-formulaic-kelsie.ngrok-free.dev`

## 🔍 Posibles Causas del Botón Desactivado

El botón se desactiva generalmente por problemas en el **frontend de Mercado Pago**, no en la creación de la preferencia:

### 1. **Problema con el Card Token** (Más Común)
Cuando ingresas los datos de la tarjeta, Mercado Pago intenta crear un `card_token`. Si falla:
- El botón se desactiva
- Aparecen errores en la consola del navegador

**Solución:**
- Limpia los datos de la tarjeta completamente
- Ingresa los datos de la tarjeta de prueba desde cero
- No copies/pegues, escríbelos manualmente

### 2. **Tarjeta de Prueba con Problemas**
Algunas tarjetas de prueba pueden tener restricciones.

**Tarjeta de Prueba Recomendada:**
```
Número: 4509 9535 6623 3704
Nombre: APRO
Vencimiento: 11/25
CVV: 123
Tipo: Crédito
DNI: 12345678
```

### 3. **Cookies/Cache del Navegador**
Las cookies o caché pueden interferir.

**Solución:**
1. Limpia las cookies de `sandbox.mercadopago.com.mx`
2. Limpia el caché del navegador
3. Prueba en una ventana de incógnito

### 4. **Problemas de JavaScript en Mercado Pago**
Errores en el JavaScript de Mercado Pago pueden desactivar el botón.

**Verificación:**
1. Abre la consola del navegador (F12)
2. Busca errores en rojo
3. Busca especialmente errores relacionados con `card_token` o `AssociateCard`

## 🛠️ Pasos de Solución

### Paso 1: Reinicia Django
```bash
# Detén el servidor (Ctrl+C) y reinicia
python manage.py runserver
```

### Paso 2: Crea un NUEVO Intent de Pago
**IMPORTANTE:** No uses la URL antigua. Crea un nuevo intento desde el portal del cliente.

### Paso 3: Limpia el Navegador
1. Presiona `Ctrl + Shift + Delete`
2. Selecciona "Cookies" y "Caché"
3. Limpia datos de `mercadopago.com` y `mercadolibre.com`

### Paso 4: Prueba en Ventana de Incógnito
1. Abre una ventana de incógnito (Ctrl + Shift + N)
2. Accede a la URL del pago
3. Intenta el pago nuevamente

### Paso 5: Verifica la Consola del Navegador
1. Abre DevTools (F12)
2. Ve a la pestaña **Console**
3. Busca errores en rojo
4. Ve a la pestaña **Network**
5. Busca la petición `card_tokens` o `AssociateCard`
6. Revisa la respuesta - si hay un error 404 o 400, ese es el problema

### Paso 6: Re-ingresa los Datos de la Tarjeta
1. Haz clic en "Modificar" en la tarjeta
2. Borra todos los datos
3. Ingresa los datos de la tarjeta de prueba manualmente (no copies/pegues)
4. Espera a que el formulario valide los datos
5. El botón debería activarse

## 📋 Verificación Final

Si después de todos estos pasos el botón sigue desactivado:

1. **Revisa los logs de Django** - Busca los mensajes sobre la preferencia creada
2. **Revisa la respuesta de Mercado Pago** - En los logs deberías ver el JSON completo de la respuesta
3. **Verifica la consola del navegador** - Busca errores específicos relacionados con el token de la tarjeta

## ⚠️ Nota Importante sobre ngrok

**Ngrok NO debería causar que el botón se desactive**, pero puede causar problemas si:
- La URL de ngrok cambia constantemente
- Hay problemas de conectividad con ngrok

Si el problema persiste, intenta:
1. Verificar que ngrok esté corriendo y estable
2. Usar un dominio de ngrok estático (plan de pago)
3. O temporalmente probar sin ngrok usando `localhost:8000` (aunque no funcionará el `auto_return`)

## 🔄 Código Actualizado

El código ya incluye:
- ✅ Validación mejorada del email
- ✅ Formato correcto del teléfono
- ✅ Logging detallado para debug
- ✅ Validación de campos requeridos

**El problema ahora es más probable que sea en el frontend de Mercado Pago, no en nuestro código.**

