# 📝 Guía: Cambiar Contraseña desde el Formulario de Edición del Admin

## ✅ Nueva Funcionalidad Agregada

Ahora puedes cambiar la contraseña de un cliente **directamente desde el formulario de edición** en el Admin de Django, sin necesidad de usar acciones masivas.

---

## 🎯 Cómo Cambiar la Contraseña desde el Formulario

### Paso 1: Acceder al Admin
1. Ve a: `http://localhost:8000/admin/`
2. Inicia sesión con tus credenciales

### Paso 2: Ir al Cliente
1. Menú lateral → **CLIENTES** → **Clientes**
2. Busca el cliente que quieres editar
3. Haz clic en el **nombre del cliente** (o en el enlace "Cambiar" si estás en la lista)

### Paso 3: Expandir la Sección "Portal de Cliente"
1. Desplázate hasta la sección **"Portal de Cliente"**
2. Haz clic para **expandir** la sección (si está colapsada)
3. Verás los campos:
   - **Usuario:** (solo lectura - muestra el usuario asociado)
   - **Debe cambiar password:** (checkbox)
   - **Nueva contraseña del portal:** ← Campo nuevo
   - **Confirmar contraseña:** ← Campo nuevo

### Paso 4: Ingresar la Nueva Contraseña
1. En el campo **"Nueva contraseña del portal"**, ingresa la nueva contraseña
2. En el campo **"Confirmar contraseña"**, repite la misma contraseña
3. **Importante:** 
   - Mínimo 8 caracteres
   - Si dejas los campos vacíos, NO se cambiará la contraseña
   - Solo se cambia si ingresas una contraseña nueva

### Paso 5: Guardar
1. Haz clic en el botón **"Guardar"** (parte inferior del formulario)
2. Verás un mensaje de confirmación: `✅ Contraseña del portal actualizada para [Cliente]`

---

## 📋 Ejemplo Visual

```
[Formulario de Edición de Cliente]
│
├── Información Personal
│   ├── Nombre: [Juan Pérez]
│   ├── Email: [juan@email.com]
│   └── ...
│
├── Portal de Cliente  ← Expandir esta sección
│   ├── Usuario: juan.perez@email.com (solo lectura)
│   ├── ☐ Debe cambiar password
│   ├── Nueva contraseña del portal: [___________]  ← Ingresar aquí
│   └── Confirmar contraseña:       [___________]  ← Repetir aquí
│
└── [Guardar] [Guardar y continuar editando] [Guardar y añadir otro]
```

---

## ⚠️ Validaciones

El sistema valida:
- ✅ Si ingresas una contraseña, debe tener mínimo 8 caracteres
- ✅ Las contraseñas deben coincidir
- ✅ Si el cliente no tiene usuario, no se puede cambiar la contraseña
- ✅ Si dejas los campos vacíos, NO se cambia la contraseña

---

## 🔑 Características

### Ventajas:
- ✅ **Más fácil:** No necesitas usar acciones masivas
- ✅ **Edición directa:** Cambias la contraseña mientras editas otros datos del cliente
- ✅ **Opcional:** Si no ingresas contraseña, no se cambia
- ✅ **Validación en tiempo real:** El formulario valida antes de guardar

### Cuándo usar:
- Cuando quieres cambiar la contraseña de un solo cliente
- Cuando ya estás editando otros datos del cliente
- Cuando quieres control manual completo

---

## 📝 Ejemplo Práctico

**Escenario:** Cambiar la contraseña del cliente "María García"

1. **Acceder al admin:**
   ```
   http://localhost:8000/admin/clientes/cliente/
   ```

2. **Buscar y abrir el cliente:**
   - Buscar: "María García"
   - Clic en el nombre del cliente

3. **Expandir "Portal de Cliente":**
   - Desplazarse hasta "Portal de Cliente"
   - Expandir la sección (si está colapsada)

4. **Ingresar contraseña:**
   ```
   Nueva contraseña del portal:     MiNuevaPass123
   Confirmar contraseña:            MiNuevaPass123
   ```

5. **Guardar:**
   - Clic en: [Guardar]
   - Mensaje: `✅ Contraseña del portal actualizada para María García`

6. **Listo:**
   - La contraseña ha sido cambiada
   - El cliente puede iniciar sesión con: `MiNuevaPass123`

---

## 🔒 Seguridad

- ⚠️ **No se envía email automáticamente** (debes comunicar la contraseña al cliente)
- ⚠️ Las contraseñas están encriptadas (no se pueden ver después de guardar)
- ⚠️ Solo administradores pueden cambiar contraseñas
- ✅ El sistema fuerza el cambio de contraseña en el próximo login (si `debe_cambiar_password` está activo)

---

## 📍 Ubicación en el Formulario

```
Admin → CLIENTES → Clientes → [Nombre del Cliente]
  ↓
[Formulario de Edición]
  ↓
  Portal de Cliente (expandir)
    ├── Usuario: (solo lectura)
    ├── Debe cambiar password: ☐
    ├── Nueva contraseña del portal: [_______]  ← Aquí
    └── Confirmar contraseña:       [_______]  ← Aquí
```

---

## ❓ Preguntas Frecuentes

**P: ¿Qué pasa si dejo los campos de contraseña vacíos?**
R: No se cambiará la contraseña. Los campos son opcionales.

**P: ¿Se envía un email al cliente?**
R: No, con este método NO se envía email. Debes comunicar la contraseña manualmente.

**P: ¿Puedo cambiar la contraseña de múltiples clientes a la vez?**
R: No, este método es para un cliente a la vez. Para múltiples, usa las acciones masivas.

**P: ¿Qué pasa si el cliente no tiene usuario?**
R: No se puede cambiar la contraseña. Primero debes crear el usuario usando la acción "🔐 Crear usuario para portal".

**P: ¿Se valida la contraseña antes de guardar?**
R: Sí, el formulario valida:
   - Mínimo 8 caracteres
   - Las contraseñas deben coincidir
   - Si ingresas una, debes confirmarla

---

## ✅ Resumen Rápido

**Para cambiar contraseña desde el formulario:**
1. Admin → CLIENTES → Clientes → [Abrir cliente]
2. Expandir sección "Portal de Cliente"
3. Ingresar nueva contraseña
4. Confirmar contraseña
5. [Guardar]

**¡Listo!** La contraseña ha sido cambiada. 🎉

---

## 🔄 Comparación de Métodos

| Característica | Formulario de Edición | Acción Masiva "Establecer" |
|----------------|----------------------|----------------------------|
| Múltiples clientes | ❌ No | ✅ Sí |
| Edición simultánea de otros datos | ✅ Sí | ❌ No |
| Formulario intermedio | ❌ No | ✅ Sí |
| Más rápido para un cliente | ✅ Sí | ❌ No |
| Útil para múltiples clientes | ❌ No | ✅ Sí |









