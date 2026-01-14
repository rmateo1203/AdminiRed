# 📋 Resumen: Estado Actual de ngrok

## ✅ Estado Actual

### Authtoken de ngrok configurado:
```
381uKw30O08GisDZWGinwuPxmz3_4ZGQQo11zWBmfMZwet2uM
```

### URL pública de ngrok:
```
https://unpunctually-formulaic-kelsie.ngrok-free.dev
```

### Puerto local:
```
8082
```

## 🔧 Scripts Disponibles

### 1. `iniciar_ngrok_y_configurar.sh`
Inicia ngrok, obtiene la URL y actualiza `SITE_URL` en `.env` automáticamente.

**Uso:**
```bash
./iniciar_ngrok_y_configurar.sh [puerto]
# Ejemplo:
./iniciar_ngrok_y_configurar.sh 8082
```

**Características:**
- ✅ Detiene procesos de ngrok anteriores automáticamente
- ✅ Inicia ngrok con header para evitar la página de advertencia
- ✅ Actualiza `SITE_URL` en `.env` automáticamente
- ✅ Muestra la URL pública generada

### 2. `corregir_ngrok_auth.sh`
Configura el authtoken de ngrok.

**Uso:**
```bash
./corregir_ngrok_auth.sh
```

## 🛠️ Comandos Útiles

### Detener ngrok:
```bash
pkill -f "ngrok http"
# O más agresivo:
pkill -9 -f "ngrok"
```

### Ver información del túnel:
```bash
curl http://localhost:4040/api/tunnels | python3 -m json.tool
```

### Ver dashboard de ngrok:
Abre en el navegador: `http://localhost:4040`

### Iniciar ngrok manualmente:
```bash
/snap/bin/ngrok http 8082 \
    --request-header-add="ngrok-skip-browser-warning:true" \
    --host-header="localhost:8082"
```

## ⚠️ Solución de Problemas

### Error: "endpoint is already online"
**Solución:**
```bash
pkill -9 -f "ngrok"
sleep 2
# Luego inicia nuevamente
./iniciar_ngrok_y_configurar.sh 8082
```

### Error: "ERR_NGROK_3200" (endpoint offline)
**Solución:**
1. Verifica que ngrok esté corriendo: `ps aux | grep ngrok`
2. Si no está corriendo, inicia con: `./iniciar_ngrok_y_configurar.sh 8082`
3. Verifica la URL en: `http://localhost:4040`

### La URL de ngrok cambia cada vez
**Solución:**
- Con el plan gratuito, la URL cambia cada vez que reinicias ngrok
- Para URL estática, necesitas un plan de pago de ngrok
- Alternativamente, puedes usar el script `iniciar_ngrok_y_configurar.sh` que actualiza `SITE_URL` automáticamente

## 📝 Configuración Actual

### Archivo de configuración de ngrok:
```
/home/rmateo/snap/ngrok/340/.config/ngrok/ngrok.yml
```

### Variables de entorno necesarias:
- `SITE_URL` en `.env` - debe apuntar a la URL de ngrok
- `MERCADOPAGO_ACCESS_TOKEN` - token de acceso de Mercado Pago
- `MERCADOPAGO_PUBLIC_KEY` - clave pública de Mercado Pago

### Configuración en Django:
- `ALLOWED_HOSTS` - se actualiza automáticamente con el dominio de ngrok
- `CSRF_TRUSTED_ORIGINS` - se actualiza automáticamente con la URL de ngrok

## ✅ Verificación

Para verificar que todo está configurado correctamente:

1. **Verificar que ngrok esté corriendo:**
   ```bash
   ps aux | grep ngrok
   ```

2. **Obtener la URL actual:**
   ```bash
   curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*"' | head -1
   ```

3. **Verificar SITE_URL en .env:**
   ```bash
   grep SITE_URL .env
   ```

4. **Verificar que Django acepta el dominio:**
   - Revisa los logs de Django al iniciar
   - Deberías ver: `✅ Dominio agregado a ALLOWED_HOSTS: ...`
   - Deberías ver: `✅ Origen agregado a CSRF_TRUSTED_ORIGINS: ...`




