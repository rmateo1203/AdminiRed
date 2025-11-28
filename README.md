# AdminiRed
Sistema para el control total de instalaciones de internet.

## Estructura del Proyecto

Este proyecto sigue las mejores prácticas de Django y Python:

```
AdminiRed/
├── adminired/              # Configuración del proyecto
│   ├── settings/           # Configuración modular por entorno
│   │   ├── __init__.py    # Selector de entorno
│   │   ├── base.py        # Configuración base compartida
│   │   ├── development.py # Configuración de desarrollo
│   │   └── production.py  # Configuración de producción
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── clientes/               # Aplicación: Gestión de clientes
├── instalaciones/           # Aplicación: Gestión de instalaciones
├── pagos/                   # Aplicación: Control de pagos
├── inventario/              # Aplicación: Gestión de inventario
├── notificaciones/          # Aplicación: Sistema de notificaciones
├── static/                  # Archivos estáticos (CSS, JS, imágenes)
├── staticfiles/             # Archivos estáticos recolectados (generado)
├── media/                   # Archivos de medios subidos por usuarios
├── templates/               # Plantillas HTML del proyecto
├── manage.py
├── requirements.txt         # Dependencias del proyecto
├── .env                     # Variables de entorno (no versionado)
├── .env.example             # Ejemplo de variables de entorno
└── venv/                    # Entorno virtual (no versionado)
```

## Configuración

### Variables de Entorno

El proyecto utiliza `python-decouple` para manejar variables de entorno de forma segura.

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita `.env` con tus configuraciones específicas.

### Configuración Modular

La configuración está separada en tres archivos:
- **base.py**: Configuración compartida entre todos los entornos
- **development.py**: Configuración para desarrollo local
- **production.py**: Configuración para producción

El entorno se selecciona automáticamente mediante la variable `DJANGO_ENVIRONMENT` en `.env`.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd AdminiRed
   ```

2. Crea y activa el entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env con tus configuraciones
   ```

5. Ejecuta las migraciones:
   ```bash
   python manage.py migrate
   ```

6. Crea un superusuario (opcional):
   ```bash
   python manage.py createsuperuser
   ```

## Uso

### Servidor de Desarrollo

```bash
source venv/bin/activate
python manage.py runserver
```

El servidor estará disponible en `http://127.0.0.1:8000/`

### Comandos Útiles

- Verificar configuración: `python manage.py check`
- Crear migraciones: `python manage.py makemigrations`
- Aplicar migraciones: `python manage.py migrate`
- Recolectar archivos estáticos: `python manage.py collectstatic`

## Mejores Prácticas Implementadas

- ✅ Configuración modular por entorno (desarrollo/producción)
- ✅ Variables de entorno con `python-decouple`
- ✅ Separación de archivos estáticos y medios
- ✅ Configuración de idioma y zona horaria (español/México)
- ✅ Estructura de directorios organizada
- ✅ `.gitignore` configurado correctamente
- ✅ `requirements.txt` actualizado

## Aplicaciones del Proyecto

El proyecto está organizado en 5 aplicaciones Django especializadas:

### 1. **clientes** - Gestión de Clientes
- Modelo `Cliente`: Información completa de clientes (datos personales, dirección, estado)
- Características:
  - Validación de teléfono
  - Estados: activo, inactivo, suspendido, cancelado
  - Búsqueda y filtrado avanzado
  - Propiedades para verificar instalaciones activas y pagos pendientes

### 2. **instalaciones** - Gestión de Instalaciones
- Modelos:
  - `TipoInstalacion`: Tipos de instalación (Fibra, Cable, etc.)
  - `Instalacion`: Instalaciones de internet a clientes
- Características:
  - Seguimiento completo del ciclo de vida (pendiente → programada → activa)
  - Información técnica (IP, MAC, coordenadas)
  - Gestión de planes y velocidades
  - Control de fechas (solicitud, programación, instalación, activación)

### 3. **pagos** - Control de Pagos
- Modelos:
  - `Pago`: Registro de pagos individuales
  - `PlanPago`: Planes de pago recurrentes
- Características:
  - Estados: pendiente, pagado, vencido, cancelado
  - Múltiples métodos de pago
  - Control de períodos (mes/año)
  - Cálculo automático de días vencidos
  - Referencias de pago para trazabilidad

### 4. **inventario** - Gestión de Materiales
- Modelos:
  - `CategoriaMaterial`: Categorías de materiales
  - `Material`: Materiales del inventario
  - `MovimientoInventario`: Historial de movimientos
- Características:
  - Control de stock (actual, mínimo)
  - Alertas automáticas de bajo stock
  - Precios de compra y venta
  - Historial completo de movimientos (entrada, salida, ajuste, devolución)
  - Ubicación en almacén

### 5. **notificaciones** - Sistema de Notificaciones
- Modelos:
  - `TipoNotificacion`: Tipos de notificaciones
  - `Notificacion`: Notificaciones individuales
  - `ConfiguracionNotificacion`: Configuración de notificaciones automáticas
- Características:
  - Múltiples canales (email, SMS, WhatsApp, sistema)
  - Notificaciones programadas
  - Notificaciones automáticas de pagos vencidos
  - Seguimiento de intentos y resultados
  - Configuración flexible por tipo de notificación

## Relaciones entre Aplicaciones

```
Cliente
  ├── Instalaciones (1:N)
  │   └── PlanPago (1:1)
  ├── Pagos (1:N)
  │   └── Notificaciones (1:N)
  └── Notificaciones (1:N)
```

## Tecnologías

- Python 3.12
- Django 5.2.8
- python-decouple 3.8
