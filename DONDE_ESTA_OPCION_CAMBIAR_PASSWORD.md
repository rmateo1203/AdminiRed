# 📍 ¿Dónde está la Opción para Cambiar la Contraseña?

## ⚠️ Importante: Dos Interfaces Diferentes

El sistema tiene **DOS interfaces diferentes**:

1. **Interfaz Personalizada** (la que estás viendo): `/clientes/`
2. **Admin de Django** (donde está la opción): `/admin/`

---

## 🎯 La Opción Está en el Admin de Django

La funcionalidad para cambiar contraseñas está disponible en el **Admin de Django**, NO en la interfaz personalizada.

### Cómo Acceder:

1. **URL Directa:**
   ```
   http://localhost:8000/admin/
   ```

2. **Desde el Navegador:**
   - Abre una nueva pestaña
   - Ve a: `http://localhost:8000/admin/`
   - Inicia sesión con tus credenciales de administrador

3. **Navegación:**
   ```
   Admin de Django (/admin/)
   └── CLIENTES
       └── Clientes
           └── [Seleccionar cliente]
               └── Formulario de edición
                   └── Sección "Portal de Cliente"
                       ├── Nueva contraseña del portal
                       └── Confirmar contraseña
   ```

---

## 📋 Pasos Detallados:

### Paso 1: Ir al Admin de Django
- URL: `http://localhost:8000/admin/`
- (No es `/clientes/` - es `/admin/`)

### Paso 2: Iniciar Sesión
- Usa tus credenciales de administrador (superusuario)

### Paso 3: Navegar a Clientes
- Menú lateral izquierdo → **CLIENTES**
- Clic en **"Clientes"**

### Paso 4: Abrir un Cliente
- Buscar el cliente (usando el buscador o la lista)
- Hacer clic en el **nombre del cliente** para editarlo

### Paso 5: Encontrar los Campos de Contraseña
- Desplázate hasta la sección **"Portal de Cliente"**
- Si está colapsada, haz clic para expandirla
- Verás los campos:
  - **Usuario:** (solo lectura)
  - **Debe cambiar password:** ☐
  - **Nueva contraseña del portal:** ← **AQUÍ**
  - **Confirmar contraseña:** ← **AQUÍ**

### Paso 6: Cambiar la Contraseña
- Ingresa la nueva contraseña
- Confirma la contraseña
- Haz clic en **"Guardar"**

---

## 🔍 Comparación Visual:

### Interfaz Personalizada (donde estás ahora):
```
URL: http://localhost:8000/clientes/
- Lista de clientes
- Búsqueda y filtros
- Acciones masivas (pero NO incluye cambiar contraseña)
```

### Admin de Django (donde está la opción):
```
URL: http://localhost:8000/admin/
- Interfaz del admin de Django
- Menú lateral con todas las secciones
- Formularios de edición completos
- Campos para cambiar contraseña
```

---

## ✅ Resumen:

**La opción para cambiar contraseña NO está en:**
- ❌ La interfaz personalizada (`/clientes/`)
- ❌ El menú "Seleccionar acción..." de la lista de clientes

**La opción SÍ está en:**
- ✅ El Admin de Django (`/admin/`)
- ✅ El formulario de edición del cliente
- ✅ La sección "Portal de Cliente"

---

## 🚀 Acceso Rápido:

1. Abre: `http://localhost:8000/admin/`
2. Login → CLIENTES → Clientes
3. Abre un cliente
4. Sección "Portal de Cliente" → Campos de contraseña

---

## 💡 Nota:

Si quieres agregar esta funcionalidad también en la interfaz personalizada (`/clientes/`), sería necesario:
- Crear una vista personalizada
- Agregar una acción al menú "Seleccionar acción..."
- Crear un formulario en la interfaz personalizada

¿Quieres que agregue esta funcionalidad también en la interfaz personalizada?



