# 📋 Guía: Captura Manual de Pagos por Transferencia o Depósito

## ✅ El Sistema ESTÁ Preparado

El sistema AdminiRed **ya está configurado** para que el administrador capture manualmente los pagos realizados por transferencia bancaria o depósito.

## 🔧 Cómo Capturar un Pago Manual

### Opción 1: Desde el Admin de Django (Recomendado)

1. **Acceder al Admin de Django:**
   - URL: `http://localhost:8000/admin/` (o tu dominio)
   - Iniciar sesión como administrador

2. **Ir a la sección de Pagos:**
   - En el menú lateral, buscar y hacer clic en **"Pagos"** (dentro de PAGOS)

3. **Buscar el pago a capturar:**
   - Usar el buscador superior para buscar por:
     - Nombre del cliente
     - Teléfono del cliente
     - Referencia de pago
     - Concepto
   - O usar los filtros por:
     - Estado (filtrar por "pendiente" o "vencido")
     - Método de pago
     - Período (mes/año)
     - Fecha de vencimiento

4. **Editar el pago:**
   - Hacer clic en el pago que se desea editar
   - Se abrirá el formulario de edición

5. **Completar los datos del pago:**
   - **Estado:** Cambiar a `"Pagado"`
   - **Método de pago:** Seleccionar:
     - `"Transferencia bancaria"` para transferencias
     - `"Depósito"` para depósitos bancarios
     - `"Efectivo"` si fue en efectivo
   - **Fecha de pago:** Ingresar la fecha y hora del depósito/transferencia
     - Formato: `DD/MM/AAAA HH:MM`
     - Ejemplo: `15/01/2024 14:30`
   - **Referencia de pago:** Ingresar el número de transacción o referencia bancaria
     - Ejemplos:
       - `TRF-123456789`
       - `DEP-987654321`
       - `Código de rastreo: ABC123XYZ`
   - **Notas (opcional):** Agregar información adicional:
     - Banco origen/destino
     - Cuenta bancaria
     - Comentarios adicionales

6. **Guardar:**
   - Hacer clic en el botón **"Guardar"** (parte inferior del formulario)
   - El sistema validará los datos y guardará el pago

### Opción 2: Acción Masiva (Solo marca como pagado)

1. **Seleccionar múltiples pagos:**
   - En la lista de pagos, seleccionar los checkboxes de los pagos a marcar
   - Puedes seleccionar varios pagos

2. **Usar la acción "Marcar como pagado":**
   - En el menú desplegable "Acción" (parte superior)
   - Seleccionar `"Marcar como pagado"`
   - Hacer clic en "Ir"

3. **⚠️ Limitación:**
   - Esta acción solo cambia el estado a "pagado"
   - **NO** permite ingresar:
     - Método de pago
     - Referencia de pago
     - Fecha de pago específica
   - La fecha de pago se establece automáticamente a "ahora"

4. **Recomendación:**
   - Después de usar la acción masiva, editar cada pago individualmente para agregar:
     - Método de pago
     - Referencia de pago
     - Fecha de pago correcta

## 📊 Campos Disponibles en el Formulario

El formulario de pago incluye las siguientes secciones:

### 1. Información del Pago
- Cliente
- Instalación (opcional)
- Concepto
- Monto

### 2. Período
- Mes
- Año

### 3. Fechas
- **Fecha de vencimiento** (solo lectura si se creó automáticamente)
- **Fecha de pago** ⭐ (editable - ingresar fecha/hora del depósito/transferencia)
- Fecha de registro (solo lectura)

### 4. Estado y Método ⭐
- **Estado** ⭐ (cambiar a "Pagado")
- **Método de pago** ⭐ (seleccionar: Transferencia bancaria, Depósito, etc.)
- **Referencia de pago** ⭐ (número de transacción, referencia bancaria)

### 5. Notas
- Campo de texto libre para información adicional

⭐ = Campos clave para captura manual

## ✅ Validaciones del Sistema

El sistema realiza las siguientes validaciones:

1. **Fecha de pago:**
   - No puede ser anterior a la fecha de vencimiento
   - No puede ser futura (máximo 1 hora en el futuro para ajustes de zona horaria)

2. **Estado "Pagado":**
   - Si el estado es "Pagado", la fecha de pago es obligatoria

3. **Períodos duplicados:**
   - No puede haber dos pagos activos del mismo período para el mismo cliente e instalación

## 🔍 Buscar Pagos Pendientes

Para facilitar la captura de pagos manuales, puedes usar los filtros:

1. **Filtrar por Estado:**
   - Seleccionar "Pendiente" o "Vencido" en el filtro lateral

2. **Filtrar por Período:**
   - Seleccionar el mes y año en los filtros

3. **Ordenar:**
   - Por defecto, los pagos se ordenan por fecha de vencimiento (más recientes primero)

## 📝 Ejemplo de Captura Manual

**Escenario:** Un cliente realizó una transferencia bancaria y el administrador debe capturarla.

1. El cliente realizó una transferencia el **15 de enero de 2024 a las 14:30**
2. El número de referencia es **TRF-123456789**
3. El banco de origen es **Banco ABC**
4. El monto es **$500.00**

**Pasos:**
1. Ir al admin → Pagos
2. Buscar el pago del cliente (filtrar por estado "Pendiente")
3. Hacer clic en el pago
4. Completar:
   - Estado: `Pagado`
   - Método de pago: `Transferencia bancaria`
   - Fecha de pago: `15/01/2024 14:30`
   - Referencia de pago: `TRF-123456789`
   - Notas: `Transferencia desde Banco ABC`
5. Guardar

## 🔐 Permisos Requeridos

- El usuario debe ser **superusuario** o tener permisos de edición en el modelo `Pago`
- Normalmente, solo los administradores tienen acceso al admin de Django

## 📌 Notas Importantes

1. **Fecha de pago:**
   - Es importante capturar la fecha/hora real del depósito/transferencia, no la fecha actual
   - Esto ayuda a mantener un registro preciso de cuándo se recibió el pago

2. **Referencia de pago:**
   - Siempre capturar el número de referencia o transacción
   - Esto permite verificar el pago posteriormente si es necesario

3. **Método de pago:**
   - Seleccionar correctamente el método ayuda a generar reportes precisos
   - Opciones disponibles:
     - Efectivo
     - Transferencia bancaria
     - Tarjeta de crédito/débito
     - Depósito
     - Otro

4. **Notas:**
   - Usar el campo de notas para información adicional que pueda ser útil
   - Ejemplos:
     - Banco origen/destino
     - Número de cuenta
     - Observaciones especiales

## 🚀 Mejoras Futuras Posibles

Si en el futuro se requiere mejorar el proceso de captura manual, se podría:

1. **Crear una vista personalizada** para captura rápida de pagos manuales
2. **Agregar una acción personalizada** en el admin que permita ingresar todos los datos
3. **Implementar un formulario inline** para captura rápida desde la lista de pagos
4. **Agregar validación de referencias duplicadas** para evitar capturar el mismo pago dos veces

## ✅ Resumen

**SÍ, el sistema está preparado para capturar pagos manuales.**

El administrador puede:
- ✅ Editar pagos desde el admin de Django
- ✅ Cambiar el estado a "Pagado"
- ✅ Seleccionar el método de pago (Transferencia, Depósito, etc.)
- ✅ Ingresar la referencia de pago (número de transacción)
- ✅ Establecer la fecha y hora del pago
- ✅ Agregar notas adicionales

**No se requiere ninguna configuración adicional.**

