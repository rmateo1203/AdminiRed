# 📝 Guía: Cómo Cambiar la Contraseña de un Usuario desde el Admin

## 🔑 Opciones Disponibles

Hay **dos formas** de cambiar/establecer la contraseña de un cliente desde el Admin:

1. **🔑 Restablecer contraseña del portal** - Genera una contraseña automática y envía email
2. **✏️ Establecer contraseña manualmente** - Permite establecer una contraseña específica

---

## ✏️ Método 1: Establecer Contraseña Manualmente (Recomendado para control total)

### Paso 1: Acceder al Admin de Django
1. Abre tu navegador y ve a: `http://localhost:8000/admin/`
2. Inicia sesión con tus credenciales de administrador

### Paso 2: Ir a la Sección de Clientes
1. En el menú lateral izquierdo, busca y haz clic en **"CLIENTES"**
2. Luego haz clic en **"Clientes"**

### Paso 3: Buscar el Cliente
Puedes buscar el cliente de varias formas:
- **Búsqueda rápida:** Usa el cuadro de búsqueda en la parte superior
- **Filtros:** Usa los filtros laterales (Estado, Ciudad, Fecha, etc.)
- **Lista completa:** Navega por la lista de clientes

### Paso 4: Seleccionar el Cliente
1. Marca el **checkbox** (☐) a la izquierda del nombre del cliente que deseas editar
2. Puedes seleccionar **múltiples clientes** si quieres cambiar la contraseña a varios a la vez

### Paso 5: Ejecutar la Acción
1. En el menú desplegable **"Acción"** (parte superior de la lista), busca:
   - **"✏️ Establecer contraseña manualmente"**
2. Haz clic en el botón **"Ir"** (al lado del menú desplegable)

### Paso 6: Completar el Formulario
Se abrirá una página con un formulario. Debes completar:

1. **Nueva contraseña:**
   - Ingresa la contraseña que deseas establecer
   - Mínimo 8 caracteres

2. **Confirmar contraseña:**
   - Repite la misma contraseña para confirmar

### Paso 7: Guardar
1. Revisa que las contraseñas coincidan
2. Haz clic en el botón **"Establecer contraseña"**
3. Verás mensajes de confirmación en la parte superior

### Ejemplo Visual del Proceso:

```
Admin → CLIENTES → Clientes
  ↓
[Lista de Clientes]
  ☐ Juan Pérez          [Búsqueda: ________]  [Acción: ✏️ Establecer... ▼] [Ir]
  ☐ María García
  ☑ Carlos López  ← Seleccionado
  
  ↓ (Hacer clic en "Ir")
  
[Página de Establecer Contraseña]
  
  Establecer contraseña para: Carlos López
  Usuario: carlos.lopez@email.com
  
  Nueva contraseña:     [________________]
  Confirmar contraseña: [________________]
  
  [Establecer contraseña]  [Cancelar]
```

---

## 🔑 Método 2: Restablecer Contraseña (Genera automáticamente)

### Pasos 1-4: Iguales al Método 1
(Seguir los pasos 1-4 del método anterior)

### Paso 5: Ejecutar la Acción
1. En el menú desplegable **"Acción"**, selecciona:
   - **"🔑 Restablecer contraseña del portal"**
2. Haz clic en **"Ir"**

### Paso 6: Confirmar
- **No hay formulario adicional** - La acción se ejecuta inmediatamente
- El sistema genera una contraseña aleatoria automáticamente
- Se envía un email al cliente con la nueva contraseña

### Diferencia Clave:
- **Método 1 (Manual):** Tú defines la contraseña
- **Método 2 (Restablecer):** El sistema genera una contraseña automática

---

## 📋 Resumen de Pasos (Método Manual)

```
1. Admin → CLIENTES → Clientes
2. Buscar cliente
3. ☑ Marcar checkbox del cliente
4. Acción: "✏️ Establecer contraseña manualmente" → [Ir]
5. Ingresar nueva contraseña
6. Confirmar contraseña
7. [Establecer contraseña]
```

---

## ✅ Verificación

Después de establecer la contraseña:

1. **Mensajes de confirmación:**
   - Verás un mensaje verde: `✅ Contraseña establecida para [Cliente] (Usuario: [username]).`

