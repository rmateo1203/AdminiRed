# 📧 Sistema de Recordatorios Automáticos de Pagos

## 📋 Descripción

Sistema completo para enviar recordatorios automáticos de pagos pendientes y vencidos a los clientes. Incluye plantillas HTML profesionales, configuración flexible y seguimiento de recordatorios enviados.

---

## ✨ Funcionalidades

### 1. Recordatorios Antes de Vencimiento
- Envío automático X días antes de la fecha de vencimiento
- Configurable (por defecto: 3 días)
- Plantilla HTML profesional
- Evita duplicados (no envía si ya se envió en los últimos 2 días)

### 2. Recordatorios de Pagos Vencidos
- Envío automático X días después del vencimiento
- Configurable (por defecto: 1 día)
- Plantilla HTML con alerta urgente
- Evita duplicados (no envía si ya se envió en los últimos 7 días)

### 3. Plantillas HTML Profesionales
- Diseño responsive
- Colores diferenciados (azul para recordatorios, rojo para vencidos)
- Información completa del pago
- Mensajes claros y profesionales

### 4. Configuración Flexible
- Configuración por tipo de notificación
- Días antes/después configurables
- Canal preferido (email, SMS, WhatsApp)
- Activación/desactivación por tipo

---

## 🚀 Uso

### Comando Principal

```bash
# Enviar recordatorios con valores por defecto (3 días antes, 1 día después)
python manage.py enviar_recordatorios_pagos

# Personalizar días antes del vencimiento
python manage.py enviar_recordatorios_pagos --dias-antes 5

# Personalizar días después del vencimiento
python manage.py enviar_recordatorios_pagos --dias-despues 2

# Solo recordatorios de pagos vencidos
python manage.py enviar_recordatorios_pagos --solo-vencidos

# Solo recordatorios antes de vencimiento
python manage.py enviar_recordatorios_pagos --solo-pendientes

# Modo dry-run (simular sin crear notificaciones)
python manage.py enviar_recordatorios_pagos --dry-run

# Forzar envío incluso si ya se envió recientemente
python manage.py enviar_recordatorios_pagos --forzar
```

### Enviar Notificaciones Creadas

Después de crear los recordatorios, deben enviarse usando el comando de notificaciones:

```bash
# Enviar todas las notificaciones pendientes
python manage.py send_notifications

# Con límite
python manage.py send_notifications --limit 100

# Modo dry-run
python manage.py send_notifications --dry-run
```

---

## ⚙️ Configuración

### 1. Configurar Tipos de Notificación

Los tipos de notificación se crean automáticamente al ejecutar el comando por primera vez:

- **Recordatorio de Pago (Antes de Vencimiento)**: `recordatorio_pago_antes`
- **Recordatorio de Pago Vencido**: `recordatorio_pago_vencido`

### 2. Configurar Recordatorios en Admin

1. Ir a Django Admin → Notificaciones → Configuraciones de Notificación
2. Crear o editar configuración para cada tipo:
   - **Días antes del vencimiento**: Días antes de enviar recordatorio (default: 3)
   - **Días después del vencimiento**: Días después para enviar recordatorio (default: 1)
   - **Canal preferido**: Email, SMS, WhatsApp o Sistema
   - **Activa**: Activar/desactivar esta configuración

### 3. Configurar Email

Asegúrate de tener configurado el email en `.env`:

```env
DEFAULT_FROM_EMAIL=noreply@adminired.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password
```

---

## 📅 Programación Automática (Cron)

Para ejecutar automáticamente todos los días:

### Linux/Mac (Crontab)

```bash
# Editar crontab
crontab -e

# Agregar estas líneas (ejecutar diariamente a las 8:00 AM)
0 8 * * * cd /ruta/a/tu/proyecto && source venv/bin/activate && python manage.py enviar_recordatorios_pagos
0 9 * * * cd /ruta/a/tu/proyecto && source venv/bin/activate && python manage.py send_notifications
```

### Windows (Task Scheduler)

1. Abrir "Programador de tareas"
2. Crear tarea básica
3. Configurar:
   - **Nombre**: Recordatorios de Pagos
   - **Desencadenador**: Diariamente a las 8:00 AM
   - **Acción**: Ejecutar programa
   - **Programa**: `python`
   - **Argumentos**: `manage.py enviar_recordatorios_pagos`
   - **Iniciar en**: Ruta del proyecto

---

## 📊 Estructura del Sistema

### Archivos Creados

```
pagos/
├── management/
│   └── commands/
│       └── enviar_recordatorios_pagos.py  # Comando principal
├── services.py                            # Servicio de recordatorios
└── templates/
    └── pagos/
        └── emails/
            ├── recordatorio_antes_vencimiento.html
            └── recordatorio_vencido.html
```

