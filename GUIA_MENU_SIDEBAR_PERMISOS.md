# Guía: Menú Sidebar con Permisos por Rol

## ✅ Implementación Completada

El menú del sidebar ahora muestra automáticamente solo los módulos que el usuario puede ver según sus permisos.

## Cómo Funciona

### 1. Verificación por Módulo

El sistema usa el template tag `puede_ver_modulo` para verificar si el usuario tiene **al menos un permiso** de una categoría (módulo) específica:

```django
{% load roles_tags %}

{% if user|puede_ver_modulo:'clientes' %}
    <li><a href="{% url 'clientes:cliente_list' %}">Clientes</a></li>
{% endif %}
```

### 2. Verificación por Permiso Específico

Para elementos que requieren un permiso específico (no un módulo completo):

```django
{% if user|has_permiso:'gestionar_roles_permisos' or user.is_superuser %}
    <li><a href="{% url 'core:roles_dashboard' %}">Roles y Permisos</a></li>
{% endif %}
```

## Módulos Configurados en el Sidebar

### Módulo: Clientes
- **Verificación**: `user|puede_ver_modulo:'clientes'`
- **Se muestra si**: El usuario tiene al menos un permiso de la categoría `clientes`
- **Permisos relacionados**: `ver_clientes`, `crear_clientes`, `editar_clientes`, etc.

### Módulo: Instalaciones
- **Verificación**: `user|puede_ver_modulo:'instalaciones'`
- **Se muestra si**: El usuario tiene al menos un permiso de la categoría `instalaciones`
- **Permisos relacionados**: `ver_instalaciones`, `crear_instalaciones`, `editar_instalaciones`, etc.

### Módulo: Pagos
- **Verificación**: `user|puede_ver_modulo:'pagos'`
- **Se muestra si**: El usuario tiene al menos un permiso de la categoría `pagos`
- **Permisos relacionados**: `ver_pagos`, `crear_pagos`, `editar_pagos`, etc.

### Módulo: Inventario
- **Verificación**: `user|puede_ver_modulo:'inventario'`
- **Se muestra si**: El usuario tiene al menos un permiso de la categoría `inventario`
- **Permisos relacionados**: `ver_inventario`, `gestionar_inventario`, etc.

### Módulo: Notificaciones
- **Verificación**: `user|puede_ver_modulo:'notificaciones'`
- **Se muestra si**: El usuario tiene al menos un permiso de la categoría `notificaciones`
- **Permisos relacionados**: `ver_notificaciones`, `gestionar_notificaciones`, etc.

### Elementos Especiales

#### Catálogos
- **Verificación**: `user|has_permiso:'gestionar_roles_permisos' or user.is_superuser`
- **Se muestra si**: El usuario tiene permiso para gestionar roles/permisos o es superusuario

#### Roles y Permisos
- **Verificación**: `user|has_permiso:'gestionar_roles_permisos' or user.is_superuser`
- **Se muestra si**: El usuario tiene permiso para gestionar roles/permisos o es superusuario

#### Configuración
- **Verificación**: `user|has_permiso:'configurar_sistema' or user.is_superuser`
- **Se muestra si**: El usuario tiene permiso para configurar el sistema o es superusuario

#### Administración (Django Admin)
- **Verificación**: `user.is_staff`
- **Se muestra si**: El usuario tiene el flag `is_staff` activo

## Ejemplos de Configuración

### Ejemplo 1: Rol "Técnico" - Solo Lectura

**Permisos asignados:**
- `ver_clientes`
- `ver_instalaciones`
- `editar_instalaciones`
- `ver_pagos`
- `ver_inventario`
- `ver_notificaciones`

**Menú que verá:**
- ✅ Inicio
- ✅ Clientes (porque tiene `ver_clientes`)
- ✅ Instalaciones (porque tiene `ver_instalaciones`)
- ✅ Pagos (porque tiene `ver_pagos`)
- ✅ Inventario (porque tiene `ver_inventario`)
- ✅ Notificaciones (porque tiene `ver_notificaciones`)
- ❌ Catálogos (no tiene permiso)
- ❌ Roles y Permisos (no tiene permiso)
- ❌ Configuración (no tiene permiso)
- ✅ Administración (si tiene `is_staff=True`)

### Ejemplo 2: Rol "Instalador"

