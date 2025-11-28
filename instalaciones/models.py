from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from clientes.models import Cliente


class TipoInstalacion(models.Model):
    """Tipos de instalación disponibles (Fibra, Cable, etc.)"""
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Tipo de instalación')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    
    class Meta:
        verbose_name = 'Tipo de Instalación'
        verbose_name_plural = 'Tipos de Instalación'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Instalacion(models.Model):
    """Modelo para gestionar instalaciones de internet."""
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('programada', 'Programada'),
        ('en_proceso', 'En Proceso'),
        ('activa', 'Activa'),
        ('suspendida', 'Suspendida'),
        ('cancelada', 'Cancelada'),
    ]
    
    # Relación con cliente
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='instalaciones',
        verbose_name='Cliente'
    )
    
    # Información de la instalación
    tipo_instalacion = models.ForeignKey(
        TipoInstalacion,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Tipo de instalación'
    )
    direccion_instalacion = models.TextField(verbose_name='Dirección de instalación')
    coordenadas = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Coordenadas (lat, lng)',
        help_text='Formato: latitud,longitud'
    )
    
    # Plan y velocidad
    plan_nombre = models.CharField(max_length=100, verbose_name='Nombre del plan')
    velocidad_descarga = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Velocidad de descarga (Mbps)'
    )
    velocidad_subida = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Velocidad de subida (Mbps)',
        blank=True,
        null=True
    )
    precio_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio mensual'
    )
    
    # Estado y fechas
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de solicitud')
    fecha_programada = models.DateTimeField(blank=True, null=True, verbose_name='Fecha programada')
    fecha_instalacion = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de instalación')
    fecha_activacion = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de activación')
    
    # Información técnica
    ip_asignada = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP asignada')
    mac_equipo = models.CharField(max_length=17, blank=True, null=True, verbose_name='MAC del equipo')
    numero_contrato = models.CharField(max_length=50, unique=True, verbose_name='Número de contrato')
    
    # Notas
    notas_instalacion = models.TextField(blank=True, null=True, verbose_name='Notas de instalación')
    notas_tecnicas = models.TextField(blank=True, null=True, verbose_name='Notas técnicas')
    
    class Meta:
        verbose_name = 'Instalación'
        verbose_name_plural = 'Instalaciones'
        ordering = ['-fecha_solicitud']
        indexes = [
            models.Index(fields=['cliente', 'estado']),
            models.Index(fields=['numero_contrato']),
            models.Index(fields=['fecha_programada']),
        ]
    
    def __str__(self):
        return f"{self.cliente.nombre} - {self.plan_nombre} ({self.estado})"
    
    @property
    def esta_activa(self):
        """Verifica si la instalación está activa."""
        return self.estado == 'activa'
    
    @property
    def dias_desde_instalacion(self):
        """Calcula los días desde la instalación."""
        if self.fecha_instalacion:
            return (timezone.now() - self.fecha_instalacion).days
        return None
