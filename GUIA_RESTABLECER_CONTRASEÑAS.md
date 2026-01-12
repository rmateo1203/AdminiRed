# 🔑 Guía: Restablecer Contraseñas desde el Administrador

## ✅ Respuesta Corta

**SÍ, ahora el sistema tiene una herramienta para restablecer contraseñas desde el administrador.**

Se ha agregado una nueva acción en el Admin de Django llamada **"🔑 Restablecer contraseña del portal"** que permite a los administradores resetear las contraseñas de los clientes que tienen acceso al portal.

## 🔧 Cómo Usar la Herramienta

### Paso 1: Acceder al Admin de Django
1. Iniciar sesión en el Admin de Django: `http://localhost:8000/admin/`
2. Ir a la sección **"CLIENTES"** → **"Clientes"**

### Paso 2: Seleccionar los Clientes
1. Buscar los clientes cuyas contraseñas deseas restablecer
2. Usar el buscador o filtros para encontrar los clientes
3. Seleccionar los checkboxes de los clientes (puedes seleccionar múltiples)

### Paso 3: Usar la Acción de Restablecer Contraseña
1. En el menú desplegable **"Acción"** (parte superior de la lista)
2. Seleccionar **"🔑 Restablecer contraseña del portal"**
3. Hacer clic en el botón **"Ir"**

### Paso 4: Verificar los Resultados
- El sistema generará una nueva contraseña automáticamente para cada cliente seleccionado
- Se enviará un email a cada cliente con su nueva contraseña
- Verás mensajes de confirmación en la parte superior de la página

## 📋 Funcionalidades

### Lo que hace la herramienta:
1. ✅ **Genera una nueva contraseña automáticamente** (12 caracteres alfanuméricos)
2. ✅ **Restablece la contraseña** del usuario del portal
3. ✅ **Fuerza el cambio de contraseña** (el cliente deberá cambiarla en el próximo login)
4. ✅ **Envía un email automático** al cliente con:
   - Su nueva contraseña
   - Instrucciones para acceder al portal
   - Advertencia de seguridad
5. ✅ **Muestra mensajes informativos** sobre el proceso

### Requisitos:
- El cliente debe tener un **usuario del portal** creado
- El cliente debe tener un **email válido** configurado
- El sistema de email debe estar configurado correctamente

## ⚠️ Casos Especiales

### Cliente sin Usuario del Portal
Si intentas restablecer la contraseña de un cliente que no tiene usuario:
- **Se valida automáticamente** antes de procesar
- Se muestra un mensaje de advertencia con el nombre del cliente
- El sistema **omite** a esos clientes y continúa con los que sí tienen usuario
- Necesitas crear primero el usuario usando la acción **"🔐 Crear usuario para portal"**
- Ejemplo de mensaje:
  - Un cliente: `⚠️ El cliente "Juan Pérez" no tiene usuario del portal. Crea un usuario primero usando la acción "🔐 Crear usuario para portal".`
  - Múltiples clientes: `⚠️ 3 cliente(s) no tienen usuario del portal: Juan Pérez, María García, Carlos López. Crea usuarios primero usando la acción "🔐 Crear usuario para portal".`

### Error al Enviar Email
Si el sistema no puede enviar el email:
- Se mostrará un mensaje con la nueva contraseña
- Deberás comunicar manualmente la contraseña al cliente
- El mensaje incluirá: `Usuario: [username], Nueva Contraseña: [password]`

### Múltiples Clientes Seleccionados
- Puedes seleccionar múltiples clientes y restablecer todas sus contraseñas a la vez
- Cada cliente recibirá su propia contraseña única
- Verás un mensaje resumen al final

## 🔐 Otras Herramientas Relacionadas

### 1. Forzar Cambio de Contraseña
- **Acción:** "🔒 Forzar cambio de contraseña"
- **Función:** Marca a los clientes para que deban cambiar su contraseña en el próximo login
- **Diferencia:** NO genera una nueva contraseña, solo fuerza el cambio

### 2. Crear Usuario para Portal
- **Acción:** "🔐 Crear usuario para portal"
- **Función:** Crea un nuevo usuario del portal para clientes que no lo tienen
- **Cuando usar:** Antes de restablecer contraseñas para clientes sin usuario

### 3. Restablecimiento de Contraseña por el Cliente
- **URL:** `/password-reset/`
- **Función:** Los clientes pueden solicitar restablecer su propia contraseña
- **Requiere:** Email configurado y sistema de email funcionando

## 📝 Ejemplo de Uso

**Escenario:** Un cliente olvidó su contraseña y solicita ayuda al administrador.

1. **Ir al Admin:** `http://localhost:8000/admin/clientes/cliente/`
2. **Buscar el cliente:** Usar el buscador con el nombre, email o teléfono
3. **Seleccionar el cliente:** Marcar el checkbox del cliente
4. **Ejecutar acción:**
   - Seleccionar "🔑 Restablecer contraseña del portal" en el menú "Acción"
   - Hacer clic en "Ir"
5. **Verificar resultado:**
   - Mensaje: "✅ Contraseña restablecida para [Cliente]. Se ha enviado un email a [email] con la nueva contraseña."
6. **Informar al cliente:**
   - El cliente recibirá un email automáticamente
   - Si no recibe el email, comunicar manualmente la contraseña (mostrada en el mensaje)

## 🔒 Seguridad

### Buenas Prácticas:
1. ✅ **Solo administradores** pueden usar esta herramienta
2. ✅ Las contraseñas se generan de forma **segura y aleatoria**
3. ✅ Se **fuerza el cambio** de contraseña en el próximo login
4. ✅ Se envía un **email de notificación** al cliente
5. ✅ Las contraseñas antiguas quedan **invalidadas inmediatamente**

### Consideraciones:
- ⚠️ Si el email no se puede enviar, el administrador verá la nueva contraseña en pantalla
- ⚠️ El administrador debe comunicar manualmente la contraseña al cliente en ese caso
- ⚠️ Las contraseñas generadas son temporales (el cliente deberá cambiarlas)

## 🚀 Comparación con Otras Opciones

| Característica | Restablecer desde Admin | Forzar Cambio | Cliente Solicita Reset |
|----------------|-------------------------|---------------|------------------------|
| Genera nueva contraseña | ✅ Sí | ❌ No | ✅ Sí (vía email) |
| Envía email automático | ✅ Sí | ❌ No | ✅ Sí |
| Fuerza cambio en login | ✅ Sí | ✅ Sí | ❌ No |
| Requiere usuario existente | ✅ Sí | ❌ No | ✅ Sí |
| Requiere email configurado | ✅ Sí | ❌ No | ✅ Sí |

## ✅ Resumen

**SÍ, el sistema ahora tiene una herramienta completa para restablecer contraseñas desde el administrador:**

- ✅ Acción disponible en el Admin de Django
- ✅ Genera contraseñas seguras automáticamente
- ✅ Envía emails a los clientes
- ✅ Fuerza cambio de contraseña
- ✅ Soporta múltiples clientes a la vez
- ✅ Maneja errores y casos especiales
- ✅ Muestra mensajes informativos

**Ubicación:** Admin de Django → CLIENTES → Clientes → Acción → "🔑 Restablecer contraseña del portal"

