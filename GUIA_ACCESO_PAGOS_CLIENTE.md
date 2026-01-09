# 📍 Guía: Dónde Ver las Opciones de Pago en el Portal del Cliente

## 🎯 Ubicación de las Opciones de Pago

Las opciones de pago en línea están disponibles en el **Portal del Cliente**. Aquí te mostramos exactamente dónde encontrarlas:

---

## 🔗 Rutas Principales

### 1. **Portal del Cliente**
- **URL**: `/clientes/portal/` o `/clientes/portal/login/`
- **Acceso**: Solo para clientes autenticados

### 2. **Mis Pagos**
- **URL**: `/clientes/portal/mis-pagos/`
- **Menú**: Sidebar izquierdo → "Mis Pagos"
- **Muestra**: Lista de todos los pagos del cliente

### 3. **Detalle de Pago**
- **URL**: `/clientes/portal/mis-pagos/<pago_id>/`
- **Acceso**: Haciendo clic en un pago desde "Mis Pagos"
- **Contiene**: Información completa del pago y botón "Pagar en Línea"

### 4. **Procesar Pago Online**
- **URL**: `/pagos/<pago_id>/pagar-online/`
- **Acceso**: Desde el botón "Pagar en Línea" en el detalle
- **Contiene**: Selección de pasarela (Mercado Pago, PayPal)

---

## 📱 Flujo Completo Paso a Paso

### **Paso 1: Acceder al Portal**

1. Ve a: `http://localhost:8000/clientes/portal/login/`
2. Inicia sesión con las credenciales del cliente
3. Serás redirigido al dashboard del portal

### **Paso 2: Ir a "Mis Pagos"**

Desde el dashboard o el sidebar izquierdo:
- Haz clic en **"Mis Pagos"** en el menú lateral
- O ve directamente a: `http://localhost:8000/clientes/portal/mis-pagos/`

### **Paso 3: Ver Lista de Pagos**

En "Mis Pagos" verás:
- **Tabla/Cards** con todos tus pagos
- **Información mostrada**:
  - Concepto
  - Fecha de vencimiento
  - Estado (Pendiente, Vencido, Pagado)
  - Monto
  - Botón **"Pagar"** (para pagos pendientes/vencidos)
  - Botón **"Ver"** (para todos los pagos)

### **Paso 4: Acceder al Detalle de un Pago**

Haz clic en:
- **"Pagar"** → Si el pago está pendiente o vencido
- **"Ver"** → Para ver cualquier pago

Esto te llevará a: `/clientes/portal/mis-pagos/<pago_id>/`

### **Paso 5: Ver el Botón "Pagar en Línea"**

En el detalle del pago, verás:

**Si el pago está Pendiente o Vencido:**
- ⚠️ Alerta amarilla: "Este pago está pendiente. Puedes pagarlo en línea."
- 🔵 **Botón grande "Pagar en Línea"** (azul/verde)

**Si el pago ya está Pagado:**
- ✅ Información del pago completado
- 📋 Historial de transacciones (si existe)
- ❌ NO aparece el botón "Pagar en Línea"

### **Paso 6: Seleccionar Método de Pago**

Al hacer clic en **"Pagar en Línea"**:

1. Serás redirigido a: `/pagos/<pago_id>/pagar-online/`
2. Verás un formulario con las pasarelas disponibles:
   - ✅ **Mercado Pago** (si está configurado)
   - ✅ **PayPal** (si está configurado)
   - ✅ **Stripe** (si está configurado)

3. Selecciona la pasarela deseada
4. Haz clic en **"Continuar con el Pago"**

### **Paso 7: Completar el Pago**

- Serás redirigido a la pasarela seleccionada
- Completa el proceso de pago
- Serás redirigido de vuelta al portal con confirmación

---

## 🔍 Ubicación Visual en la Interfaz

### **En el Sidebar (Menú Lateral)**

```
┌─────────────────────────┐
│  Mis Servicios          │
│                         │
│  👤 Nombre Cliente      │
│                         │
│  💳 Mis Pagos  ←─── AQUÍ│
│                         │
│  📡 Mis Instalaciones   │
│  • Plan Ultra 100 Mbps  │
│  • Plan Ultra 100 Mbps  │
│                         │
│  📊 Resumen             │
│  [KPIs de pagos]        │
│                         │
│  🔍 Filtros             │
│  [Búsqueda y filtros]   │
└─────────────────────────┘
```