2. **Probar el login:**
   - El cliente puede iniciar sesión en el portal con la nueva contraseña
   - URL del portal: `http://localhost:8000/clientes/portal/login/`

---

## ⚠️ Casos Especiales

### Cliente sin Usuario del Portal
Si el cliente no tiene usuario:
- Verás una advertencia: `⚠️ El cliente "[Nombre]" no tiene usuario del portal.`
- **Solución:** Primero crea el usuario usando la acción **"🔐 Crear usuario para portal"**

### Múltiples Clientes Seleccionados
- Puedes seleccionar varios clientes
- La misma contraseña se aplicará a todos los clientes seleccionados
- Se mostrará un resumen al final

### Validaciones
El sistema valida:
- ✅ Contraseña no vacía
- ✅ Mínimo 8 caracteres
- ✅ Las contraseñas coinciden
- ✅ El cliente tiene usuario del portal

---

## 🎯 Ejemplo Práctico Completo

**Escenario:** Cambiar la contraseña del cliente "Juan Pérez"

1. **Acceder al admin:**
   ```
   http://localhost:8000/admin/
   ```

2. **Navegar a clientes:**
   ```
   Menú lateral → CLIENTES → Clientes
   ```

3. **Buscar cliente:**
   - En el buscador escribo: "Juan Pérez"
   - Presiono Enter o hago clic en buscar

4. **Seleccionar:**
   - Marca el checkbox: ☑ Juan Pérez

5. **Ejecutar acción:**
   - Acción: "✏️ Establecer contraseña manualmente"
   - Clic en: [Ir]

6. **Completar formulario:**
   ```
   Nueva contraseña:     MiNuevaPassword123
   Confirmar contraseña: MiNuevaPassword123
   ```

7. **Guardar:**
   - Clic en: [Establecer contraseña]

8. **Resultado:**
   - Mensaje: `✅ Contraseña establecida para Juan Pérez (Usuario: juan.perez@email.com).`
   - El cliente puede iniciar sesión con: `MiNuevaPassword123`

---

## 🔒 Seguridad

### Buenas Prácticas:
- ✅ Usa contraseñas seguras (mínimo 8 caracteres, mayúsculas, números, símbolos)
- ✅ Comunica la nueva contraseña al cliente de forma segura
- ✅ El sistema fuerza el cambio de contraseña en el próximo login
- ✅ Solo administradores pueden usar esta funcionalidad

### Consideraciones:
- ⚠️ La contraseña se establece inmediatamente (no hay confirmación adicional)
- ⚠️ El cliente deberá cambiar la contraseña en el próximo login (si `debe_cambiar_password` está activo)
- ⚠️ No se envía email automáticamente con el método manual (debes comunicarla tú)

---

## 📍 Ubicación en el Admin

```
Admin de Django
└── CLIENTES
    └── Clientes
        ├── [Lista de clientes con checkboxes]
        ├── [Búsqueda]
        ├── [Filtros]
        └── [Acción: ✏️ Establecer contraseña manualmente] → [Ir]
```

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo cambiar la contraseña de múltiples clientes a la vez?**
R: Sí, selecciona múltiples checkboxes y usa la acción. La misma contraseña se aplicará a todos.

**P: ¿Se envía un email al cliente?**
R: Con "Establecer contraseña manualmente" NO se envía email. Con "Restablecer contraseña" SÍ se envía.

**P: ¿Qué pasa si el cliente no tiene usuario?**
R: Verás una advertencia y deberás crear el usuario primero.

**P: ¿La contraseña tiene alguna validación?**
R: Sí, mínimo 8 caracteres y debe coincidir en ambos campos.

**P: ¿Puedo ver la contraseña después de establecerla?**
R: No, las contraseñas están encriptadas. Solo puedes establecer una nueva.

---

## ✅ Resumen Rápido

**Para cambiar contraseña manualmente:**
1. Admin → CLIENTES → Clientes
2. ☑ Seleccionar cliente(s)
3. Acción: "✏️ Establecer contraseña manualmente"
4. [Ir]
5. Ingresar contraseña
6. Confirmar contraseña
7. [Establecer contraseña]

**¡Listo!** La contraseña ha sido cambiada. 🎉

