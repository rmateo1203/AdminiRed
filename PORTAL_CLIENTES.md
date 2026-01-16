# 🎯 Portal de Clientes - Documentación

## 📋 Resumen

Se ha implementado un **Portal de Clientes** completo que permite a los clientes:
- ✅ Registrarse en el sistema
- ✅ Iniciar sesión con sus credenciales
- ✅ Ver solo sus propios pagos y servicios activos
- ✅ Realizar pagos en línea
- ✅ Gestionar su perfil

## 🔐 Autenticación

### Modelo Cliente

Se agregó un campo `usuario` (OneToOneField) al modelo `Cliente` que vincula cada cliente con un usuario del sistema Django:

```python
usuario = models.OneToOneField(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='cliente_perfil',
    verbose_name='Usuario del sistema'
)
```

### Creación de Usuario

El método `crear_usuario_portal()` crea automáticamente un usuario cuando:
- Un cliente se registra desde el portal
- Un administrador crea un usuario para un cliente existente

**Características:**
- Username basado en email o teléfono
- Contraseña generada automáticamente o proporcionada
- `is_staff=False` (no accede al admin)
- `is_superuser=False`

## 🛣️ URLs del Portal

### Registro y Login
- `/clientes/portal/registro/` - Registro de nuevos clientes
- `/clientes/portal/login/` - Login para clientes

### Dashboard y Navegación
- `/clientes/portal/` - Dashboard principal
- `/clientes/portal/mis-pagos/` - Lista de pagos del cliente
- `/clientes/portal/mis-pagos/<pago_id>/` - Detalle de un pago
- `/clientes/portal/mis-servicios/` - Lista de servicios/instalaciones
- `/clientes/portal/perfil/` - Perfil del cliente (editable)
- `/clientes/portal/cambiar-password/` - Cambiar contraseña

## 🔒 Seguridad y Permisos

### Decorador `@cliente_required`

Todas las vistas del portal están protegidas con el decorador `@cliente_required` que:
1. Verifica que el usuario esté autenticado
2. Verifica que el usuario tenga un perfil de cliente asociado
3. Verifica que el cliente esté activo y no eliminado
4. Pasa el objeto `cliente` a la vista

### Restricciones de Acceso

- Los clientes **solo pueden ver sus propios datos**
- No pueden acceder al admin de Django
- No pueden ver datos de otros clientes
- Las vistas de pago verifican que el pago pertenezca al cliente

## 📱 Funcionalidades

### Dashboard
- Estadísticas de pagos (pendientes, vencidos, pagados)
- Monto pendiente total
- Servicios activos
- Próximos pagos (próximos 30 días)
- Acciones rápidas

### Mis Pagos
- Lista filtrable de todos los pagos del cliente
- Búsqueda por concepto, referencia, etc.
- Filtro por estado
- Paginación
- Acceso directo a detalle y pago en línea

### Detalle de Pago
- Información completa del pago
- Historial de transacciones
- Botón para pagar en línea (si está pendiente/vencido)
- Integración con pasarelas de pago (Stripe, Mercado Pago, PayPal)

### Mis Servicios
- Lista de todas las instalaciones del cliente
- Filtro por estado
- Información detallada de cada servicio
- Tarjetas visuales con estado

### Perfil
- Edición de datos de contacto (email, teléfono, dirección)
- Información de cuenta (usuario, estado, fecha de registro)
- Acceso a cambio de contraseña

### Cambiar Contraseña
- Validación de contraseña actual
- Validación de nueva contraseña (mínimo 8 caracteres)
- Confirmación de contraseña

## 🎨 Templates

Todos los templates están en `clientes/templates/clientes/portal_*.html`:

- `portal_login.html` - Página de login
- `portal_registro.html` - Página de registro
- `portal_base.html` - Template base con sidebar
- `portal_dashboard.html` - Dashboard principal
- `portal_mis_pagos.html` - Lista de pagos
- `portal_detalle_pago.html` - Detalle de pago
- `portal_mis_servicios.html` - Lista de servicios
- `portal_perfil.html` - Perfil del cliente
- `portal_cambiar_password.html` - Cambiar contraseña

## 🔄 Flujo de Registro

1. Cliente accede a `/clientes/portal/registro/`
2. Completa el formulario con sus datos
3. El sistema crea:
   - Registro de `Cliente`
   - Usuario de Django vinculado
   - Inicia sesión automáticamente
4. Redirige al dashboard

## 🔄 Flujo de Pago

1. Cliente ve sus pagos en "Mis Pagos"
2. Hace clic en un pago pendiente/vencido
3. Ve el detalle y hace clic en "Pagar en Línea"
4. Selecciona la pasarela (Stripe, Mercado Pago, PayPal)
5. Completa el pago en la pasarela
6. Regresa al sistema con confirmación
7. El pago se marca como pagado automáticamente

## 🛠️ Integración con Pagos

Las vistas de pago (`pago_procesar_online`, `pago_exitoso`, `pago_cancelado`) han sido modificadas para:
- Permitir acceso a clientes (no solo staff)
- Verificar que el pago pertenezca al cliente
- Redirigir correctamente según el tipo de usuario

## 📝 Notas para Administradores

### Crear Usuario para Cliente Existente

Desde el admin de Django:
1. Editar el cliente
2. En la sección "Portal de Cliente", asignar un usuario
3. O usar el método `crear_usuario_portal()` desde el shell:

```python
from clientes.models import Cliente

cliente = Cliente.objects.get(pk=1)
usuario = cliente.crear_usuario_portal(password='contraseña_segura')
```

### Desactivar Acceso de Cliente

- Cambiar `estado_cliente` a 'inactivo', 'suspendido' o 'cancelado'
- O eliminar el usuario asociado
- O hacer soft delete del cliente

## ✅ Checklist de Implementación

- [x] Modelo Cliente con campo `usuario`
- [x] Método `crear_usuario_portal()`
- [x] Vistas de registro y login
- [x] Vistas del portal (dashboard, pagos, servicios, perfil)
- [x] Decorador `@cliente_required`
- [x] Templates del portal
- [x] URLs configuradas
- [x] Integración con pasarelas de pago
- [x] Restricciones de acceso
- [x] Migración de base de datos

## 🚀 Próximos Pasos (Opcionales)

- [ ] Recuperación de contraseña para clientes
- [ ] Notificaciones por email al cliente
- [ ] Historial de pagos más detallado
- [ ] Facturas descargables
- [ ] Soporte/tickets para clientes
- [ ] Dashboard con gráficos

---

**¡Portal de Clientes implementado exitosamente!** 🎉










