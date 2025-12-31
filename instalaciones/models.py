from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from clientes.models import Cliente
import re
from django.core.cache import cache


class ConfiguracionNumeroContrato(models.Model):
    """Configuración para la generación automática de números de contrato."""
    
    activa = models.BooleanField(default=True, verbose_name='Configuración activa')
    formato = models.CharField(
        max_length=200,
        default='INST-{YYYY}{MM}{DD}-{####}',
        verbose_name='Formato del número de contrato',
        help_text='Variables disponibles: {YYYY} (año), {YY} (año 2 dígitos), {MM} (mes), {DD} (día), {####} (número secuencial), {PREFIJO} (prefijo personalizado)'
    )
    prefijo = models.CharField(
        max_length=20,
        default='INST',
        blank=True,
        verbose_name='Prefijo personalizado',
        help_text='Prefijo opcional (se usa con {PREFIJO})'
    )
    numero_inicial = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Número inicial',
        help_text='Número inicial para la secuencia (ej: 1, 100, 1000)'
    )
    digitos_secuencia = models.IntegerField(
        default=4,
        validators=[MinValueValidator(1), MinValueValidator(10)],
        verbose_name='Dígitos de secuencia',
        help_text='Cantidad de dígitos para el número secuencial (1-10)'
    )
    reiniciar_diario = models.BooleanField(
        default=True,
        verbose_name='Reiniciar secuencia diariamente',
        help_text='Si está activo, la secuencia se reinicia cada día'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración de Número de Contrato'
        verbose_name_plural = 'Configuraciones de Número de Contrato'
    
    def __str__(self):
        return f"Configuración: {self.formato}"
    
    def save(self, *args, **kwargs):
        # Solo permitir una configuración activa
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
            if config is None:
                # Crear configuración por defecto si no existe
                config = cls.objects.create(
                    activa=True,
                    formato='INST-{YYYY}{MM}{DD}-{####}',
                    prefijo='INST',
                    numero_inicial=1,
                    digitos_secuencia=4,
                    reiniciar_diario=True
                )
            cache.set('config_numero_contrato', config, 3600)  # Cache por 1 hora
        return config


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
    numero_contrato = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True,
        null=False,  # No permitir NULL, pero sí permitir vacío (se genera automáticamente)
        default='',  # Valor por defecto vacío
        verbose_name='Número de contrato',
        help_text='Se generará automáticamente si se deja vacío'
    )
    
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
    
    def clean(self):
        """Validaciones del modelo."""
        # Validar MAC address si está presente
        if self.mac_equipo:
            mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
            if not re.match(mac_pattern, self.mac_equipo):
                raise ValidationError({
                    'mac_equipo': 'Formato de MAC address inválido. Use: XX:XX:XX:XX:XX:XX'
                })
        
        # Validar coordenadas si están presentes
        if self.coordenadas:
            try:
                coords = self.coordenadas.replace(' ', '').split(',')
                if len(coords) != 2:
                    raise ValueError()
                lat = float(coords[0])
                lon = float(coords[1])
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    raise ValueError()
            except (ValueError, IndexError):
                raise ValidationError({
                    'coordenadas': 'Formato de coordenadas inválido. Use: latitud,longitud'
                })
            except:
                raise ValidationError({
                    'coordenadas': 'Formato de coordenadas inválido.'
                })
    
    def save(self, *args, **kwargs):
        """Genera número de contrato automáticamente si no existe."""
        if not self.numero_contrato or self.numero_contrato.strip() == '':
            from instalaciones.services import NumeroContratoService
            self.numero_contrato = NumeroContratoService.generar_numero_contrato()
        
        # Si se selecciona un plan pero no hay plan_nombre, usar el nombre del plan
        if self.plan and not self.plan_nombre:
            self.plan_nombre = self.plan.nombre
        
        # Si hay plan, actualizar campos automáticamente si están vacíos
        if self.plan:
            if not self.velocidad_descarga:
                self.velocidad_descarga = self.plan.velocidad_descarga
            if not self.velocidad_subida and self.plan.velocidad_subida:
                self.velocidad_subida = self.plan.velocidad_subida
            if not self.precio_mensual:
                self.precio_mensual = self.plan.precio_mensual
        
        super().save(*args, **kwargs)
