# 🔄 Solución: Retorno desde Mercado Pago al Sistema Django

## 🎯 Problema

Después de realizar el pago en Mercado Pago, el usuario se queda en la pantalla de Mercado Pago y no regresa automáticamente al sistema Django.

## 🔍 Causa

Cuando se usa `localhost` o `127.0.0.1`, Mercado Pago **NO permite** la redirección automática (`auto_return`). Esto es una limitación de seguridad de Mercado Pago que requiere un dominio público válido.

## ✅ Solución Implementada

### 1. **Instrucciones Claras en la Página de Selección de Pasarela**

Se agregó un banner informativo visible que se muestra **SOLO cuando se detecta localhost**, indicando al usuario que:

1. Después de completar el pago, será redirigido a la página de confirmación de Mercado Pago
2. Debe hacer clic en el botón **"Volver al sitio"** o **"Volver a la tienda"** que aparece en la página de Mercado Pago
3. Una vez que haga clic, será redirigido automáticamente al sistema

**Ubicación:** `pagos/templates/pagos/pago_seleccionar_pasarela.html`

### 2. **Flujo Completo de Retorno**

```
1. Usuario completa pago en Mercado Pago ✅
   ↓
2. Mercado Pago muestra: "¡Listo! Tu pago ya se acreditó" 📄
   ↓
3. Usuario hace clic en "Volver al sitio" 👆 (manual, necesario con localhost)
   ↓
4. Redirección a: /pagos/{id}/pago-exitoso/ en Django ✅
   ↓
5. Redirección automática después de 5 segundos a: /clientes/portal/ 🎉
```

---

## 📋 Cambios Realizados

### Archivo: `pagos/views.py`

**Línea ~842-849:**
- Se agregó detección de `localhost` usando `SITE_URL`
- Se pasa la variable `es_localhost` al contexto del template

```python
# Detectar si estamos en localhost para mostrar advertencia
base_url = getattr(settings, 'SITE_URL', None) or request.build_absolute_uri('/').rstrip('/')
es_localhost = any(host in base_url.lower() for host in ['localhost', '127.0.0.1', '0.0.0.0'])

context = {
    'pago': pago,
    'pasarelas_disponibles': pasarelas_disponibles,
    'es_localhost': es_localhost,
}
```

### Archivo: `pagos/templates/pagos/pago_seleccionar_pasarela.html`

**Línea ~36-58:**
- Se agregó un banner informativo con estilo destacado (amarillo/dorado)
- Solo se muestra cuando `es_localhost` es `True`
- Instrucciones claras paso a paso

---

## 🎨 Aspecto Visual del Banner

El banner tiene:
- **Fondo:** Gradiente amarillo/dorado suave
- **Borde izquierdo:** Amarillo oscuro (4px)
- **Icono:** ⚠️ Información
- **Título:** "Instrucciones Importantes"
- **Contenido:** Explicación clara con pasos a seguir
- **Sección destacada:** Caja blanca con borde que resalta el paso importante

---

## 🔧 Para Habilitar Redirección Automática (Producción)

Si quieres que la redirección sea **completamente automática** sin necesidad de hacer clic, necesitas usar un dominio público:

### Opción 1: Usar ngrok (Para pruebas locales)

1. **Instalar ngrok:**
   ```bash
   sudo snap install ngrok
   ```

2. **Iniciar ngrok:**
   ```bash
   ngrok http 8000
   ```

3. **Copiar la URL HTTPS** (ej: `https://abc123.ngrok.io`)

4. **Actualizar `.env`:**
   ```env
   SITE_URL=https://abc123.ngrok.io
   ```

5. **Reiniciar Django**

Con ngrok, el banner NO se mostrará y la redirección será automática.

### Opción 2: Usar un Dominio Real (Producción)

1. Configura tu dominio público (ej: `https://tudominio.com`)
2. Actualiza `.env`:
   ```env
   SITE_URL=https://tudominio.com
   ```
3. Reinicia Django

Con un dominio público, Mercado Pago habilitará `auto_return` y la redirección será automática.

---

## 📍 Dónde Está el Botón "Volver al Sitio" en Mercado Pago

En la página de éxito de Mercado Pago, el botón puede aparecer en diferentes ubicaciones:

1. **En la parte superior de la página** (arriba del mensaje "¡Listo! Tu pago ya se acreditó")
2. **En la parte inferior de la página** (debajo del resumen del pago)
3. **Como parte del mensaje de confirmación**

El texto puede variar:
- "Volver al sitio"
- "Volver a la tienda"
- "Continuar"

---

## ✅ Verificación

### 1. Verificar que el Banner Aparece

1. Ve a: `/pagos/{id}/pagar-online/`
2. Deberías ver un banner amarillo con instrucciones
3. Solo aparece si `SITE_URL` contiene `localhost`, `127.0.0.1`, o `0.0.0.0`

### 2. Probar el Flujo Completo

1. Selecciona Mercado Pago
2. Completa el pago con una tarjeta de prueba
3. En la página de éxito de Mercado Pago, busca el botón "Volver al sitio"
4. Haz clic en él
5. Deberías ser redirigido a `/pagos/{id}/pago-exitoso/`
6. Después de 5 segundos, serás redirigido automáticamente al portal

### 3. Verificar Logs

Los logs del servidor deberían mostrar:
```
Auto_return deshabilitado (localhost detectado). El usuario deberá hacer clic en 'Volver al sitio' manualmente.
```

---

## 🐛 Solución de Problemas

### El banner no aparece

- Verifica que `SITE_URL` en `.env` contenga `localhost` o `127.0.0.1`
- Recarga la página con `Ctrl + Shift + R` (limpiar caché)

### No encuentro el botón "Volver al sitio" en Mercado Pago

- Busca en la parte superior de la página
- Busca en la parte inferior de la página
- Revisa si hay un enlace de texto en lugar de un botón
- Si no aparece, puedes usar el botón "Atrás" del navegador, pero no es recomendable

### Después de hacer clic, no regresa al sistema

- Verifica que las URLs de retorno estén correctamente configuradas en los logs
- Verifica que el servidor Django esté corriendo
- Revisa los logs del servidor para errores

---

## 📚 Referencias

- [Documentación de Mercado Pago - back_urls](https://www.mercadopago.com.mx/developers/es/docs/checkout-pro/checkout-customization/preferences)
- [Documentación de Mercado Pago - auto_return](https://www.mercadopago.com.mx/developers/es/docs/checkout-pro/checkout-customization/preferences)

---

**¡Problema resuelto!** El usuario ahora tiene instrucciones claras sobre cómo regresar al sistema después del pago. 🎉









