# 🔐 Guía: Cómo Dar Acceso a Clientes al Portal

## 📋 Resumen

Existen **3 formas principales** de dar acceso a los clientes al portal:

1. **Registro automático** - El cliente se registra desde el portal público
2. **Desde el Admin de Django** - El administrador crea/asigna el usuario
3. **Programáticamente** - Desde el shell de Django o scripts

---

## 🌐 Método 1: Registro Automático (Recomendado)

### ¿Cómo funciona?

El cliente accede a `/clientes/portal/registro/` y completa el formulario. El sistema automáticamente:
- Crea el registro de `Cliente`
- Crea el usuario de Django
- Vincula el usuario con el cliente
- Inicia sesión automáticamente

### Ventajas:
- ✅ No requiere intervención del administrador
- ✅ El cliente elige su propia contraseña
- ✅ Proceso rápido y sencillo

### Pasos para el cliente:
1. Ir a: `http://tudominio.com/clientes/portal/registro/`
2. Completar el formulario con sus datos
3. Crear contraseña
4. ¡Listo! Ya tiene acceso

---

## 👨‍💼 Método 2: Desde el Admin de Django

### Opción A: Asignar Usuario Existente

Si ya existe un usuario en el sistema:

1. **Ir al Admin de Django**: `/admin/`
2. **Clientes** → Seleccionar el cliente
3. En la sección **"Portal de Cliente"**, seleccionar un usuario existente del dropdown
4. **Guardar**

### Opción B: Crear Usuario Nuevo y Asignarlo

1. **Crear el usuario primero**:
   - Ir a **Usuarios** → **Agregar usuario**
   - Completar: Username, Password, Email
   - ⚠️ **IMPORTANTE**: NO marcar "Es staff" ni "Es superusuario"
   - Guardar

2. **Asignar al cliente**:
   - Ir a **Clientes** → Seleccionar el cliente
   - En **"Portal de Cliente"**, seleccionar el usuario creado
   - Guardar

### ⚠️ Limitación Actual

Actualmente, el admin no tiene un botón para crear automáticamente el usuario. Se puede mejorar agregando una acción personalizada.

---

## 💻 Método 3: Programáticamente (Shell/Scripts)

### Desde el Shell de Django

```python
python manage.py shell
```

```python
from clientes.models import Cliente
from django.contrib.auth import get_user_model

User = get_user_model()

# Opción 1: Usar el método del modelo (RECOMENDADO)
cliente = Cliente.objects.get(pk=1)  # O usar email, teléfono, etc.
usuario = cliente.crear_usuario_portal(password='contraseña_segura123')
print(f'Usuario creado: {usuario.username}')
print(f'Contraseña: contraseña_segura123')

# Opción 2: Crear manualmente
cliente = Cliente.objects.get(email='cliente@ejemplo.com')
usuario = User.objects.create_user(
    username=cliente.email,
    email=cliente.email,
    password='contraseña_segura123',
    is_staff=False,
    is_superuser=False
)
cliente.usuario = usuario
cliente.save()
print(f'Usuario creado y asignado: {usuario.username}')
```

### Script para Crear Múltiples Usuarios

```python
# crear_usuarios_clientes.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from clientes.models import Cliente
import secrets
import string

def generar_contraseña():
    """Genera una contraseña aleatoria segura."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(12))

# Obtener clientes sin usuario
clientes_sin_usuario = Cliente.objects.filter(usuario__isnull=True, is_deleted=False)

print(f'Encontrados {clientes_sin_usuario.count()} clientes sin usuario')

for cliente in clientes_sin_usuario:
    try:
        password = generar_contraseña()
        usuario = cliente.crear_usuario_portal(password=password)
        print(f'✅ {cliente.nombre_completo}: {usuario.username} / {password}')
    except Exception as e:
        print(f'❌ Error con {cliente.nombre_completo}: {e}')
```

Ejecutar:
```bash
python crear_usuarios_clientes.py
```

---

## 🔧 Mejora: Agregar Acción en el Admin

Para facilitar la creación de usuarios desde el admin, podemos agregar una acción personalizada:

### Implementación

