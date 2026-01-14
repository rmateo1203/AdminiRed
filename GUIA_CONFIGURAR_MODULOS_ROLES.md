# Guía: Configurar Módulos y Permisos por Rol

Esta guía explica cómo configurar qué módulos puede ver y usar cada rol en el sistema AdminiRed.

## 📋 Índice

1. [Conceptos Básicos](#conceptos-básicos)
2. [Estructura de Permisos por Módulo](#estructura-de-permisos-por-módulo)
3. [Cómo Asignar Permisos a un Rol](#cómo-asignar-permisos-a-un-rol)
4. [Usar Permisos en las Vistas](#usar-permisos-en-las-vistas)
5. [Verificar Permisos en Templates](#verificar-permisos-en-templates)
6. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Conceptos Básicos

### ¿Qué es un Módulo?
Un **módulo** es una categoría funcional del sistema. Los módulos principales son:
- **clientes**: Gestión de clientes
- **instalaciones**: Gestión de instalaciones
- **pagos**: Control de pagos
- **inventario**: Gestión de inventario
- **notificaciones**: Sistema de notificaciones
- **sistema**: Configuración del sistema

### ¿Qué es un Permiso?
Un **permiso** es una acción específica que se puede realizar en un módulo. Por ejemplo:
- `ver_clientes`: Ver la lista de clientes
- `crear_clientes`: Crear nuevos clientes
- `editar_clientes`: Editar clientes existentes
- `eliminar_clientes`: Eliminar clientes

### ¿Qué es un Rol?
Un **rol** es un conjunto de permisos agrupados. Los usuarios tienen roles, y los roles tienen permisos.

**Flujo**: Usuario → Rol → Permisos → Acceso a Módulos

---

## Estructura de Permisos por Módulo

### Módulo: Clientes (`categoria: 'clientes'`)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `ver_clientes` | Ver Clientes | Ver lista y detalles de clientes |
| `crear_clientes` | Crear Clientes | Crear nuevos clientes |
| `editar_clientes` | Editar Clientes | Editar información de clientes |
| `eliminar_clientes` | Eliminar Clientes | Eliminar clientes |
| `gestionar_portal_clientes` | Gestionar Portal de Clientes | Gestionar acceso y credenciales del portal |

### Módulo: Instalaciones (`categoria: 'instalaciones'`)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `ver_instalaciones` | Ver Instalaciones | Ver lista y detalles de instalaciones |
| `crear_instalaciones` | Crear Instalaciones | Crear nuevas instalaciones |
| `editar_instalaciones` | Editar Instalaciones | Editar información de instalaciones |
| `eliminar_instalaciones` | Eliminar Instalaciones | Eliminar instalaciones |
| `gestionar_materiales_instalacion` | Gestionar Materiales de Instalación | Gestionar materiales asignados |

### Módulo: Pagos (`categoria: 'pagos'`)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `ver_pagos` | Ver Pagos | Ver lista y detalles de pagos |
| `crear_pagos` | Crear Pagos | Crear nuevos pagos |
| `editar_pagos` | Editar Pagos | Editar información de pagos |
| `eliminar_pagos` | Eliminar Pagos | Eliminar pagos |
| `marcar_pagos_pagados` | Marcar Pagos como Pagados | Marcar pagos como pagados |
| `capturar_pagos_manuales` | Capturar Pagos Manuales | Capturar pagos por transferencia/depósito |
| `reembolsar_pagos` | Reembolsar Pagos | Reembolsar pagos |
| `ver_reportes_pagos` | Ver Reportes de Pagos | Ver reportes y estadísticas |

### Módulo: Inventario (`categoria: 'inventario'`)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `ver_inventario` | Ver Inventario | Ver el inventario de materiales |
| `gestionar_inventario` | Gestionar Inventario | Crear, editar y eliminar materiales |
| `registrar_movimientos_inventario` | Registrar Movimientos | Registrar entradas, salidas y ajustes |

### Módulo: Notificaciones (`categoria: 'notificaciones'`)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `ver_notificaciones` | Ver Notificaciones | Ver notificaciones del sistema |
| `gestionar_notificaciones` | Gestionar Notificaciones | Crear y gestionar notificaciones |
| `configurar_notificaciones` | Configurar Notificaciones | Configurar notificaciones automáticas |

### Módulo: Sistema (`categoria: 'sistema'`)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `gestionar_roles_permisos` | Gestionar Roles y Permisos | Gestionar roles y permisos del sistema |
| `gestionar_usuarios` | Gestionar Usuarios | Gestionar usuarios del sistema |
| `configurar_sistema` | Configurar Sistema | Configurar parámetros del sistema |
| `ver_reportes_generales` | Ver Reportes Generales | Ver reportes y estadísticas generales |

---

## Cómo Asignar Permisos a un Rol

### ✅ Método 1: Desde el Admin Personalizado (RECOMENDADO)

1. **Accede al Admin Personalizado**: `/core/roles/`
2. **Ve a la Lista de Roles**: Haz clic en "Lista de Roles" o ve a `/core/roles/lista/`
3. **Selecciona un Rol**: Haz clic en el rol que quieres configurar (ej: "Técnico")
4. **Gestiona Permisos**: 
   - En la página de detalle del rol, verás un botón "Gestionar Permisos" o
   - Ve directamente a `/core/roles/<id_rol>/permisos/`
5. **Selecciona Permisos por Módulo**: 
   - Los permisos están organizados por categoría (módulo)
   - Marca los permisos que deseas asignar al rol
   - Desmarca los que no debe tener
6. **Guarda los Cambios**: Haz clic en "Guardar"

**Ventajas del Admin Personalizado:**
- ✅ Interfaz más amigable
- ✅ Permisos organizados por módulo (categoría)
- ✅ Vista clara de qué permisos tiene cada rol
- ✅ Fácil de usar para usuarios no técnicos

### Método 2: Desde el Admin de Django

1. **Accede al Admin de Django**: `/admin/`
2. **Ve a Core → Roles**: Encuentra el rol que quieres configurar
3. **Edita el Rol**: Haz clic en el rol (ej: "Técnico")
4. **Asigna Permisos**: En la sección "Permisos del Rol", selecciona los permisos que deseas asignar
5. **Guarda**: Haz clic en "Guardar"

### Ejemplo: Configurar Rol "Técnico"

Para que un técnico pueda:
- ✅ Ver clientes
- ✅ Ver instalaciones
- ✅ Editar instalaciones (pero no crear)
- ✅ Ver pagos
- ✅ Ver inventario
- ❌ NO puede crear instalaciones
- ❌ NO puede gestionar pagos

**Pasos para configurar:**

1. **Accede al Admin Personalizado**: `/core/roles/lista/`
2. **Selecciona el Rol "Técnico"**: Haz clic en el nombre del rol
3. **Gestiona Permisos**: Haz clic en el botón "Gestionar Permisos" (o ve a `/core/roles/<id>/permisos/`)
4. **Selecciona los Permisos por Módulo**:
   - **Módulo Clientes**: Marca `ver_clientes`
   - **Módulo Instalaciones**: Marca `ver_instalaciones` y `editar_instalaciones` (NO marques `crear_instalaciones`)
   - **Módulo Pagos**: Marca `ver_pagos` (NO marques `crear_pagos` ni `editar_pagos`)
   - **Módulo Inventario**: Marca `ver_inventario`
   - **Módulo Notificaciones**: Marca `ver_notificaciones`
5. **Guarda**: Haz clic en "Guardar Permisos"

**Permisos a asignar:**
- `ver_clientes`
- `ver_instalaciones`
- `editar_instalaciones`
- `ver_pagos`
- `ver_inventario`
- `ver_notificaciones`

---

## Usar Permisos en las Vistas

### Decorador `@permiso_required`

Protege una vista para que solo usuarios con el permiso específico puedan acceder:

```python
from core.roles_decorators import permiso_required

@login_required
@permiso_required('ver_clientes')
def cliente_list(request):
    """Lista de clientes - solo usuarios con permiso 'ver_clientes'"""
    # Tu código aquí
    pass

@login_required
@permiso_required('crear_clientes')
def cliente_create(request):
    """Crear cliente - solo usuarios con permiso 'crear_clientes'"""
    # Tu código aquí
    pass
```

### Decorador `@permisos_required` (múltiples permisos)

Requiere uno o varios permisos:

```python
from core.roles_decorators import permisos_required

# Requiere AL MENOS UNO de los permisos
@permisos_required('ver_pagos', 'ver_reportes_pagos')
def ver_informacion_pagos(request):
    """Puede ver si tiene ver_pagos O ver_reportes_pagos"""
    pass

# Requiere TODOS los permisos
@permisos_required('ver_clientes', 'editar_clientes', require_all=True)
def gestionar_clientes(request):
    """Debe tener AMBOS permisos"""
    pass
```

### Decorador `@rol_required`

Requiere un rol específico (menos flexible que permisos):

```python
from core.roles_decorators import rol_required

@rol_required('administrador', 'supervisor')
def configuracion_avanzada(request):
    """Solo administradores o supervisores"""
    pass
```

### Verificar Permisos Manualmente

Si necesitas verificar permisos dentro de una vista:

```python
from core.roles_utils import usuario_tiene_permiso

def mi_vista(request):
    if usuario_tiene_permiso(request.user, 'ver_clientes'):
        # Mostrar información adicional
        pass
    else:
        # Ocultar o mostrar mensaje
        pass
```

---

## Verificar Permisos en Templates

### En Templates Django

El sistema ya incluye template tags listos para usar. Carga `roles_tags`:

```django
{% load roles_tags %}

{# Verificar un permiso específico #}
{% if user|has_permiso:'ver_clientes' %}
    <a href="{% url 'clientes:cliente_list' %}">Ver Clientes</a>
{% endif %}

{# Verificar si puede crear #}
{% if user|has_permiso:'crear_clientes' %}
    <a href="{% url 'clientes:cliente_create' %}">Crear Cliente</a>
{% endif %}

{# Verificar si puede ver un módulo completo #}
{% if user|puede_ver_modulo:'clientes' %}
    <li><a href="{% url 'clientes:cliente_list' %}">Clientes</a></li>
{% endif %}

{# Verificar un rol #}
{% if user|has_rol:'administrador' %}
    <a href="{% url 'admin:index' %}">Admin</a>
{% endif %}
```

### Ocultar Módulos Completos en el Menú

```django
{% load permisos_tags %}

{# Módulo Clientes #}
{% if user|tiene_permiso:'ver_clientes' %}
<li class="menu-item">
    <a href="{% url 'clientes:cliente_list' %}">
        <i class="fas fa-users"></i> Clientes
    </a>
</li>
{% endif %}

{# Módulo Pagos #}
{% if user|tiene_permiso:'ver_pagos' %}
<li class="menu-item">
    <a href="{% url 'pagos:pago_list' %}">
        <i class="fas fa-money-bill"></i> Pagos
    </a>
</li>
{% endif %}
```

---

## Ejemplos Prácticos

### Ejemplo 1: Rol "Técnico" - Solo Lectura

**Objetivo**: El técnico puede ver información pero no modificar.

**Permisos a asignar:**
- `ver_clientes`
- `ver_instalaciones`
- `editar_instalaciones` (para actualizar estado)
- `ver_pagos`
- `ver_inventario`
- `ver_notificaciones`

**Vistas a proteger:**
```python
# clientes/views.py
@login_required
@permiso_required('ver_clientes')
def cliente_list(request):
    # ...

@login_required
@permiso_required('ver_clientes')
def cliente_detail(request, pk):
    # ...

# NO agregar @permiso_required('crear_clientes') si no debe crear
```

### Ejemplo 2: Rol "Instalador" - Gestión de Instalaciones

**Objetivo**: El instalador puede gestionar instalaciones y ver información relacionada.

**Permisos a asignar:**
- `ver_clientes` (para ver datos del cliente)
- `ver_instalaciones`
- `crear_instalaciones`
- `editar_instalaciones`
- `gestionar_materiales_instalacion`
- `ver_pagos` (para ver información relacionada)
- `ver_inventario`
- `registrar_movimientos_inventario` (para registrar uso de materiales)
- `ver_notificaciones`

### Ejemplo 3: Rol "Supervisor" - Todo Excepto Configuración

**Objetivo**: El supervisor puede gestionar todo excepto configuración del sistema.

**Permisos a asignar:**
- Todos los permisos de: clientes, instalaciones, pagos, inventario, notificaciones
- `ver_reportes_generales`
- ❌ NO incluir: `gestionar_roles_permisos`, `configurar_sistema`

---

## Checklist para Configurar un Nuevo Rol

1. ✅ **Crear el Rol** en `/admin/core/rol/` o `/core/roles/`
2. ✅ **Asignar Permisos** al rol según las necesidades
3. ✅ **Proteger las Vistas** con `@permiso_required`
4. ✅ **Actualizar el Menú** para mostrar/ocultar módulos según permisos
5. ✅ **Probar el Acceso** con un usuario de prueba

---

## Comandos Útiles

### Crear Roles y Permisos Iniciales

```bash
python manage.py crear_roles_permisos_iniciales
```

Este comando crea todos los roles y permisos básicos del sistema.

### Verificar Permisos de un Usuario (Shell)

```python
python manage.py shell

from django.contrib.auth import get_user_model
from core.roles_utils import usuario_tiene_permiso, obtener_permisos_usuario

User = get_user_model()
usuario = User.objects.get(username='nombre_usuario')

# Verificar un permiso específico
usuario_tiene_permiso(usuario, 'ver_clientes')

# Ver todos los permisos del usuario
permisos = obtener_permisos_usuario(usuario)
for permiso in permisos:
    print(f"{permiso.codigo} - {permiso.nombre} ({permiso.categoria})")
```

---

## Resumen

1. **Permisos** están organizados por **categoría** (módulo)
2. **Roles** tienen **permisos** asignados
3. **Usuarios** tienen **roles** asignados
4. **Vistas** se protegen con decoradores `@permiso_required`
5. **Templates** verifican permisos para mostrar/ocultar elementos

**Flujo completo:**
```
Usuario → Rol → Permisos → Acceso a Módulos
```

## ✅ Implementación en el Admin Personalizado

**SÍ, está completamente implementado** en el admin personalizado. Puedes gestionar permisos por módulo desde:

### Ruta Principal
- **Dashboard de Roles**: `/core/roles/`
- **Lista de Roles**: `/core/roles/lista/`
- **Gestionar Permisos de un Rol**: `/core/roles/<id_rol>/permisos/`

### Características del Admin Personalizado

✅ **Interfaz organizada por módulos**: Los permisos se muestran agrupados por categoría (módulo)
✅ **Fácil de usar**: Checkboxes para seleccionar/deseleccionar permisos
✅ **Vista previa**: Puedes ver qué permisos tiene cada rol antes de editarlos
✅ **Información detallada**: Cada permiso muestra su nombre, descripción y código
✅ **Actualización en tiempo real**: Los cambios se aplican inmediatamente

### Cómo Acceder

1. Inicia sesión como usuario con permiso `gestionar_roles_permisos`
2. Ve a `/core/roles/` o busca "Roles y Permisos" en el menú
3. Selecciona un rol de la lista
4. Haz clic en "Gestionar Permisos"
5. Marca/desmarca los permisos por módulo
6. Guarda los cambios

---

## Notas Importantes

- ⚠️ Los **superusuarios** tienen todos los permisos automáticamente
- ⚠️ Los permisos deben estar **activos** para funcionar
- ⚠️ Los roles deben estar **activos** para funcionar
- ⚠️ Un usuario puede tener **múltiples roles**
- ⚠️ Si un usuario tiene múltiples roles, tiene la **unión** de todos los permisos

---

¿Necesitas ayuda con alguna configuración específica? Revisa los ejemplos o consulta la documentación del código.

