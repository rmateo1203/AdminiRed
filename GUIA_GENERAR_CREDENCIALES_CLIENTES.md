# 🔐 Guía Práctica: Generar y Enviar Credenciales a Clientes

## 📋 Resumen

Esta guía te muestra **cómo generar contraseñas y darlas a los clientes** para que puedan acceder al portal y pagar sus servicios.

---

## 🎯 Métodos Disponibles

### ✅ Método 1: Desde el Admin de Django (MÁS FÁCIL)

#### Para UN Cliente:

1. **Ir al Admin**: `/admin/clientes/cliente/`
2. **Seleccionar el cliente** (hacer clic en su nombre)
3. **En la sección "Portal de Cliente"**:
   - Si NO tiene usuario: Verás un campo vacío
   - **Opción A**: Crear usuario manualmente desde aquí (ver abajo)
   - **Opción B**: Usar la acción masiva (ver Método 2)

#### Para MÚLTIPLES Clientes:

1. **Ir al Admin**: `/admin/clientes/cliente/`
2. **Seleccionar los clientes** (marcar con checkbox)
3. **En "Acciones"** → Seleccionar: **"🔐 Crear usuario para portal (clientes seleccionados)"**
4. **Clic en "Ir"**
5. **Verás mensajes** con las credenciales de cada cliente:
   ```
   ✅ Usuario creado para Juan Pérez: juan@ejemplo.com | Contraseña: aB3xK9mP2qR7
   ✅ Usuario creado para María García: maria@ejemplo.com | Contraseña: mN8pQ4rT6vW2
   ```
6. **Copiar las credenciales** y enviarlas a los clientes

---

### ✅ Método 2: Script Automatizado

#### Ejecutar el Script:

```bash
cd /home/rmateo/Documentos/otros/project/django/AdminiRed
source venv/bin/activate
python crear_usuarios_clientes.py
```

#### El Script:

1. Busca clientes sin usuario
2. Muestra cuántos encontró
3. Pide confirmación
4. Crea usuarios con contraseñas seguras
5. **Guarda las credenciales en `credenciales_clientes.txt`**

#### Ejemplo de Salida:

```
======================================================================
🔐 CREACIÓN DE USUARIOS PARA PORTAL DE CLIENTES
======================================================================

📊 Encontrados 5 cliente(s) sin usuario

¿Deseas crear usuarios para estos 5 cliente(s)? (s/n): s

Creando usuarios...
----------------------------------------------------------------------
✅ Juan Pérez
   Username: juan@ejemplo.com
   Contraseña: aB3xK9mP2qR7

✅ María García
   Username: maria@ejemplo.com
   Contraseña: mN8pQ4rT6vW2

...

======================================================================
📊 RESUMEN
======================================================================
✅ Usuarios creados: 5
❌ Errores: 0

💾 Credenciales guardadas en: credenciales_clientes.txt
⚠️  IMPORTANTE: Envía estas credenciales a los clientes de forma segura.
```

#### Archivo Generado: `credenciales_clientes.txt`

```
======================================================================
CREDENCIALES DE ACCESO AL PORTAL
======================================================================

Cliente: Juan Pérez
Email: juan@ejemplo.com
Teléfono: 9931234567
Username: juan@ejemplo.com
Contraseña: aB3xK9mP2qR7
----------------------------------------------------------------------

Cliente: María García
Email: maria@ejemplo.com
Teléfono: 9937654321
Username: maria@ejemplo.com
Contraseña: mN8pQ4rT6vW2
----------------------------------------------------------------------
```

---

### ✅ Método 3: Desde el Shell de Django

#### Para UN Cliente:

```bash
python manage.py shell
```

```python
from clientes.models import Cliente

# Buscar el cliente
cliente = Cliente.objects.get(email='cliente@ejemplo.com')
# O por teléfono: Cliente.objects.get(telefono='9931234567')
# O por ID: Cliente.objects.get(pk=1)

# Crear usuario con contraseña personalizada
usuario = cliente.crear_usuario_portal(password='MiContraseña123')

print(f'✅ Usuario creado para: {cliente.nombre_completo}')
print(f'   Username: {usuario.username}')
print(f'   Contraseña: MiContraseña123')
print(f'   URL de acceso: http://tudominio.com/clientes/portal/login/')
```

#### Para MÚLTIPLES Clientes:

```python
from clientes.models import Cliente
import secrets
import string

def generar_contraseña():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(12))

# Obtener clientes sin usuario
clientes = Cliente.objects.filter(usuario__isnull=True, is_deleted=False)

for cliente in clientes:
    password = generar_contraseña()
    usuario = cliente.crear_usuario_portal(password=password)
    print(f'{cliente.nombre_completo}: {usuario.username} / {password}')
```

---

## 📧 Cómo Enviar las Credenciales a los Clientes

