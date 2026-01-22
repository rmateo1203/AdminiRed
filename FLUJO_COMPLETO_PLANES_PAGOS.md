# 📋 Flujo Completo: Cliente → Instalación → PlanPago → Pagos

## 🎯 Objetivo
Documentar el flujo completo desde la creación de un cliente hasta la generación de pagos mensuales.

---

## 🔄 Flujo Paso a Paso

### 1️⃣ **Crear Cliente**
```
Cliente se crea con:
- Nombre, apellidos, teléfono, email, etc.
- Estado: activo
```

### 2️⃣ **Crear Instalación**
```
Instalación se crea asociada al Cliente:
- Cliente: [Cliente seleccionado]
- Plan: [PlanInternet del catálogo, opcional]
- plan_nombre: "Plan Básico 50 Mbps"
- precio_mensual: $500.00
- velocidad_descarga: 50 Mbps
- estado: "pendiente" (por defecto)
- fecha_solicitud: [automático]
```

**Estado inicial:** `pendiente` → No tiene PlanPago todavía

---

### 3️⃣ **Activar Instalación** ⭐ (PASO CRÍTICO)

Cuando la instalación cambia a estado `activa`:

#### 3.1 Establecer fecha_activacion
```python
# En Instalacion.save():
if estado == 'activa' and not fecha_activacion:
    fecha_activacion = timezone.now()
```

**Ejemplo:** Si se activa el **15 de enero de 2024 a las 10:30 AM**
- `fecha_activacion = 2024-01-15 10:30:00`

#### 3.2 Crear PlanPago automáticamente
```python
# Señal automática crea PlanPago en tabla pagos_planpago:
PlanPago.objects.create(
    instalacion=instalacion,
    monto_mensual=instalacion.precio_mensual,  # $500.00
    dia_vencimiento=15,  # Día de fecha_activacion
    activo=True
)
```

**Resultado:**
- ✅ PlanPago registrado en `pagos_planpago`
- ✅ `monto_mensual` = $500.00 (desde instalación)
- ✅ `dia_vencimiento` = 15 (día de fecha_activacion)
- ✅ `activo` = True

#### 3.3 Usuario tiene servicio
**A partir de `fecha_activacion` (15/01/2024), el cliente ya tiene servicio de internet activo.**

---

### 4️⃣ **Generar Pagos Mensuales**

Usar el comando de gestión:
```bash
python manage.py generar_pagos
```

#### 4.1 El comando:
1. Busca todos los `PlanPago` activos con `Instalacion` activa
2. Para cada PlanPago, genera un `Pago` para el período (mes/año)
3. Calcula `fecha_vencimiento` usando `dia_vencimiento`

#### 4.2 Ejemplo de generación:

**PlanPago:**
- `monto_mensual` = $500.00
- `dia_vencimiento` = 15

**Pagos generados:**
```
Enero 2024:
  - monto: $500.00
  - fecha_vencimiento: 2024-01-15
  - periodo_mes: 1
  - periodo_anio: 2024
  - estado: pendiente

Febrero 2024:
  - monto: $500.00
  - fecha_vencimiento: 2024-02-15
  - periodo_mes: 2
  - periodo_anio: 2024
  - estado: pendiente

Marzo 2024:
  - monto: $500.00
  - fecha_vencimiento: 2024-03-15
  - periodo_mes: 3
  - periodo_anio: 2024
  - estado: pendiente
```

---

## 📊 Estructura de Datos

### Tabla: `clientes_cliente`
```sql
id | nombre | apellido1 | telefono | email | ...
```

### Tabla: `instalaciones_instalacion`
```sql
id | cliente_id | plan_id | plan_nombre | precio_mensual | estado | fecha_activacion | ...
```

### Tabla: `pagos_planpago` ⭐
```sql
id | instalacion_id | monto_mensual | dia_vencimiento | activo
```
**Relación:** OneToOne con `instalaciones_instalacion`

