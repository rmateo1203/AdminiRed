# 🔧 Sistema Configurable de Número de Contrato

## 📋 Descripción

Sistema dinámico y configurable para la generación automática de números de contrato en instalaciones. Permite personalizar completamente el formato, prefijo, secuencia y comportamiento de la generación.

---

## ✨ Funcionalidades

### 1. **Configuración Dinámica** ✅
- Formato personalizable con variables
- Prefijo configurable
- Número inicial configurable
- Cantidad de dígitos de secuencia configurable
- Opción de reiniciar secuencia diariamente o mantener secuencia global

### 2. **Variables Disponibles** ✅
- `{YYYY}` - Año completo (ej: 2024)
- `{YY}` - Año de 2 dígitos (ej: 24)
- `{MM}` - Mes con 2 dígitos (ej: 12)
- `{DD}` - Día con 2 dígitos (ej: 15)
- `{####}` - Número secuencial (obligatorio)
- `{PREFIJO}` - Prefijo personalizado

### 3. **Interfaz de Configuración** ✅
- Vista web para configurar el formato
- Preview en tiempo real del formato
- Ejemplos de formatos predefinidos
- Validación de formato

### 4. **Generación Automática** ✅
- Generación automática si no se especifica número de contrato
- Verificación de unicidad
- Prevención de colisiones
- Caché para mejor rendimiento

---

## 🚀 Uso

### Acceder a la Configuración

1. **Desde la lista de instalaciones:**
   - Hacer clic en "Configurar Número Contrato"

2. **URL directa:**
   ```
   /instalaciones/configurar-numero-contrato/
   ```

3. **Desde Django Admin:**
   - Instalaciones → Configuraciones de Número de Contrato

### Configurar el Formato

1. **Activar configuración**: Marcar "Configuración activa"
2. **Definir formato**: Usar variables disponibles
3. **Configurar prefijo**: Si se usa `{PREFIJO}`
4. **Ajustar secuencia**: Número inicial y dígitos
5. **Reiniciar diario**: Activar/desactivar según necesidad
6. **Ver preview**: Se actualiza automáticamente
7. **Guardar**: Hacer clic en "Guardar Configuración"

---

## 📝 Ejemplos de Formatos

### Formato 1: Con fecha completa
```
Formato: INST-{YYYY}{MM}{DD}-{####}
Resultado: INST-20241215-0001
```

### Formato 2: Con año corto
```
Formato: {PREFIJO}-{YY}{MM}{DD}-{####}
Resultado: INST-241215-0001
```

### Formato 3: Solo año y número
```
Formato: CONTRATO-{YYYY}-{####}
Resultado: CONTRATO-2024-0001
```

### Formato 4: Sin separadores
```
Formato: {PREFIJO}{YYYY}{MM}{DD}{####}
Resultado: INST202412150001
```

### Formato 5: Con separadores personalizados
```
Formato: {PREFIJO}/{YYYY}/{MM}/{####}
Resultado: INST/2024/12/0001
```

---

## ⚙️ Configuración Detallada

### Campos de Configuración

#### **Formato** (Obligatorio)
- **Descripción**: Patrón del número de contrato
- **Requisito**: Debe contener `{####}` para el número secuencial
- **Ejemplo**: `INST-{YYYY}{MM}{DD}-{####}`

#### **Prefijo Personalizado**
- **Descripción**: Prefijo usado con `{PREFIJO}`
- **Opcional**: Sí
- **Ejemplo**: `INST`, `CONTRATO`, `INSTAL`

#### **Número Inicial**
- **Descripción**: Número inicial de la secuencia
- **Rango**: 1 o mayor
- **Default**: 1

#### **Dígitos de Secuencia**
- **Descripción**: Cantidad de dígitos para el número secuencial
- **Rango**: 1-10
- **Default**: 4
- **Ejemplo**: 4 dígitos = `0001`, 6 dígitos = `000001`

#### **Reiniciar Secuencia Diariamente**
- **Descripción**: Si la secuencia se reinicia cada día
- **Opciones**:
  - ✅ **Activado**: La secuencia se reinicia cada día (ej: 0001, 0002... cada día)
  - ❌ **Desactivado**: La secuencia es global y continúa incrementándose

---

## 🔄 Comportamiento

### Con Reinicio Diario (Activado)

**Ventaja**: Números más cortos y organizados por día
**Ejemplo**:
- Día 1: `INST-20241215-0001`, `INST-20241215-0002`
- Día 2: `INST-20241216-0001`, `INST-20241216-0002` (reinicia)

