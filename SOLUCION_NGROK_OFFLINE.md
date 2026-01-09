# 🔧 Solución: ngrok Endpoint Offline (ERR_NGROK_3200)

## ❌ Error

```
The endpoint abc123.ngrok.io is offline.
ERR_NGROK_3200
```

Este error significa que el túnel de ngrok no está activo o la URL expiró.

---

## ✅ Solución Rápida

### Paso 1: Verificar si ngrok está corriendo

En una terminal, verifica si ngrok está activo:

```bash
ps aux | grep ngrok
```

Si no ves ningún proceso, ngrok no está corriendo.

### Paso 2: Iniciar ngrok

1. **Abre una nueva terminal**
2. **Asegúrate de que tu servidor Django esté corriendo** en el puerto 8000:
   ```bash
   python manage.py runserver
   ```

3. **En otra terminal, inicia ngrok:**
   ```bash
   ngrok http 8000
   ```

4. **Copia la URL HTTPS** que ngrok te da:
   ```
   Forwarding  https://abc123.ngrok.io -> http://localhost:8000
   ```
   (La URL será diferente cada vez)

### Paso 3: Actualizar SITE_URL en .env

1. **Abre el archivo `.env`** en la raíz del proyecto

2. **Actualiza `SITE_URL`** con la nueva URL de ngrok:
   ```env
   SITE_URL=https://abc123.ngrok.io
   ```
   ⚠️ **IMPORTANTE:** Usa la URL **HTTPS** (no HTTP)

3. **Guarda el archivo**

### Paso 4: Reiniciar el servidor Django

1. **Detén el servidor** (Ctrl+C)
2. **Inícialo de nuevo:**
   ```bash
   python manage.py runserver
   ```

Ahora tu servidor debería estar accesible desde internet a través de ngrok.

---

## 🔄 ¿Por Qué la URL Cambia?

**Con la cuenta gratuita de ngrok:**
- La URL cambia **cada vez que reinicias ngrok**
- Las URLs expiran después de cierto tiempo de inactividad
- Cada sesión genera una URL diferente

**Ejemplo:**
- Primera vez: `https://abc123.ngrok.io`
- Después de reiniciar: `https://xyz789.ngrok.io` (diferente)

---

## 💡 Solución Permanente (Opcional)

Si necesitas una URL fija para desarrollo:

### Opción 1: ngrok con cuenta gratuita + subdominio aleatorio

```bash
# Inicia ngrok con un subdominio personalizado (requiere cuenta gratuita)
ngrok http 8000 --subdomain=mi-proyecto-dev
```

Necesitarás:
1. Crear cuenta gratuita en https://ngrok.com
2. Obtener tu authtoken
3. Configurarlo: `ngrok config add-authtoken TU_TOKEN`

### Opción 2: ngrok con dominio reservado (pago)

Con un plan de pago de ngrok, puedes reservar un dominio fijo.

### Opción 3: Alternativas a ngrok

- **Cloudflare Tunnel** (gratis, URL fija)
- **LocalTunnel** (gratis, pero menos estable)
- **Serveo** (gratis, pero menos confiable)

---

## 🔍 Verificar que ngrok Funciona

Después de iniciar ngrok, deberías ver:

```
ngrok

Session Status                online
Account                       (tu cuenta)
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**URLs importantes:**
- **Forwarding:** Esta es la URL que debes usar en `SITE_URL`
- **Web Interface:** Panel web de ngrok en `http://127.0.0.1:4040` para ver requests

---

## 📋 Checklist de Configuración

- [ ] Servidor Django corriendo en puerto 8000
- [ ] ngrok iniciado y mostrando "Session Status: online"
- [ ] Copié la URL HTTPS del forwarding
- [ ] Actualicé `SITE_URL` en `.env` con la URL HTTPS de ngrok
- [ ] Reinicié el servidor Django
- [ ] Verifiqué que el sitio es accesible en `https://tu-url.ngrok.io`

---

## 🐛 Solución de Problemas

### Error: "ngrok: command not found"

**Solución:** ngrok no está instalado.

**Instalación:**
```bash
# Ubuntu/Debian
sudo snap install ngrok

# O descarga desde https://ngrok.com/download
# Descomprime y mueve a /usr/local/bin
```

### Error: "bind: address already in use"

**Solución:** El puerto 8000 ya está en uso.

**Verificar:**
```bash
lsof -i :8000
```

**Solución:**
- Detén el otro proceso
- O usa otro puerto: `ngrok http 8080` (y cambia Django a puerto 8080)

### Error: "authtoken required"

**Solución:** Necesitas autenticarte con ngrok (para funciones avanzadas).

**Solución:**
1. Crea cuenta en https://ngrok.com
2. Obtén tu authtoken
3. Ejecuta: `ngrok config add-authtoken TU_TOKEN`

---

## 🎯 Para Desarrollo Local sin ngrok

**Si no necesitas probar la redirección automática de Mercado Pago**, puedes trabajar sin ngrok:

1. **En `.env`:**
   ```env
   SITE_URL=http://localhost:8000
   ```

2. **En el código:**
   - Ya está configurado para detectar localhost
   - `auto_return` se deshabilita automáticamente
   - El pago funcionará, solo que sin redirección automática

3. **El usuario tendrá que hacer clic en "Volver al sitio"** después del pago

---

## 📝 Resumen

**Para resolver el error ERR_NGROK_3200:**

1. ✅ Inicia ngrok: `ngrok http 8000`
2. ✅ Copia la URL HTTPS (ej: `https://abc123.ngrok.io`)
3. ✅ Actualiza `.env`: `SITE_URL=https://abc123.ngrok.io`
4. ✅ Reinicia Django

**⚠️ Recuerda:** La URL de ngrok cambia cada vez que lo reinicias. Tendrás que actualizar `SITE_URL` cada vez.

---

**¡Después de seguir estos pasos, ngrok debería funcionar correctamente!** 🚀


