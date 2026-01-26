"""Señales para el modelo Instalacion."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Instalacion, CambioEstadoInstalacion


@receiver(post_save, sender=Instalacion)
def registrar_cambio_estado_instalacion(sender, instance, created, **kwargs):
    """Registra cambios de estado de instalaciones."""
    if created:
        return  # No registrar cambios en creación
    
    # Verificar si hay cambio de estado
    if hasattr(instance, '_estado_anterior') and instance._estado_anterior != instance.estado:
        CambioEstadoInstalacion.objects.create(
            instalacion=instance,
            estado_anterior=instance._estado_anterior,
            estado_nuevo=instance.estado,
            usuario=getattr(instance, '_usuario_cambio', None),
            notas=f'Cambio automático de estado: {instance._get_estado_display(instance._estado_anterior)} → {instance.get_estado_display()}'
        )

