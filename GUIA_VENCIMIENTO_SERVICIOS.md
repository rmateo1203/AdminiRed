# Guía: Determinación del Vencimiento de Servicios

## Resumen

El vencimiento de un servicio (instalación) se determina mediante la relación entre **Instalaciones**, **PlanPago** y **Pagos**.

## Cómo Funciona Actualmente

### 1. PlanPago (Plan de Pago Recurrente)

Un `PlanPago` está asociado a una instalación y define:
- **`monto_mensual`**: Monto que se cobra cada mes
- **`dia_vencimiento`**: Día del mes (1-31) en que vence el pago cada mes
- **`activo`**: Si el plan está activo

**Ejemplo:**
- Si `dia_vencimiento = 15`, el servicio vence el día 15 de cada mes.

### 2. Pagos

Cada `Pago` representa un cobro específico con:
- **`fecha_vencimiento`**: Fecha exacta en que vence ese pago
- **`periodo_mes`** y **`periodo_anio`**: Período al que corresponde
- **`estado`**: `pendiente`, `pagado`, `vencido`, `cancelado`

### 3. Determinación del Vencimiento

El vencimiento de un servicio se determina así:

1. **Si existe PlanPago activo:**
   - El vencimiento es el `dia_vencimiento` de cada mes
   - Se puede calcular automáticamente usando `PlanPago.calcular_proximo_vencimiento()`

2. **Si no existe PlanPago:**
   - Se busca el próximo pago pendiente o vencido
   - O se calcula basado en el último pago pagado

## Métodos Implementados

### En el Modelo `Instalacion`

#### `proximo_vencimiento` (property)
Calcula la próxima fecha de vencimiento del servicio.

```python
instalacion = Instalacion.objects.get(pk=1)
fecha_proxima = instalacion.proximo_vencimiento
# Retorna: date(2024, 12, 15) o None
```

#### `esta_al_dia` (property)
Verifica si el servicio está al día (sin pagos vencidos).

```python
if instalacion.esta_al_dia:
    print("Servicio al día")
else:
    print("Tiene pagos vencidos")
```

#### `dias_restantes_proximo_vencimiento` (property)
Calcula los días restantes hasta el próximo vencimiento.

```python
dias = instalacion.dias_restantes_proximo_vencimiento
if dias and dias <= 3:
    print(f"¡Urgente! Vence en {dias} días")
```

#### `monto_pendiente` (property)
Calcula el monto total pendiente de pagos.

```python
monto = instalacion.monto_pendiente
print(f"Monto pendiente: ${monto}")
```

#### `tiene_pago_vencido` (property)
Verifica si tiene algún pago vencido.

```python
if instalacion.tiene_pago_vencido:
    print("Tiene pagos vencidos")
```

### En el Modelo `PlanPago`

#### `calcular_fecha_vencimiento(mes, anio)`
Calcula la fecha de vencimiento para un mes y año específicos.

```python
plan_pago = PlanPago.objects.get(pk=1)
fecha = plan_pago.calcular_fecha_vencimiento(mes=12, anio=2024)
# Retorna: date(2024, 12, 15)
```

#### `calcular_proximo_vencimiento(desde_fecha=None)`
Calcula la próxima fecha de vencimiento desde una fecha dada.

```python
plan_pago = PlanPago.objects.get(pk=1)
proxima = plan_pago.calcular_proximo_vencimiento()
# Retorna: date(2025, 1, 15) si ya pasó el día 15 de este mes
```

#### `generar_pago_para_periodo(mes, anio, concepto=None)`
Genera una instancia de Pago para un período específico (sin guardar).

```python
plan_pago = PlanPago.objects.get(pk=1)
nuevo_pago = plan_pago.generar_pago_para_periodo(mes=12, anio=2024)
nuevo_pago.save()  # Guardar manualmente
```

## Ejemplos de Uso

### Ejemplo 1: Verificar si un servicio está al día

```python
from instalaciones.models import Instalacion

instalacion = Instalacion.objects.get(pk=1)

if instalacion.esta_al_dia:
    print(f"✓ {instalacion} está al día")
else:
    print(f"⚠ {instalacion} tiene pagos pendientes/vencidos")
    if instalacion.tiene_pago_vencido:
        print(f"  Monto pendiente: ${instalacion.monto_pendiente}")
```

### Ejemplo 2: Calcular el próximo vencimiento