### Sin Reinicio Diario (Desactivado)

**Ventaja**: Secuencia continua y única globalmente
**Ejemplo**:
- Día 1: `INST-20241215-0001`, `INST-20241215-0002`
- Día 2: `INST-20241216-0003`, `INST-20241216-0004` (continúa)

---

## 🛠️ Implementación Técnica

### Modelo
- **`ConfiguracionNumeroContrato`**: Modelo para almacenar la configuración
- Solo una configuración activa a la vez
- Caché para mejor rendimiento

### Servicio
- **`NumeroContratoService`**: Servicio para generar números
- Método `generar_numero_contrato()`: Genera número único
- Método `obtener_preview()`: Genera preview del formato

### Vista
- **`configurar_numero_contrato`**: Vista de configuración
- **`preview_numero_contrato`**: API para preview en tiempo real

---

## 📊 Flujo de Generación

1. **Usuario crea instalación** sin especificar número de contrato
2. **Sistema obtiene configuración activa** (con caché)
3. **Reemplaza variables** de fecha y prefijo
4. **Busca último número** usado (según reinicio diario)
5. **Genera siguiente número** en secuencia
6. **Formatea número** con dígitos especificados
7. **Verifica unicidad** y ajusta si es necesario
8. **Asigna número** a la instalación

---

## 🔍 Validaciones

### Validaciones del Formulario
- ✅ Formato debe contener `{####}`
- ✅ Dígitos de secuencia entre 1 y 10
- ✅ Número inicial mayor a 0

### Validaciones del Modelo
- ✅ Solo una configuración activa
- ✅ Formato válido con variables

### Validaciones de Generación
- ✅ Verificación de unicidad
- ✅ Prevención de colisiones
- ✅ Límite de intentos (1000)

---

## 💡 Mejores Prácticas

### Recomendaciones de Formato

1. **Incluir fecha**: Facilita identificación y organización
   ```
   INST-{YYYY}{MM}{DD}-{####}
   ```

2. **Usar separadores**: Mejora legibilidad
   ```
   {PREFIJO}-{YYYY}-{####}
   ```

3. **Dígitos suficientes**: 4-6 dígitos para secuencias largas
   ```
   {####} con 4-6 dígitos
   ```

4. **Prefijo descriptivo**: Identifica el tipo de contrato
   ```
   INST, CONTRATO, INSTAL, etc.
   ```

### Cuándo Reiniciar Diariamente

✅ **Recomendado cuando:**
- Se crean muchas instalaciones diarias
- Se quiere organización por día
- Los números se usan para reportes diarios

❌ **No recomendado cuando:**
- Se crean pocas instalaciones
- Se necesita secuencia global única
- Se requiere rastreo continuo

---

## 🐛 Solución de Problemas

### El número no se genera automáticamente

**Causa**: El campo `numero_contrato` está siendo llenado manualmente
**Solución**: Dejar el campo vacío al crear la instalación

### El formato no funciona

**Causa**: Formato inválido o falta `{####}`
**Solución**: Verificar que el formato contenga `{####}` y use variables válidas

### Números duplicados

**Causa**: Configuración incorrecta o problema de concurrencia
**Solución**: El sistema verifica unicidad automáticamente, pero si persiste, revisar configuración

### Preview no se actualiza

**Causa**: Error en JavaScript o formato inválido
**Solución**: Verificar formato y recargar la página

---

## 📋 Checklist de Configuración

- [ ] Acceder a configuración de número de contrato
- [ ] Activar configuración
- [ ] Definir formato con `{####}`
- [ ] Configurar prefijo (si se usa `{PREFIJO}`)
- [ ] Ajustar número inicial
- [ ] Configurar dígitos de secuencia
- [ ] Decidir si reiniciar diariamente
- [ ] Verificar preview
- [ ] Guardar configuración
- [ ] Probar creando una instalación sin número de contrato

---

## ✅ Estado

**Sistema implementado y funcional** ✅

- ✅ Modelo de configuración
- ✅ Servicio de generación dinámica
- ✅ Vista de configuración
- ✅ Template con preview en tiempo real
- ✅ API para preview
- ✅ Integración con formulario de instalación
- ✅ Validaciones robustas
- ✅ Caché para rendimiento

---

*Sistema implementado: Diciembre 2024*  
*Módulo: Instalaciones*  
*Versión: 1.0*

