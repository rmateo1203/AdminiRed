"""Señales para el modelo Instalacion."""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Instalacion, CambioEstadoInstalacion

User = get_user_model()


@receiver(pre_save, sender=Instalacion)
def capturar_estado_anterior(sender, instance, **kwargs):
    """Captura el estado anterior antes de guardar para poder compararlo."""
    if instance.pk:
        try:
            instancia_anterior = Instalacion.objects.get(pk=instance.pk)
            instance._estado_anterior = instancia_anterior.estado
        except Instalacion.DoesNotExist:
            instance._estado_anterior = None
    else:
        instance._estado_anterior = None


@receiver(post_save, sender=Instalacion)
def registrar_cambio_estado_instalacion(sender, instance, created, **kwargs):
    """Registra cambios de estado de instalaciones."""
    # Si es nueva instalación, registrar el estado inicial
    if created:
        CambioEstadoInstalacion.objects.create(
            instalacion=instance,
            estado_anterior=None,  # None es válido ahora que el campo permite null
            estado_nuevo=instance.estado,
            usuario=getattr(instance, '_usuario_cambio', None),
            notas=f'Instalación creada con estado: {instance.get_estado_display()}'
        )
        return
    
    # Verificar si hay cambio de estado
    estado_anterior = getattr(instance, '_estado_anterior', None)
    if estado_anterior and estado_anterior != instance.estado:
        CambioEstadoInstalacion.objects.create(
            instalacion=instance,
            estado_anterior=estado_anterior,
            estado_nuevo=instance.estado,
            usuario=getattr(instance, '_usuario_cambio', None),
            notas=f'Cambio automático de estado: {dict(Instalacion.ESTADO_CHOICES).get(estado_anterior, estado_anterior)} → {instance.get_estado_display()}'
        )

