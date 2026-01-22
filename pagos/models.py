from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from clientes.models import Cliente
from instalaciones.models import Instalacion
import logging

logger = logging.getLogger(__name__)


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
        constraints = [
            # Constraint para evitar períodos duplicados por cliente e instalación
            # Solo aplica a pagos no cancelados
            models.UniqueConstraint(
                fields=['cliente', 'instalacion', 'periodo_mes', 'periodo_anio'],
                condition=models.Q(estado__in=['pendiente', 'pagado', 'vencido']),
                name='unique_periodo_por_cliente_instalacion_activo'
            ),
            # Constraint alternativo para pagos sin instalación
            models.UniqueConstraint(
                fields=['cliente', 'periodo_mes', 'periodo_anio'],
                condition=models.Q(instalacion__isnull=True, estado__in=['pendiente', 'pagado', 'vencido']),
                name='unique_periodo_por_cliente_sin_instalacion_activo'
            ),
        ]
    
    def __str__(self):
        return f"{self.cliente.nombre_completo} - ${self.monto} - {self.get_estado_display()}"
    
    def clean(self):
        """Validaciones del modelo, incluyendo períodos duplicados."""
        super().clean()
        
        # Validar períodos duplicados (excluyendo cancelados)
        if self.cliente and self.periodo_mes and self.periodo_anio:
            # Buscar pagos duplicados del mismo período
            qs = Pago.objects.filter(
                cliente=self.cliente,
                periodo_mes=self.periodo_mes,
                periodo_anio=self.periodo_anio
            ).exclude(estado='cancelado')  # Excluir cancelados
            
            # Si hay instalación, validar por instalación específica
            if self.instalacion:
                qs = qs.filter(instalacion=self.instalacion)
            else:
                # Si no hay instalación, validar que no haya otro sin instalación
                qs = qs.filter(instalacion__isnull=True)
            
            # Excluir el pago actual si estamos editando
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            
            if qs.exists():
                pago_duplicado = qs.first()
                mensaje = f'Ya existe un pago activo para este cliente'
                if self.instalacion:
                    mensaje += f' e instalación ({self.instalacion.numero_contrato})'
                mensaje += f' en el período {self.get_periodo_mes_display()} {self.periodo_anio}.'
                if pago_duplicado:
                    mensaje += f' Pago existente: {pago_duplicado.concepto} (${pago_duplicado.monto}) - Estado: {pago_duplicado.get_estado_display()}'
                
                raise ValidationError({
                    'periodo_mes': mensaje,
                    'periodo_anio': mensaje,
                })
    
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
        """Actualiza el estado a vencido si corresponde y valida períodos duplicados."""
        # Validar antes de guardar
        self.full_clean()
        
        # Actualizar estado a vencido si corresponde
        if self.estado == 'pendiente' and self.fecha_vencimiento < timezone.now().date():
            self.estado = 'vencido'
        super().save(*args, **kwargs)
    
    @classmethod
    def actualizar_pagos_vencidos(cls):
        """
        Marca automáticamente como vencidos todos los pagos pendientes cuya fecha de vencimiento ya pasó.
        
        Este método se ejecuta automáticamente cuando:
        - Se lista pagos (pago_list, pago_vencidos_list, pago_pendientes_list)
        - Se guarda un pago (método save())
        
        También se puede ejecutar manualmente o mediante un comando de gestión periódico.
        
        Returns:
            int: Cantidad de pagos actualizados a estado 'vencido'
        """
        hoy = timezone.now().date()
        pagos_vencidos = cls.objects.filter(
            estado='pendiente',
            fecha_vencimiento__lt=hoy
        )
        cantidad = pagos_vencidos.update(estado='vencido')
        
        if cantidad > 0:
            logger.info(f'✅ Se actualizaron {cantidad} pago(s) a estado vencido automáticamente.')
        
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
    
    def calcular_fecha_vencimiento(self, mes=None, anio=None):
        """
        Calcula la fecha de vencimiento para un mes y año específicos.
        Si no se proporcionan, calcula para el mes actual.
        
        Args:
            mes (int, optional): Mes (1-12). Si es None, usa el mes actual.
            anio (int, optional): Año. Si es None, usa el año actual.
        
        Returns:
            date: Fecha de vencimiento calculada
        """
        from datetime import date
        from calendar import monthrange
        
        hoy = date.today()
        mes = mes or hoy.month
        anio = anio or hoy.year
        
        # Calcular día de vencimiento ajustado según los días del mes
        dias_en_mes = monthrange(anio, mes)[1]
        dia_vencimiento = min(self.dia_vencimiento, dias_en_mes)
        
        try:
            return date(anio, mes, dia_vencimiento)
        except ValueError:
            # Si el día no es válido (ej: 31 de febrero), usar el último día del mes
            return date(anio, mes, dias_en_mes)
    
    def calcular_proximo_vencimiento(self, desde_fecha=None):
        """
        Calcula la próxima fecha de vencimiento desde una fecha dada.
        Si no se proporciona fecha, usa la fecha actual.
        
        Args:
            desde_fecha (date, optional): Fecha desde la cual calcular. Si es None, usa hoy.
        
        Returns:
            date: Próxima fecha de vencimiento
        """
        from datetime import date
        
        if desde_fecha is None:
            desde_fecha = date.today()
        
        # Calcular vencimiento del mes actual
        fecha_vencimiento_actual = self.calcular_fecha_vencimiento(
            mes=desde_fecha.month,
            anio=desde_fecha.year
        )
        
        # Si ya pasó, calcular para el próximo mes
        if fecha_vencimiento_actual < desde_fecha:
            mes_siguiente = desde_fecha.month + 1
            anio_siguiente = desde_fecha.year
            
            if mes_siguiente > 12:
                mes_siguiente = 1
                anio_siguiente += 1
            
            return self.calcular_fecha_vencimiento(mes=mes_siguiente, anio=anio_siguiente)
        
        return fecha_vencimiento_actual
    
    def generar_pago_para_periodo(self, mes, anio, concepto=None):
        """
        Genera un pago para un período específico basado en este PlanPago.
        
        Args:
            mes (int): Mes del período (1-12)
            anio (int): Año del período
            concepto (str, optional): Concepto del pago. Si es None, se genera automáticamente.
        
        Returns:
            Pago: Instancia del pago creada (no guardada)
        """
        from datetime import date
        
        if concepto is None:
            meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            concepto = f"Pago mensual de servicio - {meses[mes]} {anio}"
        
        fecha_vencimiento = self.calcular_fecha_vencimiento(mes=mes, anio=anio)
        
        return Pago(
            cliente=self.instalacion.cliente,
            instalacion=self.instalacion,
            monto=self.monto_mensual,
            concepto=concepto,
            periodo_mes=mes,
            periodo_anio=anio,
            fecha_vencimiento=fecha_vencimiento,
            estado='pendiente'
        )


