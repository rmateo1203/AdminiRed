from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords
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
    ip_asignada = models.GenericIPAddressField(
        blank=True, 
        null=True, 
        verbose_name='IP asignada',
        help_text='La IP debe ser única en el sistema'
    )
    mac_equipo = models.CharField(
        max_length=17, 
        blank=True, 
        null=True, 
        verbose_name='MAC del equipo',
        help_text='La MAC debe ser única en el sistema'
    )
    numero_contrato = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True,
        null=True,
        verbose_name='Número de contrato',
        help_text='Se genera automáticamente si se deja vacío'
    )
    
    # Notas
    notas_instalacion = models.TextField(blank=True, null=True, verbose_name='Notas de instalación')
    notas_tecnicas = models.TextField(blank=True, null=True, verbose_name='Notas técnicas')
    
    # Historial de cambios
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Instalación'
        verbose_name_plural = 'Instalaciones'
        ordering = ['-fecha_solicitud']
        indexes = [
            models.Index(fields=['cliente', 'estado']),
            models.Index(fields=['numero_contrato']),
            models.Index(fields=['fecha_programada']),
            models.Index(fields=['ip_asignada']),
            models.Index(fields=['mac_equipo']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['ip_asignada'],
                condition=models.Q(ip_asignada__isnull=False),
                name='unique_ip_when_not_null'
            ),
            models.UniqueConstraint(
                fields=['mac_equipo'],
                condition=models.Q(mac_equipo__isnull=False),
                name='unique_mac_when_not_null'
            ),
        ]
    
    def __str__(self):
        return f"{self.cliente.nombre_completo} - {self.plan_nombre} ({self.estado})"
    
    def clean(self):
        """Validaciones del modelo."""
        super().clean()
        
        # Validar unicidad de IP
        if self.ip_asignada:
            qs = Instalacion.objects.filter(ip_asignada=self.ip_asignada)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({
                    'ip_asignada': 'Esta IP ya está asignada a otra instalación.'
                })
        
        # Validar unicidad de MAC
        if self.mac_equipo:
            # Normalizar MAC (mayúsculas, sin espacios)
            mac_normalizada = self.mac_equipo.upper().replace(' ', '').replace('-', ':')
            self.mac_equipo = mac_normalizada
            
            # Validar formato MAC
            import re
            if not re.match(r'^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$', mac_normalizada):
                raise ValidationError({
                    'mac_equipo': 'Formato de MAC inválido. Use formato: 00:1B:44:11:3A:B7'
                })
            
            qs = Instalacion.objects.filter(mac_equipo=mac_normalizada)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({
                    'mac_equipo': 'Esta MAC ya está asignada a otra instalación.'
                })
    
    def save(self, *args, **kwargs):
        """Genera automáticamente el número de contrato si no se proporciona y registra cambios de estado."""
        # Extraer usuario si se pasa
        user = kwargs.pop('user', None)
        
        # Guardar usuario para que el signal lo use
        if user:
            self._usuario_cambio = user
        
        # Solo generar si es una nueva instalación (no tiene pk) o si no tiene número de contrato
        if not self.numero_contrato:
            try:
                from .services import NumeroContratoService
                self.numero_contrato = NumeroContratoService.generar_numero_contrato(self)
            except Exception as e:
                # Si hay error en el servicio, usar formato simple
                import uuid
                self.numero_contrato = f"CONT-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Validar antes de guardar
        self.full_clean()
        
        super().save(*args, **kwargs)
        
        # El registro de cambio de estado se maneja en signals.py
    
    def _get_estado_display(self, estado):
        """Helper para obtener el display de un estado."""
        return dict(self.ESTADO_CHOICES).get(estado, estado)
    
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
    
    @property
    def proximo_vencimiento(self):
        """
        Calcula la próxima fecha de vencimiento del servicio.
        Basado en PlanPago o el último pago pendiente/vencido.
        """
        from datetime import date
        from calendar import monthrange
        
        hoy = date.today()
        
        # Si tiene PlanPago activo, calcular desde el día de vencimiento
        if hasattr(self, 'plan_pago') and self.plan_pago and self.plan_pago.activo:
            plan_pago = self.plan_pago
            mes_actual = hoy.month
            anio_actual = hoy.year
            
            # Calcular día de vencimiento para este mes
            dias_en_mes = monthrange(anio_actual, mes_actual)[1]
            dia_vencimiento = min(plan_pago.dia_vencimiento, dias_en_mes)
            
            try:
                fecha_vencimiento_mes = date(anio_actual, mes_actual, dia_vencimiento)
            except ValueError:
                fecha_vencimiento_mes = date(anio_actual, mes_actual, dias_en_mes)
            
            # Si el día de vencimiento ya pasó este mes, calcular para el próximo mes
            if fecha_vencimiento_mes < hoy:
                mes_actual += 1
                if mes_actual > 12:
                    mes_actual = 1
                    anio_actual += 1
                dias_en_mes = monthrange(anio_actual, mes_actual)[1]
                dia_vencimiento = min(plan_pago.dia_vencimiento, dias_en_mes)
                try:
                    return date(anio_actual, mes_actual, dia_vencimiento)
                except ValueError:
                    return date(anio_actual, mes_actual, dias_en_mes)
            else:
                return fecha_vencimiento_mes
        
        # Si no tiene PlanPago, buscar el próximo pago pendiente o vencido
        from pagos.models import Pago
        proximo_pago = Pago.objects.filter(
            instalacion=self,
            estado__in=['pendiente', 'vencido']
        ).order_by('fecha_vencimiento').first()
        
        if proximo_pago:
            return proximo_pago.fecha_vencimiento
        
        # Si no hay pagos pendientes, buscar el último pago pagado y calcular el siguiente mes
        ultimo_pago = Pago.objects.filter(
            instalacion=self,
            estado='pagado'
        ).order_by('-fecha_vencimiento').first()
        
        if ultimo_pago:
            # Calcular el siguiente mes desde la última fecha de vencimiento
            mes = ultimo_pago.fecha_vencimiento.month
            anio = ultimo_pago.fecha_vencimiento.year
            
            mes += 1
            if mes > 12:
                mes = 1
                anio += 1
            
            dias_en_mes = monthrange(anio, mes)[1]
            dia = min(ultimo_pago.fecha_vencimiento.day, dias_en_mes)
            try:
                return date(anio, mes, dia)
            except ValueError:
                return date(anio, mes, dias_en_mes)
        
        return None
    
    @property
    def esta_al_dia(self):
        """
        Verifica si el servicio está al día (sin pagos vencidos).
        """
        from pagos.models import Pago
        
        # Si la instalación no está activa, no se considera "al día"
        if self.estado != 'activa':
            return False
        
        # Verificar si hay pagos vencidos sin pagar
        tiene_pagos_vencidos = Pago.objects.filter(
            instalacion=self,
            estado='vencido'
        ).exists()
        
        return not tiene_pagos_vencidos
    
    @property
    def dias_restantes_proximo_vencimiento(self):
        """
        Calcula los días restantes hasta el próximo vencimiento.
        Retorna None si no hay vencimiento próximo.
        """
        proxima_fecha = self.proximo_vencimiento
        if not proxima_fecha:
            return None
        
        from datetime import date
        hoy = date.today()
        delta = proxima_fecha - hoy
        return delta.days
    
    @property
    def monto_pendiente(self):
        """
        Calcula el monto total pendiente (pendientes + vencidos) de esta instalación.
        """
        from django.db.models import Sum
        from pagos.models import Pago
        
        resultado = Pago.objects.filter(
            instalacion=self,
            estado__in=['pendiente', 'vencido']
        ).aggregate(Sum('monto'))
        
        return resultado['monto__sum'] or 0
    
    @property
    def tiene_pago_vencido(self):
        """
        Verifica si tiene algún pago vencido.
        """
        from pagos.models import Pago
        return Pago.objects.filter(
            instalacion=self,
            estado='vencido'
        ).exists()