### Tabla: `pagos_pago`
```sql
id | cliente_id | instalacion_id | monto | fecha_vencimiento | periodo_mes | periodo_anio | estado | ...
```

---

## 🔑 Puntos Clave

### ✅ **Fecha de Activación**
- Se establece **automáticamente** cuando `estado` cambia a `'activa'`
- Si no existe, se usa `timezone.now()`
- **Es la fecha desde la cual el cliente tiene servicio**

### ✅ **Día de Vencimiento**
- Se calcula desde `fecha_activacion.day`
- **Ejemplo:** Si se activa el día 15, todos los meses vence el día 15
- Si el mes tiene menos días (ej: febrero), se ajusta al último día del mes

### ✅ **Monto Mensual**
- Se toma de `instalacion.precio_mensual`
- Si cambia el precio, se sincroniza automáticamente con `PlanPago.monto_mensual`

### ✅ **PlanPago Automático**
- Se crea **automáticamente** cuando instalación se activa
- Solo si `precio_mensual > 0`
- Se registra en tabla `pagos_planpago`
- **No se puede crear manualmente** (se crea automáticamente)

---

## 🎬 Ejemplo Completo

### Escenario:
1. **15/01/2024 10:00** - Se crea Cliente "Juan Pérez"
2. **15/01/2024 10:05** - Se crea Instalación para Juan Pérez
   - `estado` = "pendiente"
   - `precio_mensual` = $500.00
   - **No hay PlanPago todavía**
3. **15/01/2024 14:30** - Se activa la instalación
   - `estado` → "activa"
   - `fecha_activacion` = 2024-01-15 14:30:00
   - **Se crea PlanPago automáticamente:**
     - `monto_mensual` = $500.00
     - `dia_vencimiento` = 15
     - `activo` = True
   - **Cliente tiene servicio desde 15/01/2024 14:30**
4. **16/01/2024** - Se ejecuta `python manage.py generar_pagos --mes 1 --anio 2024`
   - Se crea Pago para Enero 2024:
     - `monto` = $500.00
     - `fecha_vencimiento` = 2024-01-15
     - `estado` = "pendiente"
5. **01/02/2024** - Se ejecuta `python manage.py generar_pagos --mes 2 --anio 2024`
   - Se crea Pago para Febrero 2024:
     - `monto` = $500.00
     - `fecha_vencimiento` = 2024-02-15
     - `estado` = "pendiente"

---

## ⚙️ Comandos Útiles

```bash
# Generar pagos para el mes actual
python manage.py generar_pagos

# Generar pagos para un mes específico
python manage.py generar_pagos --mes 2 --anio 2024

# Solo generar si no existe pago del período
python manage.py generar_pagos --solo-pendientes

# Simular sin crear (dry-run)
python manage.py generar_pagos --dry-run
```

---

## 🔍 Verificación

Para verificar que todo funciona:

1. **Ver PlanPago creado:**
   ```python
   instalacion = Instalacion.objects.get(numero_contrato="...")
   print(instalacion.plan_pago)
   # Debe mostrar: PlanPago con monto_mensual y dia_vencimiento
   ```

2. **Ver fecha de activación:**
   ```python
   print(instalacion.fecha_activacion)
   # Debe mostrar la fecha cuando se activó
   ```

3. **Verificar día de vencimiento:**
   ```python
   print(instalacion.plan_pago.dia_vencimiento)
   # Debe ser igual a instalacion.fecha_activacion.day
   ```

---

## ✅ Resumen

1. ✅ Cliente se crea
2. ✅ Instalación se crea (estado: pendiente)
3. ✅ Cuando instalación se activa:
   - ✅ Se establece `fecha_activacion`
   - ✅ Se crea `PlanPago` automáticamente en `pagos_planpago`
   - ✅ `dia_vencimiento` = día de `fecha_activacion`
   - ✅ `monto_mensual` = `precio_mensual` de instalación
4. ✅ A partir de `fecha_activacion`, cliente tiene servicio
5. ✅ Se generan pagos mensuales desde `PlanPago`