**Permisos asignados:**
- `ver_clientes`
- `ver_instalaciones`
- `crear_instalaciones`
- `editar_instalaciones`
- `gestionar_materiales_instalacion`
- `ver_inventario`
- `registrar_movimientos_inventario`
- `ver_notificaciones`

**Menú que verá:**
- ✅ Inicio
- ✅ Clientes
- ✅ Instalaciones
- ❌ Catálogos
- ❌ Pagos (no tiene ningún permiso de pagos)
- ✅ Inventario
- ✅ Notificaciones
- ❌ Roles y Permisos
- ❌ Configuración
- ✅ Administración (si tiene `is_staff=True`)

### Ejemplo 3: Rol "Supervisor"

**Permisos asignados:**
- Todos los permisos de lectura y escritura de: clientes, instalaciones, pagos, inventario, notificaciones
- `gestionar_roles_permisos`
- `configurar_sistema`
- `ver_reportes_generales`

**Menú que verá:**
- ✅ Inicio
- ✅ Clientes
- ✅ Instalaciones
- ✅ Catálogos
- ✅ Pagos
- ✅ Inventario
- ✅ Notificaciones
- ✅ Roles y Permisos
- ✅ Configuración
- ✅ Administración

## Cómo Agregar Nuevos Elementos al Menú

### Paso 1: Agregar el Elemento en el Template

Edita `templates/base.html` y agrega el elemento dentro de la verificación de permisos apropiada:

```django
{% load roles_tags %}

{% if user|puede_ver_modulo:'nombre_modulo' %}
    <li>
        <a href="{% url 'app:view_name' %}" 
           class="{% if 'ruta' in request.path %}active{% endif %}">
            <i class="fas fa-icono"></i> Nombre del Módulo
        </a>
    </li>
{% endif %}
```

### Paso 2: Asegurar que los Permisos Existan

Asegúrate de que los permisos de ese módulo estén creados en la base de datos con la categoría correcta.

### Paso 3: Asignar Permisos a Roles

Desde `/core/roles/<id>/permisos/`, asigna los permisos necesarios a cada rol.

## Template Tags Disponibles

### `puede_ver_modulo`
Verifica si el usuario puede ver un módulo completo (tiene al menos un permiso de esa categoría).

```django
{% if user|puede_ver_modulo:'clientes' %}
    <!-- Mostrar módulo de clientes -->
{% endif %}
```

### `has_permiso`
Verifica si el usuario tiene un permiso específico.

```django
{% if user|has_permiso:'ver_clientes' %}
    <!-- Mostrar opción -->
{% endif %}
```

### `has_rol`
Verifica si el usuario tiene un rol específico.

```django
{% if user|has_rol:'administrador' %}
    <!-- Mostrar opción solo para administradores -->
{% endif %}
```

## Notas Importantes

1. **Superusuarios**: Los superusuarios (`is_superuser=True`) siempre ven todos los módulos y tienen todos los permisos.

2. **Múltiples Roles**: Si un usuario tiene múltiples roles, tiene la **unión** de todos los permisos de esos roles.

3. **Permisos Activos**: Solo los permisos y roles **activos** se consideran para mostrar el menú.

4. **Cache**: Los permisos se verifican en cada carga de página. Si cambias los permisos de un rol, el usuario debe recargar la página para ver los cambios.

5. **Sidebar Izquierdo y Superior**: Ambos sidebars (izquierdo y superior) usan la misma lógica de permisos.

## Solución de Problemas

### El menú no se muestra aunque el usuario tiene permisos

1. Verifica que el permiso esté **activo** en `/admin/core/permiso/`
2. Verifica que el rol esté **activo** en `/admin/core/rol/`
3. Verifica que el usuario tenga el rol asignado y **activo** en `/admin/core/usuariorol/`
4. Verifica que el permiso tenga la **categoría correcta** (debe coincidir con el módulo)

### El usuario ve módulos que no debería ver

1. Revisa los permisos asignados al rol del usuario
2. Verifica que no tenga múltiples roles con permisos adicionales
3. Verifica que no sea superusuario (`is_superuser=True`)

## Archivos Modificados

- `templates/base.html`: Menú del sidebar actualizado con verificaciones de permisos
- `core/templatetags/roles_tags.py`: Template tags para verificar permisos

---

¿Necesitas ayuda? Revisa la guía completa en `GUIA_CONFIGURAR_MODULOS_ROLES.md`.