class TransaccionPago(models.Model):
    """Modelo para almacenar transacciones de pasarela de pago."""
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('completada', 'Completada'),
        ('fallida', 'Fallida'),
        ('cancelada', 'Cancelada'),
        ('reembolsada', 'Reembolsada'),
    ]
    
    PASARELA_CHOICES = [
        ('stripe', 'Stripe'),
        ('mercadopago', 'Mercado Pago'),
        ('paypal', 'PayPal'),
        ('conekta', 'Conekta'),
    ]
    
    # Relación con pago
    pago = models.ForeignKey(
        Pago,
        on_delete=models.CASCADE,
        related_name='transacciones',
        verbose_name='Pago'
    )
    
    # Información de la transacción
    pasarela = models.CharField(
        max_length=20,
        choices=PASARELA_CHOICES,
        default='stripe',
        verbose_name='Pasarela de pago'
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado de la transacción'
    )
    
    # IDs de la pasarela
    id_transaccion_pasarela = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='ID de transacción (pasarela)',
        help_text='ID único de la transacción en la pasarela de pago'
    )
    
    id_pago_intento = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='ID de intento de pago',
        help_text='ID del intento de pago en la pasarela'
    )
    
    # Información financiera
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Monto de la transacción'
    )
    
    moneda = models.CharField(
        max_length=3,
        default='MXN',
        verbose_name='Moneda',
        help_text='Código de moneda ISO 4217 (MXN, USD, etc.)'
    )
    
    # Información del método de pago
    metodo_pago_tipo = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Tipo de método de pago',
        help_text='card, bank_transfer, etc.'
    )
    
    ultimos_digitos = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name='Últimos 4 dígitos',
        help_text='Últimos 4 dígitos de la tarjeta (si aplica)'
    )
    
    # Información adicional
    datos_respuesta = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Datos de respuesta',
        help_text='Respuesta completa de la pasarela en formato JSON'
    )
    
    mensaje_error = models.TextField(
        blank=True,
        null=True,
        verbose_name='Mensaje de error',
        help_text='Mensaje de error si la transacción falló'
    )
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    fecha_completada = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de completación')
    
    class Meta:
        verbose_name = 'Transacción de Pago'
        verbose_name_plural = 'Transacciones de Pago'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['pago', 'estado']),
            models.Index(fields=['id_transaccion_pasarela']),
            models.Index(fields=['fecha_creacion']),
        ]
    
    def __str__(self):
        return f"{self.pago.cliente.nombre_completo} - ${self.monto} - {self.get_estado_display()}"
    
    def marcar_como_completada(self):
        """Marca la transacción como completada y actualiza el pago."""
        # Verificar que el pago no esté ya pagado (evitar duplicidad)
        if self.pago.estado == 'pagado':
            logger.warning(f"Intento de marcar como completada una transacción para un pago ya pagado (Pago ID: {self.pago.id}, Transacción ID: {self.id})")
            # Solo actualizar el estado de la transacción, no el pago
            self.estado = 'completada'
            self.fecha_completada = timezone.now()
            self.save()
            return
        
        # Verificar que no haya otra transacción completada para este pago
        otra_completada = TransaccionPago.objects.filter(
            pago=self.pago,
            estado='completada'
        ).exclude(id=self.id).exists()
        
        if otra_completada:
            logger.warning(f"Intento de marcar como completada una transacción cuando ya existe otra completada (Pago ID: {self.pago.id}, Transacción ID: {self.id})")
            # Solo actualizar el estado de esta transacción, no el pago
            self.estado = 'completada'
            self.fecha_completada = timezone.now()
            self.save()
            return
        
        # Marcar la transacción como completada
        self.estado = 'completada'
        self.fecha_completada = timezone.now()
        self.save()
        
        # Determinar el método de pago según la pasarela
        metodo_pago = 'tarjeta'  # Por defecto
        if self.pasarela == 'mercadopago':
            metodo_pago = 'tarjeta'  # Mercado Pago principalmente usa tarjetas
        elif self.pasarela == 'paypal':
            metodo_pago = 'tarjeta'  # PayPal también usa tarjetas principalmente
        elif self.pasarela == 'stripe':
            metodo_pago = 'tarjeta'
        
        # Marcar el pago como pagado con el método correcto (solo si no está ya pagado)
        if self.pago.estado != 'pagado':
            self.pago.marcar_como_pagado(
                metodo_pago=metodo_pago,
                referencia=f"{self.pasarela.upper()}-{self.id_transaccion_pasarela}"
            )
            logger.info(f"Pago {self.pago.id} marcado como pagado por transacción {self.id}")
        else:
            logger.warning(f"Pago {self.pago.id} ya estaba pagado, no se actualizó")
    
    def marcar_como_fallida(self, mensaje_error=None):
        """Marca la transacción como fallida."""
        self.estado = 'fallida'
        if mensaje_error:
            self.mensaje_error = mensaje_error
        self.save()
