from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from clientes.models import Cliente
from instalaciones.models import Instalacion


class Pago(models.Model):
    """Modelo para gestionar pagos de clientes."""
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia bancaria'),
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('deposito', 'Depósito'),
        ('otro', 'Otro'),
    ]
    
    # Relaciones
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name='Cliente'
    )
    instalacion = models.ForeignKey(
        Instalacion,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name='Instalación',
        null=True,
        blank=True
    )
    
    # Información del pago
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Monto'
    )
    concepto = models.CharField(max_length=200, verbose_name='Concepto')
    PERIODO_MES_CHOICES = [
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre'),
    ]
    
    periodo_mes = models.IntegerField(
        verbose_name='Mes',
        choices=PERIODO_MES_CHOICES
    )
    periodo_anio = models.IntegerField(
        verbose_name='Año',
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )
    
    # Fechas
    fecha_vencimiento = models.DateField(verbose_name='Fecha de vencimiento')
    fecha_pago = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de pago')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    
    # Estado y método
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODO_PAGO_CHOICES,
        blank=True,
        null=True,
        verbose_name='Método de pago'
    )
    
    # Información adicional
    referencia_pago = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Referencia de pago',
        help_text='Número de transacción, referencia bancaria, etc.'
    )
    notas = models.TextField(blank=True, null=True, verbose_name='Notas')
    
    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_vencimiento', '-fecha_registro']
        indexes = [
            models.Index(fields=['cliente', 'estado']),
            models.Index(fields=['fecha_vencimiento']),
            models.Index(fields=['periodo_anio', 'periodo_mes']),
        ]
    
    def __str__(self):
        return f"{self.cliente.nombre_completo} - ${self.monto} - {self.get_estado_display()}"
    
    @property
    def esta_vencido(self):
        """Verifica si el pago está vencido."""
        if self.estado == 'pagado':
            return False
        return self.fecha_vencimiento < timezone.now().date()
    
    @property
    def dias_vencido(self):
        """Calcula los días de vencimiento."""
        if self.estado != 'pagado' and self.fecha_vencimiento < timezone.now().date():
            return (timezone.now().date() - self.fecha_vencimiento).days
        return 0
    
    def marcar_como_pagado(self, metodo_pago=None, referencia=None):
        """Marca el pago como pagado."""
        self.estado = 'pagado'
        self.fecha_pago = timezone.now()
        if metodo_pago:
            self.metodo_pago = metodo_pago
        if referencia:
            self.referencia_pago = referencia
        self.save()
    
    def save(self, *args, **kwargs):
        """Actualiza el estado a vencido si corresponde."""
        if self.estado == 'pendiente' and self.fecha_vencimiento < timezone.now().date():
            self.estado = 'vencido'
        super().save(*args, **kwargs)
    
    @classmethod
    def actualizar_pagos_vencidos(cls):
        """Marca automáticamente como vencidos todos los pagos pendientes cuya fecha de vencimiento ya pasó."""
        hoy = timezone.now().date()
        pagos_vencidos = cls.objects.filter(
            estado='pendiente',
            fecha_vencimiento__lt=hoy
        )
        cantidad = pagos_vencidos.update(estado='vencido')
        return cantidad


class PlanPago(models.Model):
    """Modelo para definir planes de pago recurrentes."""
    
    instalacion = models.OneToOneField(
        Instalacion,
        on_delete=models.CASCADE,
        related_name='plan_pago',
        verbose_name='Instalación'
    )
    monto_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Monto mensual'
    )
    dia_vencimiento = models.IntegerField(
        verbose_name='Día de vencimiento',
        help_text='Día del mes en que vence el pago (1-31)',
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        verbose_name = 'Plan de Pago'
        verbose_name_plural = 'Planes de Pago'
    
    def __str__(self):
        return f"{self.instalacion.cliente.nombre} - ${self.monto_mensual}/mes"
