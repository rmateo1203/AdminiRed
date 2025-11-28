from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Cliente(models.Model):
    """Modelo para gestionar información de clientes."""
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Información básica
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido1 = models.CharField(max_length=50, verbose_name='Primer apellido')
    apellido2 = models.CharField(max_length=50, verbose_name='Segundo apellido', blank=True, null=True)
    email = models.EmailField(verbose_name='Correo electrónico', blank=True, null=True)
    telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Formato de teléfono inválido')],
        verbose_name='Teléfono'
    )
    
    # Dirección
    direccion = models.TextField(verbose_name='Dirección')
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    estado = models.CharField(max_length=50, verbose_name='Estado')
    codigo_postal = models.CharField(max_length=10, verbose_name='Código postal', blank=True)
    
    # Estado y fechas
    estado_cliente = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activo',
        verbose_name='Estado del cliente'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    # Información adicional
    notas = models.TextField(blank=True, null=True, verbose_name='Notas adicionales')
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['nombre', 'apellido1']),
            models.Index(fields=['telefono']),
            models.Index(fields=['estado_cliente']),
        ]
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del cliente."""
        apellidos = f"{self.apellido1}"
        if self.apellido2:
            apellidos += f" {self.apellido2}"
        return f"{self.nombre} {apellidos}".strip()
    
    def __str__(self):
        return f"{self.nombre_completo} - {self.telefono}"
    
    @property
    def tiene_instalacion_activa(self):
        """Verifica si el cliente tiene una instalación activa."""
        return self.instalaciones.filter(estado='activa').exists()
    
    @property
    def tiene_pagos_pendientes(self):
        """Verifica si el cliente tiene pagos pendientes."""
        return self.pagos.filter(estado='pendiente').exists()
