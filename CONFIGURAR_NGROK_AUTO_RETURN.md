# 🚀 Configurar ngrok para Auto-Return de Mercado Pago

## 🎯 Objetivo

Habilitar la redirección automática después del pago en Mercado Pago usando ngrok para crear un túnel público a localhost.

---

## 📋 Paso 1: Instalar ngrok

### Opción A: Usando snap (Recomendado para Ubuntu/Linux)

```bash
sudo snap install ngrok
```

### Opción B: Descarga directa

1. Ve a: https://ngrok.com/download
2. Descarga ngrok para Linux
3. Descomprime y mueve a `/usr/local/bin/`:
   ```bash
   unzip ngrok.zip
   sudo mv ngrok /usr/local/bin/
   sudo chmod +x /usr/local/bin/ngrok
   ```

### Opción C: Usando apt (si está disponible)

```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

---

## 📋 Paso 2: Crear cuenta en ngrok (Gratis)

1. Ve a: https://dashboard.ngrok.com/signup
2. Crea una cuenta gratuita
3. Obtén tu authtoken desde: https://dashboard.ngrok.com/get-started/your-authtoken

---

## 📋 Paso 3: Configurar ngrok

```bash
ngrok config add-authtoken TU_AUTHTOKEN_AQUI
```

Reemplaza `TU_AUTHTOKEN_AQUI` con tu token de ngrok.

---

## 📋 Paso 4: Iniciar ngrok

En una terminal separada, ejecuta:

```bash
ngrok http 8000
```

Esto creará un túnel público. Verás algo como:

```
Forwarding   https://abc123-def456.ngrok.io -> http://localhost:8000
```

**Copia la URL HTTPS** (ej: `https://abc123-def456.ngrok.io`)

---

## 📋 Paso 5: Actualizar SITE_URL en .env

Abre tu archivo `.env` y actualiza:

```env
# Antes:
SITE_URL=http://localhost:8000

# Después (con ngrok):
SITE_URL=https://abc123-def456.ngrok.io
```

**⚠️ IMPORTANTE:** 
- Usa la URL HTTPS (no HTTP)
- No agregues `/` al final
- Reemplaza `abc123-def456` con tu URL real de ngrok

---

## 📋 Paso 6: Reiniciar Django

```bash
# Detén el servidor Django (Ctrl+C)
# Luego reinicia:
python manage.py runserver
```

---

## ✅ Verificación

1. Inicia un pago de prueba
2. Verifica en los logs que ya NO aparezca el mensaje de advertencia
3. Deberías ver:
   ```
   Auto_return habilitado (redirección automática después del pago)
   ```
4. Después de completar el pago en Mercado Pago, serás redirigido automáticamente sin necesidad de hacer clic en "Volver al sitio"

---

## 🔄 Automatización (Opcional)

### Script para iniciar ngrok y Django juntos

Crea un archivo `start_dev.sh`:

```bash
#!/bin/bash

# Iniciar ngrok en segundo plano
ngrok http 8000 > /dev/null &
NGROK_PID=$!

# Esperar a que ngrok esté listo
sleep 3

# Obtener la URL de ngrok
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Error: No se pudo obtener la URL de ngrok"
    kill $NGROK_PID
    exit 1
fi

echo "✅ ngrok iniciado: $NGROK_URL"

# Actualizar .env con la nueva URL
sed -i "s|^SITE_URL=.*|SITE_URL=$NGROK_URL|" .env
echo "✅ .env actualizado: SITE_URL=$NGROK_URL"

# Función para limpiar al salir
cleanup() {
    echo "Deteniendo ngrok..."
    kill $NGROK_PID
    exit
}
trap cleanup INT TERM

# Iniciar Django
echo "Iniciando Django..."
python manage.py runserver

# Limpiar al finalizar
cleanup
```

Hazlo ejecutable:

```bash
chmod +x start_dev.sh
```

Usa:

```bash
./start_dev.sh
```

---

## 🐛 Solución de Problemas

### Error: "ngrok: command not found"

- Verifica que ngrok esté instalado: `which ngrok`
- Si no está, sigue el Paso 1 para instalarlo

### Error: "authtoken is required"

- Ejecuta: `ngrok config add-authtoken TU_TOKEN`
- Obtén tu token desde: https://dashboard.ngrok.com/get-started/your-authtoken

### La URL de ngrok cambia cada vez

**Solución para URL fija (Plan de pago):**

1. Crea una cuenta en ngrok (gratis)
2. Ve a: https://dashboard.ngrok.com/cloud-edge/domains
3. Reserva un dominio gratuito (ej: `mi-app.ngrok-free.app`)
4. Inicia ngrok con tu dominio:
   ```bash
   ngrok http 8000 --domain=mi-app.ngrok-free.app
   ```

**Solución temporal (URL dinámica):**

- Actualiza `.env` cada vez que inicies ngrok con la nueva URL

### El servidor Django no responde a través de ngrok

- Verifica que Django esté corriendo en el puerto 8000: `python manage.py runserver`
- Verifica que ngrok esté corriendo: `curl http://localhost:4040/api/tunnels`

### Error 502 Bad Gateway

- Asegúrate de que Django esté corriendo en `localhost:8000`
- Verifica que ngrok esté apuntando al puerto correcto

---

## 📝 Notas Importantes

1. **URL de ngrok cambia:** Con la cuenta gratuita, la URL cambia cada vez que reinicias ngrok (excepto si usas un dominio reservado)

2. **Webhooks:** Si configuraste webhooks de Mercado Pago, también necesitarás actualizar la URL del webhook para usar ngrok

3. **Producción:** En producción, usa tu dominio real (no ngrok)

4. **Seguridad:** ngrok expone tu servidor local a internet. Solo úsalo para desarrollo.

---

## 🎉 Resultado Esperado

Después de configurar ngrok:

1. ✅ No más advertencias sobre localhost
2. ✅ `auto_return` habilitado automáticamente
3. ✅ Redirección automática después del pago en Mercado Pago
4. ✅ Mejor experiencia de usuario (no necesita hacer clic en "Volver al sitio")

---

**¡Listo para probar!** 🚀

Configura ngrok y actualiza tu `.env` con la URL HTTPS de ngrok.









