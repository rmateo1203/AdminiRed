# 🚀 Guía Rápida: Configurar Telegram (5 minutos)

## ⚡ Configuración Automática (Recomendada)

Ejecuta el script de ayuda:

```bash
python configurar_telegram.py
```

El script te guiará paso a paso para:
1. Crear tu bot en Telegram
2. Obtener tu Chat ID
3. Guardar la configuración en `.env`

---

## 📱 Configuración Manual

### Paso 1: Crear Bot en Telegram

1. Abre Telegram (app o web)
2. Busca: **@BotFather**
3. Inicia conversación
4. Envía: `/newbot`
5. Sigue las instrucciones:
   - **Nombre del bot:** `AdminiRed Notificaciones` (o el que prefieras)
   - **Username:** Debe terminar en `bot`, ej: `adminired_notificaciones_bot`
6. **Copia el TOKEN** que te da BotFather (ej: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Paso 2: Obtener tu Chat ID

**Opción A - Más fácil:**
1. Busca: **@userinfobot** en Telegram
2. Inicia conversación
3. Te mostrará tu Chat ID (número como `123456789`)
4. **Copia el Chat ID**

**Opción B - Alternativa:**
1. Busca tu bot por su username (ej: `@adminired_notificaciones_bot`)
2. Inicia conversación
3. Envía cualquier mensaje (ej: `/start` o `Hola`)
4. Visita: `https://api.telegram.org/bot<TOKEN>/getUpdates`
5. Busca `"chat":{"id":` en la respuesta
6. **Copia el número** que aparece después de `"id":`

### Paso 3: Agregar al .env

Abre tu archivo `.env` y agrega:

```env
# Telegram Bot (GRATIS - Alternativa a SMS/WhatsApp)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

**Reemplaza:**
- `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` con tu TOKEN real
- `123456789` con tu Chat ID real

---

## ✅ Verificar Configuración

Ejecuta en la terminal:

```bash
python manage.py shell
```

Luego ejecuta:

```python
from notificaciones.services import NotificationService
from decouple import config

token = config('TELEGRAM_BOT_TOKEN', default='')
chat_id = config('TELEGRAM_CHAT_ID', default='')

print(f"Token configurado: {'✅ Sí' if token else '❌ No'}")
print(f"Chat ID configurado: {'✅ Sí' if chat_id else '❌ No'}")

# Probar envío
if token and chat_id:
    result = NotificationService._send_sms_telegram('+521234567890', 'Test de notificación')
    print(f"Resultado: {result}")
```

---

## 🎯 ¿Cómo Funciona?

Una vez configurado:

1. **SMS/WhatsApp sin Twilio:**
   - El sistema intenta usar Twilio primero
   - Si Twilio no está configurado, usa Telegram automáticamente
   - Los mensajes llegan a tu Chat ID de Telegram

2. **Formato de mensajes:**
   - SMS: `📱 SMS para +521234567890: [mensaje]`
   - WhatsApp: `💬 WhatsApp para +521234567890: [mensaje]`

3. **Para enviar a otros usuarios:**
   - Necesitas su Chat ID
   - O crear un grupo y agregar el bot al grupo

---

## 💡 Tips

- **Grupo de notificaciones:** Crea un grupo en Telegram, agrega el bot, y usa el Chat ID del grupo
- **Múltiples usuarios:** Puedes crear un grupo y agregar a todos los que necesiten recibir notificaciones
- **Privacidad:** El bot solo puede enviar mensajes a usuarios que hayan iniciado conversación con él

---

## ❓ Problemas Comunes

**Error: "Telegram no está configurado"**
- Verifica que `TELEGRAM_BOT_TOKEN` esté en `.env`
- Reinicia el servidor Django

**Error: "Chat ID no válido"**
- Asegúrate de haber iniciado conversación con el bot
- Verifica que el Chat ID sea numérico

**No recibo mensajes:**
- Verifica que hayas iniciado conversación con el bot
- Revisa que el Chat ID sea correcto
- Verifica los logs del servidor

---

## 🎉 ¡Listo!

Una vez configurado, el sistema usará Telegram automáticamente para SMS/WhatsApp cuando Twilio no esté disponible.

**¡Es 100% gratis e ilimitado!** 🚀

