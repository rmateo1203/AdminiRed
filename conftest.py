"""
Configuración global de pytest para el proyecto AdminiRed.
"""
import pytest
from django.contrib.auth.models import User
from clientes.models import Cliente
from instalaciones.models import Instalacion, TipoInstalacion, PlanInternet
from pagos.models import Pago
from inventario.models import Material, CategoriaMaterial


@pytest.fixture
def user(db):
    """Crea un usuario de prueba."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def superuser(db):
    """Crea un superusuario de prueba."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def cliente(db):
    """Crea un cliente de prueba."""
    return Cliente.objects.create(
        nombre='Juan',
        apellido1='Pérez',
        apellido2='García',
        email='juan@example.com',
        telefono='1234567890',
        direccion='Calle Principal 123',
        ciudad='Ciudad de México',
        estado='CDMX',
        codigo_postal='12345',
        estado_cliente='activo'
    )


@pytest.fixture
def tipo_instalacion(db):
    """Crea un tipo de instalación de prueba."""
    return TipoInstalacion.objects.create(
        nombre='Fibra Óptica',
        descripcion='Instalación de fibra óptica'
    )


@pytest.fixture
def plan_internet(db):
    """Crea un plan de internet de prueba."""
    return PlanInternet.objects.create(
        nombre='Plan Básico',
        velocidad_descarga=50,
        velocidad_subida=25,
        precio_mensual=500.00,
        activo=True
    )


@pytest.fixture
def instalacion(db, cliente, tipo_instalacion, plan_internet):
    """Crea una instalación de prueba."""
    return Instalacion.objects.create(
        cliente=cliente,
        tipo_instalacion=tipo_instalacion,
        direccion_instalacion='Calle Instalación 456',
        plan=plan_internet,
        plan_nombre='Plan Básico',
        velocidad_descarga=50,
        velocidad_subida=25,
        precio_mensual=500.00,
        estado='activa',
        numero_contrato='INST-20250102-0001'
    )


@pytest.fixture
def categoria_material(db):
    """Crea una categoría de material de prueba."""
    return CategoriaMaterial.objects.create(
        nombre='Cables',
        descripcion='Cables de red y fibra'
    )


@pytest.fixture
def material(db, categoria_material):
    """Crea un material de prueba."""
    return Material.objects.create(
        nombre='Cable UTP Cat6',
        codigo='CAB-UTP-001',
        categoria=categoria_material,
        stock_actual=100,
        stock_minimo=20,
        unidad_medida='metro',
        precio_compra=10.00,
        precio_venta=15.00,
        estado='disponible'
    )


@pytest.fixture
def pago(db, cliente, instalacion):
    """Crea un pago de prueba."""
    from datetime import date
    return Pago.objects.create(
        cliente=cliente,
        instalacion=instalacion,
        monto=500.00,
        concepto='Mensualidad Enero 2025',
        periodo_mes=1,
        periodo_anio=2025,
        fecha_vencimiento=date(2025, 1, 15),
        estado='pendiente'
    )


