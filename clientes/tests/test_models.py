"""
Tests unitarios para los modelos de la app clientes.
"""
import pytest
from django.core.exceptions import ValidationError
from clientes.models import Cliente


@pytest.mark.django_db
class TestClienteModel:
    """Tests para el modelo Cliente."""
    
    def test_crear_cliente(self, cliente):
        """Test: Crear un cliente básico."""
        assert cliente.pk is not None
        assert cliente.nombre == 'Juan'
        assert cliente.apellido1 == 'Pérez'
        assert cliente.estado_cliente == 'activo'
    
    def test_nombre_completo(self, cliente):
        """Test: Propiedad nombre_completo."""
        assert cliente.nombre_completo == 'Juan Pérez García'
        
        # Cliente sin segundo apellido
        cliente2 = Cliente.objects.create(
            nombre='María',
            apellido1='López',
            telefono='0987654321',
            direccion='Calle 2',
            ciudad='Guadalajara',
            estado='Jalisco',
            estado_cliente='activo'
        )
        assert cliente2.nombre_completo == 'María López'
    
    def test_tiene_instalacion_activa(self, cliente, instalacion):
        """Test: Propiedad tiene_instalacion_activa."""
        assert cliente.tiene_instalacion_activa is True
        
        # Cambiar instalación a no activa
        instalacion.estado = 'cancelada'
        instalacion.save()
        cliente.refresh_from_db()
        assert cliente.tiene_instalacion_activa is False
    
    def test_tiene_pagos_pendientes(self, cliente, pago):
        """Test: Propiedad tiene_pagos_pendientes."""
        assert cliente.tiene_pagos_pendientes is True
        
        # Marcar pago como pagado
        pago.estado = 'pagado'
        pago.save()
        cliente.refresh_from_db()
        assert cliente.tiene_pagos_pendientes is False
    
    def test_validacion_telefono(self):
        """Test: Validación de formato de teléfono."""
        # Teléfono válido
        cliente = Cliente(
            nombre='Test',
            apellido1='User',
            telefono='1234567890',
            direccion='Test',
            ciudad='Test',
            estado='Test',
            estado_cliente='activo'
        )
        cliente.full_clean()  # No debe lanzar error
        
        # Teléfono inválido (muy corto)
        cliente.telefono = '123'
        with pytest.raises(ValidationError):
            cliente.full_clean()
    
    def test_str_representation(self, cliente):
        """Test: Representación string del modelo."""
        assert str(cliente) == 'Juan Pérez García - 1234567890'
    
    def test_ordering(self, cliente):
        """Test: Ordenamiento por fecha de registro."""
        from datetime import timedelta
        from django.utils import timezone
        
        cliente2 = Cliente.objects.create(
            nombre='Nuevo',
            apellido1='Cliente',
            telefono='1111111111',
            direccion='Test',
            ciudad='Test',
            estado='Test',
            estado_cliente='activo'
        )
        
        clientes = Cliente.objects.all()
        assert clientes[0] == cliente2  # Más reciente primero
        assert clientes[1] == cliente


