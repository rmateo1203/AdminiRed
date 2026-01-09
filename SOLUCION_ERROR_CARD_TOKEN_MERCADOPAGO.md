# 🔧 Solución: Error "Not found 'card_token_id'" en Mercado Pago

## 🔍 Error Detectado

```
"Not found 'card_token_id' with id: a9079de6c28548c4f1fe2c2cea7e6818"
"Error produced trying to parse async response from: [AssociateCard]"
status: 404
```

Este error ocurre cuando Mercado Pago intenta procesar un token de tarjeta que:
- No existe en el sistema de Mercado Pago
- Ha expirado
- Fue invalidado
- Pertenece a una sesión anterior

---

## ✅ Soluciones Rápidas

### Solución 1: Limpiar Tarjetas Guardadas (Más Común)

**El problema**: Estás intentando usar una tarjeta guardada que ya no es válida.

**Pasos:**

1. **En la página de Mercado Pago:**
   - Haz clic en **"Modificar"** junto a la tarjeta guardada
   - Si aparece una opción para eliminar/borrar la tarjeta, hazlo
   - O simplemente ignora la tarjeta guardada

2. **Ingresa la tarjeta desde cero:**
   - Haz clic en **"Agregar nueva tarjeta"** o similar
   - Ingresa los datos de la tarjeta de prueba:
     ```
     Número: 4509 9535 6623 3704
     Nombre: APRO
     Vencimiento: 11/25 (o cualquier fecha futura)
     CVV: 123
     Tipo de documento: DNI / CURP / RFC
     Número de documento: 12345678
     Email: (cualquier email válido)
     ```

3. **No guardes la tarjeta** (por ahora, para evitar conflictos)

4. **Haz clic en "Pagar"** directamente después de ingresar los datos

---

### Solución 2: Recargar la Página de Mercado Pago

1. **Cierra la página actual de Mercado Pago**
2. **Vuelve al portal de tu sitio**
3. **Inicia el proceso de pago nuevamente:**
   - Selecciona el pago
   - Haz clic en "Pagar en Línea"
   - Elige Mercado Pago
4. Esto generará una **nueva preferencia de pago** con un token fresco

---

### Solución 3: Limpiar Caché y Cookies

1. **Abre las herramientas de desarrollador** (F12)
2. **Ve a la pestaña "Application" o "Aplicación"**
3. **Limpia:**
   - Cookies del dominio `sandbox.mercadopago.com.mx`
   - Local Storage
   - Session Storage
4. **Cierra y vuelve a abrir el navegador**
5. **Intenta el pago nuevamente**

---

### Solución 4: Usar Modo Incógnito

1. **Abre una ventana de incógnito** (Ctrl+Shift+N en Chrome/Edge, Ctrl+Shift+P en Firefox)
2. **Accede al portal del cliente**
3. **Realiza el pago**
4. Esto evitará conflictos con cookies o tokens antiguos

---

## 🔍 Verificación de la Preferencia

El error puede ocurrir si la preferencia de pago se creó hace mucho tiempo. Vamos a asegurarnos de que se cree una nueva preferencia cada vez.

### Verificar en los Logs

Revisa los logs del servidor Django. Deberías ver:

```
Creando preferencia de Mercado Pago para pago X
URLs de retorno validadas: ...
Preference ID: (un ID largo)
```

Si ves el mismo Preference ID repetido, eso podría ser el problema.

---

## 🛠️ Mejora del Código (Prevención)

Voy a verificar si necesitamos mejorar cómo se manejan los tokens en nuestro código. El problema puede estar en que:

1. La preferencia se está reutilizando
2. Los tokens se están cacheando incorrectamente
3. Hay un problema con la sesión

---

## 📋 Checklist de Solución

Sigue estos pasos en orden:

- [ ] **Paso 1**: Cierra la página actual de Mercado Pago
- [ ] **Paso 2**: Vuelve al portal y reinicia el proceso de pago
- [ ] **Paso 3**: Si ves una tarjeta guardada, haz clic en "Modificar" o elimínala
- [ ] **Paso 4**: Ingresa la tarjeta **desde cero** con los datos de prueba
- [ ] **Paso 5**: **No guardes la tarjeta** (desmarca la casilla si aparece)
- [ ] **Paso 6**: Haz clic en "Pagar" inmediatamente después de ingresar los datos
- [ ] **Paso 7**: Si el error persiste, prueba en modo incógnito

---

## 🔐 Datos de Tarjeta de Prueba Correctos

Asegúrate de usar estos datos **exactos**:

```
Número de Tarjeta: 4509 9535 6623 3704
Nombre en la Tarjeta: APRO
Fecha de Vencimiento: 11/25 (mes/año, cualquier fecha futura funciona)
CVV: 123
Tipo de Documento: DNI (o CURP, RFC, etc.)
Número de Documento: 12345678
Email: test@example.com (o cualquier email válido)
```

**⚠️ Importante:**
- No uses espacios en el número de tarjeta
- El CVV debe ser exactamente `123`
- La fecha debe ser futura
- El documento debe tener al menos 8 dígitos

---

## 🐛 Si el Error Persiste

Si después de seguir todos los pasos el error continúa:

1. **Verifica las credenciales:**
   - Asegúrate de usar credenciales de **sandbox** (`TEST-...`)
   - Verifica que `MERCADOPAGO_ACCESS_TOKEN` esté configurado correctamente

2. **Reinicia el servidor Django:**
   ```bash
   # Ctrl+C para detener
   python manage.py runserver
   ```

3. **Intenta con otra tarjeta de prueba:**
   ```
   Mastercard: 5031 7557 3453 0604
   CVV: 123
   Resto igual que arriba
   ```

4. **Revisa los logs del servidor:**
   - Busca errores al crear la preferencia
   - Verifica que las URLs sean correctas
   - Asegúrate de que no haya errores de red

---

## 💡 Explicación Técnica

### ¿Qué es un card_token_id?

Cuando ingresas los datos de una tarjeta en Mercado Pago, el sistema genera un **token temporal** que representa la tarjeta de forma segura. Este token:

- Es único para cada intento de pago
- Tiene una duración limitada
- Se usa para procesar el pago sin exponer los datos reales de la tarjeta

### ¿Por qué falla?

El error ocurre cuando:
- Mercado Pago intenta usar un token que ya no existe en su sistema
- El token expiró (tienen una duración limitada)
- Hubo un problema al generar el token inicialmente
- Estás intentando reutilizar un token de una sesión anterior

### Solución Preventiva

Para evitar este error:
- **No reutilices preferencias de pago antiguas**
- **Crea una nueva preferencia cada vez que inicias un pago**
- **No guardes tokens entre sesiones**
- **Asegúrate de que el flujo de pago sea directo** (sin interrupciones)

---

## ✅ Resumen

**Solución más rápida:**
1. Cierra la página de Mercado Pago
2. Reinicia el proceso de pago desde tu portal
3. Ingresa la tarjeta desde cero (no uses guardadas)
4. No guardes la tarjeta
5. Haz clic en "Pagar" inmediatamente

**Si no funciona:**
- Prueba en modo incógnito
- Limpia cookies y caché
- Verifica que las credenciales sean de sandbox

---

**¡Esto debería resolver el problema!** 🎉

Si el error persiste después de seguir estos pasos, comparte:
1. Los logs completos del servidor Django
2. Un screenshot de la consola del navegador con el error completo
3. Los pasos exactos que seguiste