### Modelos Utilizados

- **Pago**: Modelo de pagos
- **Notificacion**: Modelo de notificaciones
- **TipoNotificacion**: Tipos de notificaciones
- **ConfiguracionNotificacion**: Configuración de recordatorios

---

## 🔍 Flujo de Trabajo

1. **Crear Recordatorios**: Ejecutar `enviar_recordatorios_pagos`
   - Busca pagos pendientes que vencen en X días
   - Busca pagos vencidos desde hace X días
   - Crea notificaciones en estado "pendiente"

2. **Enviar Notificaciones**: Ejecutar `send_notifications`
   - Procesa notificaciones pendientes
   - Envía por el canal configurado (email, SMS, WhatsApp)
   - Marca como "enviada" o "fallida"

3. **Seguimiento**: Ver en Django Admin
   - Notificaciones → Notificaciones
   - Filtrar por tipo, estado, cliente, etc.

---

## 📧 Plantillas de Email

### Recordatorio Antes de Vencimiento

- **Color**: Azul/Púrpura (gradiente)
- **Tono**: Informativo y amigable
- **Contenido**:
  - Detalles del pago
  - Días restantes
  - Recordatorio amigable

### Recordatorio de Pago Vencido

- **Color**: Rojo (alerta)
- **Tono**: Urgente pero profesional
- **Contenido**:
  - Detalles del pago
  - Días vencido
  - Advertencia de consecuencias
  - Llamado a la acción

---

## 🛠️ Personalización

### Modificar Plantillas HTML

Editar archivos en `pagos/templates/pagos/emails/`:
- `recordatorio_antes_vencimiento.html`
- `recordatorio_vencido.html`

### Modificar Mensajes

Editar métodos en `pagos/services.py`:
- `_generar_mensaje_antes_vencimiento()`
- `_generar_mensaje_vencido()`

### Agregar Nuevos Tipos de Recordatorios

1. Crear nuevo `TipoNotificacion` en Django Admin
2. Crear `ConfiguracionNotificacion` para el tipo
3. Agregar lógica en `enviar_recordatorios_pagos.py`

---

## 📈 Estadísticas y Reportes

### Ver Recordatorios Enviados

```python
from notificaciones.models import Notificacion, TipoNotificacion

# Recordatorios antes de vencimiento
tipo_antes = TipoNotificacion.objects.get(codigo='recordatorio_pago_antes')
recordatorios_antes = Notificacion.objects.filter(tipo=tipo_antes, estado='enviada')

# Recordatorios de vencidos
tipo_vencido = TipoNotificacion.objects.get(codigo='recordatorio_pago_vencido')
recordatorios_vencidos = Notificacion.objects.filter(tipo=tipo_vencido, estado='enviada')
```

---

## ⚠️ Consideraciones

1. **Email Requerido**: Solo se envían recordatorios a clientes con email configurado
2. **Evitar Duplicados**: El sistema evita enviar recordatorios duplicados recientes
3. **Pagos Pagados**: No se envían recordatorios de pagos ya pagados
4. **Configuración**: Los valores por defecto pueden sobrescribirse en Django Admin

---

## 🐛 Solución de Problemas

### No se crean recordatorios

- Verificar que los clientes tengan email configurado
- Verificar que los pagos no estén pagados
- Verificar fechas de vencimiento

### No se envían emails

- Verificar configuración de email en `.env`
- Verificar que `send_notifications` se ejecute después de crear recordatorios
- Revisar logs de Django

### Recordatorios duplicados

- Usar `--forzar` solo cuando sea necesario
- Verificar configuración de días antes/después

---

## 📝 Ejemplos de Uso

### Ejemplo 1: Recordatorios Diarios

```bash
# Crear recordatorios (ejecutar diariamente a las 8:00 AM)
python manage.py enviar_recordatorios_pagos

# Enviar notificaciones (ejecutar diariamente a las 9:00 AM)
python manage.py send_notifications
```

### Ejemplo 2: Recordatorios Personalizados

```bash
# Recordatorios 5 días antes, 2 días después
python manage.py enviar_recordatorios_pagos --dias-antes 5 --dias-despues 2
```

### Ejemplo 3: Solo Pagos Vencidos

```bash
# Solo recordatorios de pagos vencidos
python manage.py enviar_recordatorios_pagos --solo-vencidos
```

---

## ✅ Checklist de Implementación

- [x] Comando Django para crear recordatorios
- [x] Servicio de recordatorios
- [x] Plantillas HTML profesionales
- [x] Integración con sistema de notificaciones
- [x] Configuración flexible
- [x] Prevención de duplicados
- [x] Documentación completa

---

*Sistema implementado: Diciembre 2024*  
*Versión: 1.0*


