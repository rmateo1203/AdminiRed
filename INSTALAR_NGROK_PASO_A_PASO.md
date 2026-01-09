# 🚀 Instalar y Configurar ngrok - Paso a Paso

## 📋 Paso 1: Instalar ngrok

### Opción A: Usando snap (Más fácil en Ubuntu/Linux)

```bash
sudo snap install ngrok
```

Si te pide contraseña, ingrésala y espera a que termine la instalación.

### Opción B: Descarga manual

```bash
# Descargar ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz

# Descomprimir
tar -xzf ngrok-v3-stable-linux-amd64.tgz

# Mover a /usr/local/bin
sudo mv ngrok /usr/local/bin/

# Hacer ejecutable
sudo chmod +x /usr/local/bin/ngrok

# Verificar instalación
ngrok version
```

---

## 📋 Paso 2: Crear cuenta en ngrok (Gratis)

1. Ve a: https://dashboard.ngrok.com/signup
2. Crea una cuenta con tu email
3. Confirma tu email si es necesario

---

## 📋 Paso 3: Obtener tu Authtoken

1. Ve a: https://dashboard.ngrok.com/get-started/your-authtoken
2. Copia tu authtoken (algo como: `2abc123def456ghi789jkl012mno345pqr678stu`)

---

## 📋 Paso 4: Configurar ngrok con tu Authtoken

Ejecuta en tu terminal:

```bash
ngrok config add-authtoken TU_AUTHTOKEN_AQUI
```

Reemplaza `TU_AUTHTOKEN_AQUI` con el token que copiaste.

Ejemplo:
```bash
ngrok config add-authtoken 2abc123def456ghi789jkl012mno345pqr678stu
```

Deberías ver: `Authtoken saved to configuration file: /home/tu-usuario/.config/ngrok/ngrok.yml`

---

## 📋 Paso 5: Iniciar ngrok

En una terminal nueva (o en segundo plano), ejecuta:

```bash
ngrok http 8000
```

Verás algo como:

```
ngrok

Session Status                online
Account                       tu-email@example.com (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       50ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123-def456.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**IMPORTANTE:** Copia la URL HTTPS (ej: `https://abc123-def456.ngrok.io`)

---

## 📋 Paso 6: Actualizar SITE_URL en .env

Abre tu archivo `.env` y actualiza:

```env
# Cambia esta línea:
SITE_URL=http://localhost:8000

# Por esta (con tu URL de ngrok):
SITE_URL=https://abc123-def456.ngrok.io
```

**⚠️ IMPORTANTE:**
- Usa HTTPS (no HTTP)
- No agregues `/` al final
- Reemplaza `abc123-def456` con tu URL real de ngrok

---

## 📋 Paso 7: Reiniciar Django

1. Detén el servidor Django (si está corriendo): `Ctrl + C`
2. Reinicia:
   ```bash
   python manage.py runserver
   ```

---

## ✅ Verificación

1. Inicia un pago de prueba
2. Verifica en los logs del servidor Django
3. **Ya NO deberías ver:**
   ```
   ⚠️  ADVERTENCIA: SITE_URL usa localhost...
   ```
4. **Deberías ver:**
   ```
   Auto_return habilitado (redirección automática después del pago)
   ```

---

## 🔄 Automatización (Opcional)

Si quieres automatizar el proceso, ejecuta:

```bash
./configurar_ngrok.sh
```

Este script:
- ✅ Verifica si ngrok está instalado
- ✅ Inicia ngrok automáticamente
- ✅ Obtiene la URL de ngrok
- ✅ Actualiza el `.env` automáticamente

---

## 🐛 Solución de Problemas

### Error: "ngrok: command not found"

Si instalaste con snap pero no funciona:
```bash
# Verifica si está instalado
snap list | grep ngrok

# Si no aparece, reinstala:
sudo snap install ngrok

# Si aparece pero no funciona, reinicia la terminal
```

### Error: "authtoken is required"

Asegúrate de haber ejecutado:
```bash
ngrok config add-authtoken TU_TOKEN
```

### La URL de ngrok cambia cada vez

**Con cuenta gratuita:** La URL cambia cada vez que reinicias ngrok.

**Solución:**
1. Reserva un dominio gratuito en ngrok:
   - Ve a: https://dashboard.ngrok.com/cloud-edge/domains
   - Reserva un dominio (ej: `mi-app.ngrok-free.app`)
2. Inicia ngrok con tu dominio:
   ```bash
   ngrok http 8000 --domain=mi-app.ngrok-free.app
   ```
3. Actualiza `.env` con tu dominio reservado:
   ```env
   SITE_URL=https://mi-app.ngrok-free.app
   ```

### Django no responde a través de ngrok

- Verifica que Django esté corriendo: `python manage.py runserver`
- Verifica que ngrok esté corriendo y apuntando al puerto 8000
- Revisa los logs de ngrok en: http://localhost:4040

---

## 📝 Notas Importantes

1. **Mantén ngrok corriendo:** Debes mantener ngrok corriendo mientras desarrollas. Si lo cierras, la URL dejará de funcionar.

2. **URL temporal:** Con cuenta gratuita, la URL cambia cada vez. Considera reservar un dominio si necesitas una URL estable.

3. **Producción:** En producción, usa tu dominio real (no ngrok).

4. **Webhooks:** Si usas webhooks de Mercado Pago, también actualiza la URL del webhook para usar ngrok.

---

## 🎉 Resultado

Después de configurar ngrok:

✅ No más advertencias sobre localhost  
✅ `auto_return` habilitado automáticamente  
✅ Redirección automática después del pago  
✅ Mejor experiencia de usuario  

---

**¡Listo para probar!** 🚀