```python
from instalaciones.models import Instalacion

instalacion = Instalacion.objects.get(pk=1)

proxima_fecha = instalacion.proximo_vencimiento
if proxima_fecha:
    dias_restantes = instalacion.dias_restantes_proximo_vencimiento
    
    if dias_restantes <= 0:
        print(f"⚠ El servicio venció hace {abs(dias_restantes)} días")
    elif dias_restantes <= 7:
        print(f"⚠ El servicio vence en {dias_restantes} días ({proxima_fecha})")
    else:
        print(f"✓ Próximo vencimiento: {proxima_fecha.strftime('%d/%m/%Y')} ({dias_restantes} días)")
```

### Ejemplo 3: Generar pagos automáticamente desde PlanPago

```python
from pagos.models import PlanPago
from django.utils import timezone
from datetime import date

hoy = date.today()
plan_pago = PlanPago.objects.get(pk=1)

# Calcular próximo vencimiento
proxima_fecha = plan_pago.calcular_proximo_vencimiento()

# Generar pago para ese período
nuevo_pago = plan_pago.generar_pago_para_periodo(
    mes=proxima_fecha.month,
    anio=proxima_fecha.year
)

# Verificar que no exista ya
from pagos.models import Pago
existe = Pago.objects.filter(
    cliente=nuevo_pago.cliente,
    instalacion=nuevo_pago.instalacion,
    periodo_mes=nuevo_pago.periodo_mes,
    periodo_anio=nuevo_pago.periodo_anio
).exists()

if not existe:
    nuevo_pago.save()
    print(f"✓ Pago creado: ${nuevo_pago.monto} - Vence: {nuevo_pago.fecha_vencimiento}")
else:
    print("⚠ Ya existe un pago para este período")
```

### Ejemplo 4: Listar servicios con sus vencimientos

```python
from instalaciones.models import Instalacion

servicios = Instalacion.objects.filter(estado='activa').select_related('cliente')

for servicio in servicios:
    print(f"\n{servicio.cliente.nombre_completo} - {servicio.plan_nombre}")
    print(f"  Estado: {servicio.get_estado_display()}")
    
    if servicio.esta_al_dia:
        print("  ✓ Al día")
    else:
        print(f"  ⚠ Monto pendiente: ${servicio.monto_pendiente}")
    
    proxima = servicio.proximo_vencimiento
    if proxima:
        dias = servicio.dias_restantes_proximo_vencimiento
        if dias and dias <= 7:
            print(f"  ⚠ Próximo vencimiento: {proxima.strftime('%d/%m/%Y')} ({dias} días)")
        else:
            print(f"  ✓ Próximo vencimiento: {proxima.strftime('%d/%m/%Y')} ({dias} días)")
```

## Comando de Gestión: Generar Pagos Automáticamente

Ya existe un comando para generar pagos automáticamente desde PlanPago:

```bash
# Generar pagos para el mes actual
python manage.py generar_pagos

# Generar pagos para un mes específico
python manage.py generar_pagos --mes 12 --anio 2024

# Solo generar pagos que no existen (evitar duplicados)
python manage.py generar_pagos --solo-pendientes

# Simular sin crear pagos
python manage.py generar_pagos --dry-run
```

## Casos Especiales

### Día de Vencimiento Mayor a los Días del Mes

Si `dia_vencimiento = 31` pero el mes solo tiene 30 días, se ajusta al último día del mes.

**Ejemplo:**
- `dia_vencimiento = 31`
- Mes: Febrero (28/29 días) → Se usa el último día del mes
- Mes: Abril (30 días) → Se usa el día 30

### Servicio sin PlanPago

Si una instalación no tiene PlanPago, el vencimiento se determina por:
1. El próximo pago pendiente o vencido existente
2. O se calcula sumando 1 mes al último pago pagado

## Actualización Automática de Estados

El modelo `Pago` actualiza automáticamente el estado a `vencido` cuando:
- El pago está en estado `pendiente`
- La `fecha_vencimiento` es anterior a la fecha actual
- Esto ocurre en el método `save()` del modelo

También existe un método de clase para actualizar todos los pagos vencidos:

```python
from pagos.models import Pago

cantidad = Pago.actualizar_pagos_vencidos()
print(f"Se actualizaron {cantidad} pagos a estado 'vencido'")
```

## Recomendaciones

1. **Crear PlanPago para instalaciones activas**: Esto permite calcular automáticamente los vencimientos.

2. **Ejecutar comando de generación de pagos mensualmente**: Configurar un cron job o tarea programada para ejecutar `generar_pagos` cada mes.

3. **Actualizar estados de pagos vencidos**: Ejecutar `Pago.actualizar_pagos_vencidos()` periódicamente (ej: diariamente).

4. **Monitorear servicios cerca de vencer**: Usar `dias_restantes_proximo_vencimiento` para alertas.

5. **Verificar estado del servicio**: Usar `esta_al_dia` para determinar si un servicio debe suspenderse.

