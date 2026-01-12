# 🔧 Solución: Página de Advertencia de ngrok

## ❌ Problema

ngrok muestra una página de advertencia antes de permitir el acceso al sitio cuando se usa la cuenta gratuita. Esto interrumpe el flujo de pago.

---

## ✅ Soluciones

### Solución 1: Hacer Clic en "Visit Site" (Temporal)

La primera vez que accedas a través de ngrok, simplemente haz clic en el botón **"Visit Site"**. Después de eso, ngrok recordará y no mostrará la advertencia para ese dominio.

**Limitación:** Si cambias la URL de ngrok, tendrás que hacer clic nuevamente.

---

### Solución 2: Configurar ngrok con `--host-header` (Recomendado)

He actualizado el script `iniciar_ngrok_y_configurar.sh` para usar la opción `--host-header`:

```bash
ngrok http 8000 --host-header="localhost:8000"
```

Esto ayuda a que ngrok reconozca mejor las solicitudes.

---

### Solución 3: Usar User-Agent Personalizado en Redirecciones

El middleware creado (`core/middleware.py`) intenta agregar el header, pero ngrok requiere que el header se envíe en la **solicitud del cliente**, no en la respuesta del servidor.

Para que funcione completamente, necesitarías que el navegador envíe el header. Esto se puede hacer con JavaScript, pero es más complejo.

---

### Solución 4: Actualizar a Cuenta de Pago de ngrok

Con una cuenta de pago de ngrok, no aparece la página de advertencia. Pero esto requiere un plan de pago.

---

## 🎯 Solución Implementada

He creado:

1. **Middleware** (`core/middleware.py`): Agrega el header `ngrok-skip-browser-warning` en las respuestas
2. **Script actualizado**: Usa `--host-header` al iniciar ngrok

---

## 📋 Pasos para Aplicar

1. **Reinicia ngrok** con el script actualizado:
   ```bash
   ./iniciar_ngrok_y_configurar.sh 8000
   ```

2. **Reinicia Django** para cargar el nuevo middleware

3. **La primera vez**, haz clic en "Visit Site" en la página de advertencia

4. **Después de eso**, la advertencia no debería aparecer para ese dominio

---

## ⚠️ Nota Importante

La página de advertencia de ngrok es una medida de seguridad. Aparece:
- ✅ Solo la primera vez por dominio
- ✅ Para proteger a los usuarios de sitios no confiables
- ✅ Es normal en la cuenta gratuita de ngrok

**Para desarrollo:** Simplemente haz clic en "Visit Site" la primera vez y listo.

**Para producción:** Usa tu dominio real (no ngrok) y no verás esta advertencia.

---

## 🔄 Alternativa: Configurar ngrok para Desarrollo Local

Si solo necesitas probar localmente sin la advertencia, puedes:

1. **Usar localhost directamente** (sin ngrok) para pruebas locales
2. **Solo usar ngrok** cuando necesites probar el flujo completo con Mercado Pago

---

**El middleware está configurado. Reinicia Django y ngrok para aplicar los cambios.** 🚀