class MaterialInstalacion(models.Model):
    """Materiales necesarios para una instalación."""
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
        unique_together = ['instalacion', 'material']
        ordering = ['material__nombre']
    
    def __str__(self):
        return f"{self.instalacion.numero_contrato} - {self.material.nombre} ({self.cantidad})"
    
    def clean(self):
        """Validaciones del modelo."""
        if self.material and self.cantidad:
            if self.material.stock_actual < self.cantidad:
                raise ValidationError({
                    'cantidad': f'Stock insuficiente. Disponible: {self.material.stock_actual}, Necesario: {self.cantidad}'
                })


class CambioEstadoInstalacion(models.Model):
    """Historial de cambios de estado de las instalaciones."""
    # Usar string para evitar referencia circular
    instalacion = models.ForeignKey(
        'Instalacion',
        on_delete=models.CASCADE,
        related_name='cambios_estado',
        verbose_name='Instalación'
    )
    estado_anterior = models.CharField(
        max_length=20,
        choices=Instalacion.ESTADO_CHOICES,
        blank=True,
        null=True,
        verbose_name='Estado anterior',
        help_text='Estado anterior (null para instalaciones nuevas)'
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
        estado_anterior_display = self.get_estado_anterior_display() if self.estado_anterior else 'N/A'
        return f"{self.instalacion.numero_contrato}: {estado_anterior_display} → {self.get_estado_nuevo_display()}"


class ConfiguracionNumeroContrato(models.Model):
    """Configuración para la generación automática de números de contrato."""
    
    FORMATO_ANIO_CHOICES = [
        ('completo', 'Completo (YYYY)'),
        ('corto', 'Corto (YY)'),
    ]
    
    RESETEAR_CHOICES = [
        ('nunca', 'Nunca (secuencia continua)'),
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ]
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Configuración activa',
        help_text='Solo una configuración puede estar activa'
    )
    
    # Formato básico
    prefijo = models.CharField(
        max_length=20,
        blank=True,
        default='CONT',
        verbose_name='Prefijo',
        help_text='Prefijo del número de contrato (ej: CONT, INST)'
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
    
    # Componentes del formato
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
        choices=RESETEAR_CHOICES,
        default='mensual',
        verbose_name='Resetear secuencia',
        help_text='Cuándo se reinicia la secuencia numérica'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Configuración de Número de Contrato'
        verbose_name_plural = 'Configuraciones de Número de Contrato'
    
    def __str__(self):
        return f"Configuración: {self.prefijo}{self.separador}..."
    
    def save(self, *args, **kwargs):
        """Asegura que solo una configuración esté activa."""
        if self.activa:
            ConfiguracionNumeroContrato.objects.exclude(pk=self.pk).update(activa=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_activa(cls):
        """Obtiene la configuración activa o crea una por defecto."""
        config = cls.objects.filter(activa=True).first()
        if not config:
            # Crear configuración por defecto
            config = cls.objects.create(
                activa=True,
                prefijo='CONT',
                separador='-',
                incluir_anio=True,
                formato_anio='completo',
                incluir_mes=True,
                incluir_secuencia=True,
                longitud_secuencia=4,
                resetear_secuencia='mensual'
            )
        return config
