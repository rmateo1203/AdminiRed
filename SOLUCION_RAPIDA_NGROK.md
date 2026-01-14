# ⚡ Solución Rápida: Configurar ngrok

## 🎯 Objetivo

Habilitar auto-return de Mercado Pago para que la redirección sea automática después del pago.

---

## ⚡ Pasos Rápidos

### 1. Instalar ngrok

```bash
sudo snap install ngrok
```

### 2. Crear cuenta y obtener token

1. Visita: https://dashboard.ngrok.com/signup
2. Crea cuenta gratuita
3. Obtén tu token: https://dashboard.ngrok.com/get-started/your-authtoken

### 3. Configurar ngrok

```bash
ngrok config add-authtoken TU_TOKEN_AQUI
```

### 4. Iniciar ngrok (en terminal separada)

```bash
ngrok http 8000
```

**Copia la URL HTTPS** que aparece (ej: `https://abc123.ngrok.io`)

### 5. Actualizar .env

Edita `.env` y cambia:

```env
SITE_URL=https://abc123.ngrok.io
```

(Reemplaza con tu URL real de ngrok)

### 6. Reiniciar Django

```bash
python manage.py runserver
```

---

## ✅ Listo!

Ahora el auto-return funcionará. Mercado Pago redirigirá automáticamente después del pago.

---

**Nota:** Mantén ngrok corriendo mientras desarrollas. Si lo cierras, actualiza la URL en `.env`.