```python
# En clientes/admin.py

def crear_usuario_portal(self, request, queryset):
    """Acción para crear usuarios del portal para clientes seleccionados."""
    creados = 0
    errores = 0
    
    for cliente in queryset:
        if cliente.usuario:
            continue  # Ya tiene usuario
        
        try:
            import secrets
            import string
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(12))
            
            usuario = cliente.crear_usuario_portal(password=password)
            creados += 1
            self.message_user(
                request,
                f'Usuario creado para {cliente.nombre_completo}: {usuario.username} / Contraseña: {password}',
                level=messages.SUCCESS
            )
        except Exception as e:
            errores += 1
            self.message_user(
                request,
                f'Error al crear usuario para {cliente.nombre_completo}: {str(e)}',
                level=messages.ERROR
            )
    
    if creados > 0:
        self.message_user(
            request,
            f'{creados} usuario(s) creado(s) exitosamente.',
            level=messages.SUCCESS
        )

crear_usuario_portal.short_description = 'Crear usuario para portal (clientes seleccionados)'
```

Luego agregar a `actions`:
```python
actions = ['restaurar_clientes', 'eliminar_permanentemente', 'crear_usuario_portal']
```

---

## 📧 Enviar Credenciales al Cliente

### Opción 1: Manualmente

Después de crear el usuario, enviar las credenciales por:
- Email
- WhatsApp
- Teléfono
- Mensaje en el sistema

### Opción 2: Automático (Mejora Futura)

Se puede implementar un sistema que:
1. Crea el usuario
2. Genera un email con las credenciales
3. Envía el email automáticamente al cliente

---

## ✅ Verificar Acceso

### Desde el Admin

1. Ir a **Clientes** → Seleccionar cliente
2. Verificar que en **"Portal de Cliente"** hay un usuario asignado
3. Verificar que el usuario NO es staff ni superusuario

### Desde el Shell

```python
from clientes.models import Cliente

cliente = Cliente.objects.get(pk=1)
print(f'Tiene acceso: {cliente.tiene_acceso_portal}')
print(f'Usuario: {cliente.usuario.username if cliente.usuario else "No asignado"}')
```

### Probar Login

1. Ir a: `/clientes/portal/login/`
2. Usar el username (generalmente el email)
3. Usar la contraseña asignada
4. Debería iniciar sesión y ver el dashboard

---

## 🔒 Seguridad

### Buenas Prácticas

1. **Contraseñas seguras**: Mínimo 8 caracteres, usar generador automático
2. **No compartir credenciales**: Cada cliente debe tener su propio usuario
3. **Cambio de contraseña**: Los clientes pueden cambiar su contraseña desde el portal
4. **Desactivar acceso**: Cambiar `estado_cliente` a 'inactivo' o eliminar el usuario

### Desactivar Acceso

```python
# Opción 1: Cambiar estado del cliente
cliente.estado_cliente = 'inactivo'
cliente.save()

# Opción 2: Desactivar usuario
cliente.usuario.is_active = False
cliente.usuario.save()

# Opción 3: Eliminar usuario (soft)
cliente.usuario = None
cliente.save()
```

---

## 🎯 Resumen Rápido

### Para Clientes Nuevos:
1. **Registro automático**: `/clientes/portal/registro/`
2. **O desde admin**: Crear cliente → Asignar/Crear usuario

### Para Clientes Existentes:
1. **Desde admin**: Cliente → Portal de Cliente → Seleccionar/Crear usuario
2. **Desde shell**: `cliente.crear_usuario_portal(password='...')`

### Verificar:
- Cliente tiene `usuario` asignado
- Usuario NO es staff
- Cliente puede hacer login en `/clientes/portal/login/`

---

## 📝 Notas Importantes

- ⚠️ El username generalmente es el email del cliente
- ⚠️ Si el email no es único, se genera un username alternativo
- ⚠️ Los clientes NO pueden acceder al admin (`/admin/`)
- ⚠️ Solo ven sus propios datos (pagos, servicios)
- ✅ Pueden cambiar su contraseña desde el portal
- ✅ Pueden actualizar algunos datos de su perfil

---

**¡Listo!** Ahora sabes cómo dar acceso a los clientes al portal. 🎉