### Opción 1: Email (Recomendado)

#### Manualmente:

1. **Copiar las credenciales** del admin o del archivo generado
2. **Enviar email** al cliente con:
   ```
   Asunto: Acceso al Portal de Cliente - AdminiRed
   
   Hola [Nombre del Cliente],
   
   Te hemos creado una cuenta para acceder a nuestro portal de clientes.
   
   Tus credenciales de acceso son:
   - Usuario: [username]
   - Contraseña: [contraseña]
   
   Puedes acceder en: http://tudominio.com/clientes/portal/login/
   
   Una vez dentro, podrás:
   - Ver tus pagos pendientes
   - Realizar pagos en línea
   - Ver tus servicios activos
   - Actualizar tu perfil
   
   Te recomendamos cambiar tu contraseña después del primer acceso.
   
   Saludos,
   Equipo AdminiRed
   ```

#### Automático (Mejora Futura):

Se puede implementar un sistema que envíe el email automáticamente al crear el usuario.

### Opción 2: WhatsApp

Enviar mensaje con:
```
Hola [Nombre], 

Tu acceso al portal está listo:
Usuario: [username]
Contraseña: [contraseña]

Accede en: http://tudominio.com/clientes/portal/login/

Puedes pagar tus servicios en línea desde ahí.
```

### Opción 3: Teléfono

Llamar al cliente y proporcionarle las credenciales verbalmente.

### Opción 4: Presencial

Si el cliente está en tu oficina, mostrarle las credenciales en pantalla o imprimirlas.

---

## 🔄 Flujo Completo Recomendado

### Paso 1: Crear el Cliente (si no existe)

1. Ir a `/admin/clientes/cliente/`
2. "Agregar cliente"
3. Completar datos
4. Guardar

### Paso 2: Generar Credenciales

**Opción A - Individual:**
1. Editar el cliente
2. En "Portal de Cliente" → Crear usuario (ver abajo)

**Opción B - Masivo:**
1. Seleccionar múltiples clientes
2. Acción → "Crear usuario para portal"
3. Copiar credenciales

### Paso 3: Enviar Credenciales

- Email (recomendado)
- WhatsApp
- Teléfono
- Presencial

### Paso 4: Cliente Accede

1. Cliente va a: `/clientes/portal/login/`
2. Ingresa username y contraseña
3. Ve su dashboard
4. Puede pagar sus servicios

---

## 🛠️ Mejora: Botón en el Detalle del Cliente

Para facilitar aún más, podemos agregar un botón en el detalle del cliente que:
1. Crea el usuario si no existe
2. Muestra las credenciales
3. Opción de enviar por email

¿Quieres que implemente esta mejora?

---

## 📝 Plantilla de Email

Puedes usar esta plantilla para enviar las credenciales:

```
Asunto: Acceso al Portal de Cliente - AdminiRed

Hola [NOMBRE_CLIENTE],

Te hemos creado una cuenta para acceder a nuestro portal de clientes.

🔐 TUS CREDENCIALES DE ACCESO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Usuario: [USERNAME]
Contraseña: [CONTRASEÑA]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 ACCEDER AL PORTAL:
http://tudominio.com/clientes/portal/login/

✨ LO QUE PUEDES HACER:
• Ver tus pagos pendientes
• Realizar pagos en línea (Stripe, Mercado Pago, PayPal)
• Ver tus servicios activos
• Actualizar tu información de contacto
• Cambiar tu contraseña

🔒 SEGURIDAD:
Te recomendamos cambiar tu contraseña después del primer acceso.

Si tienes alguna pregunta, no dudes en contactarnos.

Saludos,
Equipo AdminiRed
```

---

## ✅ Checklist para Dar Acceso

- [ ] Cliente existe en el sistema
- [ ] Cliente tiene email o teléfono
- [ ] Usuario creado (desde admin o script)
- [ ] Credenciales copiadas/guardadas
- [ ] Credenciales enviadas al cliente (email/WhatsApp/teléfono)
- [ ] Cliente puede hacer login
- [ ] Cliente puede ver sus pagos
- [ ] Cliente puede realizar pagos en línea

---

## 🎯 Resumen Rápido

### Para UN Cliente:
1. Admin → Cliente → Editar
2. Portal de Cliente → Crear usuario
3. Copiar credenciales
4. Enviar al cliente

### Para MÚLTIPLES Clientes:
1. Admin → Seleccionar clientes
2. Acción → "Crear usuario para portal"
3. Copiar credenciales de los mensajes
4. Enviar a cada cliente

### Script Automatizado:
```bash
python crear_usuarios_clientes.py
```
Las credenciales se guardan en `credenciales_clientes.txt`

---

**¡Listo!** Ahora puedes generar y enviar credenciales fácilmente. 🎉














