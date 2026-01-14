# Revisión de Congruencia: Usuarios, Permisos, Grupos y Roles

## Resumen Ejecutivo

Este documento analiza la congruencia entre los diferentes sistemas de autenticación y autorización en el proyecto AdminiRed.

## Sistemas Identificados

### 1. Sistema Custom de Roles y Permisos (PRINCIPAL)
- **Ubicación**: `core/models.py` - Modelos `Rol`, `Permiso`, `UsuarioRol`, `PermisoRol`
- **Decoradores**: `@permiso_required`, `@rol_required`, `@permisos_required` (en `core/roles_decorators.py`)
- **Utilidades**: `core/roles_utils.py`
- **Estado**: ✅ Sistema principal y bien implementado

### 2. Sistema de Usuarios Cliente (SEPARADO)
- **Identificación**: Usuarios con `cliente_perfil` (relación OneToOne con `Cliente`)
- **Decorador**: `@cliente_required` (en `clientes/portal_views.py`)
- **Rol**: Los clientes deberían tener el rol "Cliente" asignado automáticamente
- **Estado**: ⚠️ Necesita revisión

### 3. Django Groups (NO USADO)
- **Estado**: ✅ No se está usando Django Groups - Correcto

### 4. Django Permissions (LIMITADO)
- **Uso**: Solo para el admin de Django (`is_staff`, `is_superuser`)
- **Estado**: ✅ Uso limitado y correcto

## Problemas Identificados

### PROBLEMA 1: Mezcla de Sistemas de Protección
**Ubicación**: `pagos/views.py` (líneas 714, 872, 1259)
**Descripción**: Se usa `is_staff` en lugar de decoradores de permisos custom
```python
elif not request.user.is_staff:  # ❌ INCORRECTO
```

**Solución**: Debe usar `@permiso_required` o verificar permisos custom

### PROBLEMA 2: Vistas sin Protección de Permisos
**Ubicación**: Múltiples vistas en `clientes/views.py`, `pagos/views.py`, etc.
**Descripción**: Las vistas solo tienen `@login_required` pero no verifican permisos específicos
**Ejemplo**: `cliente_list`, `cliente_create`, `pago_list`, etc.

**Solución**: Agregar `@permiso_required` apropiado según la acción

### PROBLEMA 3: Inconsistencia en Protección
- Algunas vistas usan `@permiso_required` (ej: `roles_views.py`)
- Otras solo usan `@login_required` (ej: `clientes/views.py`, `pagos/views.py`)
- Algunas verifican `is_staff` manualmente

## Recomendaciones

### Recomendación 1: Estandarizar Protección de Vistas
Todas las vistas del admin deben usar el sistema custom de permisos:

```python
# ✅ CORRECTO
@login_required
@permiso_required('ver_clientes')
def cliente_list(request):
    ...

# ✅ CORRECTO
@login_required
@permiso_required('crear_clientes')
def cliente_create(request):
    ...

# ❌ INCORRECTO
@login_required
def cliente_list(request):
    if not request.user.is_staff:  # NO USAR
        ...
```

### Recomendación 2: Usuarios Cliente
- Los usuarios cliente NO deben acceder a vistas del admin
- Deben usar el portal de clientes (`/clientes/portal/`)
- El decorador `@cliente_required` es correcto
- Los clientes DEBEN tener el rol "Cliente" asignado

### Recomendación 3: Superusuarios
- Los superusuarios (`is_superuser=True`) tienen todos los permisos
- Esto está implementado correctamente en `roles_utils.py`
- Mantener esta funcionalidad

## Plan de Acción

1. ✅ Crear rol "Cliente" (YA HECHO)
2. ⏳ Asignar rol "Cliente" automáticamente (YA HECHO)
3. ⏳ Reemplazar `is_staff` por `@permiso_required` en `pagos/views.py`
4. ⏳ Agregar `@permiso_required` a todas las vistas del admin
5. ⏳ Verificar que los clientes no puedan acceder al admin
6. ⏳ Documentar el sistema de permisos

## Archivos a Modificar

### Alta Prioridad
1. `pagos/views.py` - Reemplazar `is_staff` por permisos custom
2. `clientes/views.py` - Agregar `@permiso_required` a todas las vistas
3. `instalaciones/views.py` - Revisar y agregar permisos
4. `inventario/views.py` - Revisar y agregar permisos
5. `notificaciones/views.py` - Revisar y agregar permisos

### Media Prioridad
6. `core/views.py` - Revisar `home` y otras vistas
7. Verificar templates que usan `user.is_staff` o `user.is_superuser`

