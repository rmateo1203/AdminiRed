from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from pagos.models import Pago


class TipoNotificacion(models.Model):
    """Tipos de notificaciones disponibles."""
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    plantilla = models.TextField(blank=True, verbose_name='Plantilla de mensaje')
    
    class Meta:
        verbose_name = 'Tipo de Notificación'
        verbose_name_plural = 'Tipos de Notificación'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Notificacion(models.Model):
    """Modelo para gestionar notificaciones a clientes."""
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviada', 'Enviada'),
        ('fallida', 'Fallida'),
        ('cancelada', 'Cancelada'),
    ]
    
    CANAL_CHOICES = [
        ('email', 'Correo electrónico'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('sistema', 'Sistema'),
    ]
    
    # Relaciones
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        verbose_name='Cliente',
        null=True,
        blank=True
    )
    pago = models.ForeignKey(
        Pago,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        verbose_name='Pago relacionado',
        null=True,
        blank=True
    )
    tipo = models.ForeignKey(
        TipoNotificacion,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Tipo de notificación'
    )
    
    # Información de la notificación
    asunto = models.CharField(max_length=200, verbose_name='Asunto')
    mensaje = models.TextField(verbose_name='Mensaje')
    canal = models.CharField(
        max_length=20,
        choices=CANAL_CHOICES,
        default='email',
        verbose_name='Canal de envío'
    )
    
    # Estado y fechas
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_programada = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Fecha programada',
        help_text='Fecha en que se debe enviar la notificación'
    )
    fecha_envio = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Fecha de envío'
    )
    
    # Resultado
    resultado = models.TextField(
        blank=True,
        null=True,
        verbose_name='Resultado',
        help_text='Información sobre el resultado del envío'
    )
    intentos = models.IntegerField(default=0, verbose_name='Intentos de envío')
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['cliente', 'estado']),
            models.Index(fields=['fecha_programada']),
            models.Index(fields=['tipo', 'canal']),
        ]
    
    def __str__(self):
        return f"{self.asunto} - {self.cliente.nombre if self.cliente else 'General'}"
    
    @property
    def esta_pendiente(self):
        """Verifica si la notificación está pendiente."""
        return self.estado == 'pendiente'
    
    @property
    def debe_enviarse(self):
        """Verifica si la notificación debe enviarse ahora."""
        if self.estado != 'pendiente':
            return False
        if self.fecha_programada:
            return timezone.now() >= self.fecha_programada
        return True
    
    def marcar_como_enviada(self, resultado=None):
        """Marca la notificación como enviada."""
        self.estado = 'enviada'
        self.fecha_envio = timezone.now()
        self.intentos += 1
        if resultado:
            self.resultado = resultado
        self.save()
    
    def marcar_como_fallida(self, resultado=None):
        """Marca la notificación como fallida."""
        self.estado = 'fallida'
        self.intentos += 1
        if resultado:
            self.resultado = resultado
        self.save()


class ConfiguracionNotificacion(models.Model):
    """Configuración para notificaciones automáticas."""
    
    tipo_notificacion = models.ForeignKey(
        TipoNotificacion,
        on_delete=models.CASCADE,
        related_name='configuraciones',
        verbose_name='Tipo de notificación'
    )
    activa = models.BooleanField(default=True, verbose_name='Activa')
    dias_antes_vencimiento = models.IntegerField(
        default=3,
        verbose_name='Días antes del vencimiento',
        help_text='Días antes del vencimiento para enviar notificación'
    )
    dias_despues_vencimiento = models.IntegerField(
        default=1,
        verbose_name='Días después del vencimiento',
        help_text='Días después del vencimiento para enviar recordatorio'
    )
    canal_preferido = models.CharField(
        max_length=20,
        choices=Notificacion.CANAL_CHOICES,
        default='email',
        verbose_name='Canal preferido'
    )
    
    class Meta:
        verbose_name = 'Configuración de Notificación'
        verbose_name_plural = 'Configuraciones de Notificación'
    
    def __str__(self):
        return f"{self.tipo_notificacion.nombre} - {self.get_canal_preferido_display()}"
