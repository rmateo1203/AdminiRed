# 🚀 Instalar y Usar ngrok - Guía Rápida

## 📥 Instalación

### Método 1: Snap (Más Fácil - Ubuntu/Debian)

```bash
sudo snap install ngrok
```

### Método 2: Descarga Manual

1. **Ve a:** https://ngrok.com/download
2. **Descarga** el binario para Linux
3. **Descomprime:**
   ```bash
   unzip ngrok.zip
   ```
4. **Mueve a un directorio en PATH:**
   ```bash
   sudo mv ngrok /usr/local/bin/
   ```
5. **Hazlo ejecutable:**
   ```bash
   sudo chmod +x /usr/local/bin/ngrok
   ```

### Método 3: Con wget

```bash
# Descargar
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz

# Descomprimir
tar xvzf ngrok-v3-stable-linux-amd64.tgz

# Mover a /usr/local/bin
sudo mv ngrok /usr/local/bin/
```

---

## ✅ Verificar Instalación

```bash
ngrok version
```

Deberías ver algo como: `ngrok version 3.x.x`

---

## 🚀 Uso Básico

### Paso 1: Asegúrate de que Django esté corriendo

```bash
python manage.py runserver
```

### Paso 2: Inicia ngrok (en otra terminal)

```bash
ngrok http 8000
```

### Paso 3: Copia la URL HTTPS

Verás algo como:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

Copia la URL **HTTPS** (la que empieza con `https://`)

### Paso 4: Actualiza .env

```bash
# Edita .env y cambia SITE_URL
SITE_URL=https://abc123.ngrok.io
```

### Paso 5: Reinicia Django

```bash
# Ctrl+C para detener
python manage.py runserver
```

---

## 💡 Notas Importantes

1. **La URL cambia cada vez:** Cada vez que reinicias ngrok, obtienes una URL diferente
2. **Usa HTTPS:** Siempre usa la URL HTTPS (no HTTP) en SITE_URL
3. **Mantén ngrok corriendo:** ngrok debe estar corriendo mientras usas el sitio
4. **Panel web:** Visita `http://127.0.0.1:4040` para ver las requests en tiempo real

---

## 🎯 Comandos Útiles

```bash
# Verificar que ngrok está corriendo
ps aux | grep ngrok

# Detener ngrok
# En la terminal donde está corriendo: Ctrl+C

# Ver requests en tiempo real
# Abre en navegador: http://127.0.0.1:4040
```

---

¡Listo! 🎉



