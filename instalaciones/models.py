from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.cache import cache
from clientes.models import Cliente

User = get_user_model()


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


class PlanInternet(models.Model):
    """Catálogo de planes de internet disponibles."""
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre del plan')
    velocidad_descarga = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Velocidad de descarga (Mbps)',
        help_text='Velocidad de descarga en Mbps'
    )
    velocidad_subida = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Velocidad de subida (Mbps)',
        blank=True,
        null=True,
        help_text='Velocidad de subida en Mbps (opcional)'
    )
    precio_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio mensual',
        help_text='Precio mensual del plan'
    )
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    activo = models.BooleanField(default=True, verbose_name='Activo', help_text='Indica si el plan está disponible')
    
    class Meta:
        verbose_name = 'Plan de Internet'
        verbose_name_plural = 'Planes de Internet'
        ordering = ['precio_mensual', 'velocidad_descarga']
    
    def __str__(self):
        return f"{self.nombre} - {self.velocidad_descarga} Mbps - ${self.precio_mensual}/mes"


class ConfiguracionNumeroContrato(models.Model):
    """
    Modelo para configurar el formato de generación automática de números de contrato.
    Permite personalizar el formato, prefijo, sufijo, separadores y secuencia.
    """
    
    FORMATO_ANIO_CHOICES = [
        ('completo', 'Completo (YYYY)'),
        ('corto', 'Corto (YY)'),
    ]
    
    RESETEAR_SECUENCIA_CHOICES = [
        ('nunca', 'Nunca (secuencia continua)'),
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ]
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Configuración activa',
        help_text='Solo una configuración puede estar activa'
    )
    
    prefijo = models.CharField(
        max_length=20,
        blank=True,
        default='CONT',
        verbose_name='Prefijo',
        help_text='Prefijo del número de contrato (ej: CONT, INST)'
    )
    
    incluir_anio = models.BooleanField(
        default=True,
        verbose_name='Incluir año',
        help_text='Incluir el año en el número de contrato'
    )
    
    formato_anio = models.CharField(
        max_length=10,
        choices=FORMATO_ANIO_CHOICES,
        default='completo',
        verbose_name='Formato del año'
    )
    
    incluir_mes = models.BooleanField(
        default=True,
        verbose_name='Incluir mes',
        help_text='Incluir el mes en el número de contrato'
    )
    
    incluir_secuencia = models.BooleanField(
        default=True,
        verbose_name='Incluir secuencia',
        help_text='Incluir número secuencial'
    )
    
    longitud_secuencia = models.IntegerField(
        default=4,
        validators=[MinValueValidator(1)],
        verbose_name='Longitud de secuencia',
        help_text='Cantidad de dígitos para el número secuencial'
    )
    
    resetear_secuencia = models.CharField(
        max_length=10,
        choices=RESETEAR_SECUENCIA_CHOICES,
        default='mensual',
        verbose_name='Resetear secuencia',
        help_text='Cuándo se reinicia la secuencia numérica'
    )
    
    separador = models.CharField(
        max_length=5,
        default='-',
        verbose_name='Separador',
        help_text='Carácter separador entre partes (ej: -, _, /)'
    )
    
    sufijo = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Sufijo',
        help_text='Sufijo opcional del número de contrato'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Configuración de Número de Contrato'
        verbose_name_plural = 'Configuraciones de Número de Contrato'
    
    def __str__(self):
        return f"Configuración: {self.prefijo or 'SIN PREFIJO'} - {'Activa' if self.activa else 'Inactiva'}"
    
    def save(self, *args, **kwargs):
        """Solo permitir una configuración activa."""
        if self.activa:
            ConfiguracionNumeroContrato.objects.exclude(pk=self.pk).update(activa=False)
        # Limpiar caché al guardar
        cache.delete('config_numero_contrato')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_activa(cls):
        """Obtiene la configuración activa, usando caché."""
        config = cache.get('config_numero_contrato')
        if config is None:
            config = cls.objects.filter(activa=True).first()
            cache.set('config_numero_contrato', config, 3600)  # Cache por 1 hora
        return config


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
    plan = models.ForeignKey(
        'PlanInternet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='instalaciones',
        verbose_name='Plan de Internet',
        help_text='Plan del catálogo (opcional, puede especificar manualmente)'
    )
    plan_nombre = models.CharField(max_length=100, verbose_name='Nombre del plan', help_text='Nombre personalizado del plan (si no se selecciona del catálogo)')
    velocidad_descarga = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Velocidad de descarga (Mbps)',
        help_text='Se llena automáticamente si se selecciona un plan del catálogo'
    )
    velocidad_subida = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Velocidad de subida (Mbps)',
        blank=True,
        null=True,
        help_text='Se llena automáticamente si se selecciona un plan del catálogo'
    )
    precio_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio mensual',
        help_text='Se llena automáticamente si se selecciona un plan del catálogo'
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
        return f"{self.cliente.nombre_completo} - {self.plan_nombre} ({self.estado})"
    
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


class MaterialInstalacion(models.Model):
    """
    Modelo para relacionar materiales del inventario con instalaciones.
    Permite registrar qué materiales se utilizan en cada instalación.
    """
    
    instalacion = models.ForeignKey(
        Instalacion,
        on_delete=models.CASCADE,
        related_name='materiales',
        verbose_name='Instalación'
    )
    
    material = models.ForeignKey(
        'inventario.Material',
        on_delete=models.CASCADE,
        related_name='instalaciones',
        verbose_name='Material'
    )
    
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad',
        help_text='Cantidad necesaria del material'
    )
    
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas',
        help_text='Notas adicionales sobre el uso de este material'
    )
    
    class Meta:
        verbose_name = 'Material de Instalación'
        verbose_name_plural = 'Materiales de Instalación'
        ordering = ['material__nombre']
        unique_together = [['instalacion', 'material']]
    
    def __str__(self):
        return f"{self.instalacion.numero_contrato} - {self.material.nombre} ({self.cantidad})"


class CambioEstadoInstalacion(models.Model):
    """
    Modelo para registrar el historial de cambios de estado de las instalaciones.
    Se crea automáticamente mediante signals cuando cambia el estado de una instalación.
    """
    
    instalacion = models.ForeignKey(
        Instalacion,
        on_delete=models.CASCADE,
        related_name='cambios_estado',
        verbose_name='Instalación'
    )
    
    estado_anterior = models.CharField(
        max_length=20,
        choices=Instalacion.ESTADO_CHOICES,
        verbose_name='Estado anterior'
    )
    
    estado_nuevo = models.CharField(
        max_length=20,
        choices=Instalacion.ESTADO_CHOICES,
        verbose_name='Estado nuevo'
    )
    
    fecha_cambio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de cambio'
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario',
        help_text='Usuario que realizó el cambio'
    )
    
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas',
        help_text='Notas adicionales sobre el cambio de estado'
    )
    
    class Meta:
        verbose_name = 'Cambio de Estado'
        verbose_name_plural = 'Cambios de Estado'
        ordering = ['-fecha_cambio']
        indexes = [
            models.Index(fields=['instalacion', 'fecha_cambio']),
        ]
    
    def __str__(self):
        estado_anterior_display = dict(Instalacion.ESTADO_CHOICES).get(self.estado_anterior, self.estado_anterior)
        estado_nuevo_display = dict(Instalacion.ESTADO_CHOICES).get(self.estado_nuevo, self.estado_nuevo)
        return f"{self.instalacion.numero_contrato} - {estado_anterior_display} → {estado_nuevo_display}"