### **En la Lista de Pagos**

```
┌─────────────────────────────────────────────────┐
│  Concepto        │ Vence  │ Estado │ Importe │ Acción │
├─────────────────────────────────────────────────┤
│  Pago mensual... │ 28/12  │ 🔴 Vencido │ $1299 │ [Pagar]│
│  Pago mensual... │ 28/12  │ 🔴 Vencido │ $1299 │ [Pagar]│
└─────────────────────────────────────────────────┘
```

### **En el Detalle del Pago**

```
┌─────────────────────────────────────┐
│  Detalle del Pago                   │
├─────────────────────────────────────┤
│  Concepto: Pago mensual - Enero 2026│
│  Monto: $1299.00                    │
│  Estado: 🔴 Vencido                 │
│  Fecha Vencimiento: 28/12/2025      │
│                                     │
│  ⚠️ Este pago está pendiente...    │
│                                     │
│  [💳 Pagar en Línea]  ←─── AQUÍ    │
│                                     │
│  [← Volver a Mis Pagos]             │
└─────────────────────────────────────┘
```

---

## ✅ Requisitos para Ver el Botón "Pagar en Línea"

El botón "Pagar en Línea" aparece SOLO si se cumplen TODAS estas condiciones:

1. ✅ El pago está en estado **"Pendiente"** o **"Vencido"**
2. ✅ Hay al menos una pasarela configurada (Mercado Pago, PayPal o Stripe)
3. ✅ El cliente está autenticado en el portal
4. ✅ El pago pertenece al cliente autenticado

---

## 🐛 Si No Ves el Botón "Pagar en Línea"

### **Problema 1: El pago ya está pagado**

✅ **Solución**: Es normal, el botón solo aparece para pagos pendientes o vencidos.

### **Problema 2: Las pasarelas no están configuradas**

❌ **Síntoma**: Aparece el mensaje: "Las pasarelas de pago no están configuradas..."

✅ **Solución**: 
1. Configura al menos una pasarela (ver `DEMO_PAGOS_MERCADOPAGO_PAYPAL.md`)
2. Verifica las credenciales en `.env`
3. Ejecuta los scripts de verificación:
   ```bash
   python verificar_mercadopago.py
   python verificar_paypal.py
   ```

### **Problema 3: No puedes acceder al portal**

❌ **Síntoma**: No puedes iniciar sesión o acceder a `/clientes/portal/`

✅ **Solución**:
1. Verifica que el cliente tenga un usuario creado
2. Verifica que el cliente esté activo
3. Contacta al administrador si necesitas acceso

---

## 📋 Resumen Rápido

| Acción | Dónde | URL |
|--------|-------|-----|
| **Iniciar sesión** | Portal Login | `/clientes/portal/login/` |
| **Ver mis pagos** | Menú lateral | `/clientes/portal/mis-pagos/` |
| **Ver detalle** | Desde lista | `/clientes/portal/mis-pagos/<id>/` |
| **Pagar en línea** | Botón en detalle | `/pagos/<id>/pagar-online/` |
| **Seleccionar pasarela** | Formulario | Selección de Mercado Pago/PayPal |

---

## 🎯 Para Probar el Demo

1. **Crear datos de prueba**:
   ```bash
   python crear_datos_demo.py
   ```

2. **Iniciar sesión como cliente**:
   - Ve a: http://localhost:8000/clientes/portal/login/
   - Usa las credenciales del cliente creado

3. **Navegar a "Mis Pagos"**:
   - Haz clic en "Mis Pagos" en el sidebar
   - O ve a: http://localhost:8000/clientes/portal/mis-pagos/

4. **Hacer clic en "Pagar"** en un pago pendiente/vencido

5. **Hacer clic en "Pagar en Línea"** en el detalle

6. **Seleccionar Mercado Pago o PayPal**

7. **Completar el pago** usando tarjetas de prueba

---

**¡Ahora sabes exactamente dónde encontrar las opciones de pago!** 🎉

