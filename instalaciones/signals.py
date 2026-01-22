"""Señales para el modelo Instalacion."""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Instalacion, CambioEstadoInstalacion
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Instalacion)
def capturar_estado_anterior(sender, instance, **kwargs):
    """Captura el estado anterior y precio anterior antes de guardar para poder compararlos."""
    if instance.pk:
        try:
            instancia_anterior = Instalacion.objects.get(pk=instance.pk)
            instance._estado_anterior = instancia_anterior.estado
            instance._precio_anterior = instancia_anterior.precio_mensual
        except Instalacion.DoesNotExist:
            instance._estado_anterior = None
            instance._precio_anterior = None
    else:
        instance._estado_anterior = None
        instance._precio_anterior = None


@receiver(post_save, sender=Instalacion)
def registrar_cambio_estado_instalacion(sender, instance, created, **kwargs):
    """
    Registra cambios de estado de instalaciones y crea PlanPago automáticamente.
    
    FLUJO COMPLETO:
    1. Cliente se crea
    2. Instalación se crea (asociada al cliente, estado inicial: pendiente)
    3. Cuando instalación cambia a estado 'activa':
       - Se establece fecha_activacion (en el método save() del modelo)
       - Se crea PlanPago automáticamente en tabla pagos_planpago
       - dia_vencimiento = día de fecha_activacion
       - monto_mensual = precio_mensual de la instalación
    4. A partir de fecha_activacion, el usuario tiene servicio de internet
    5. Se pueden generar pagos mensuales usando: python manage.py generar_pagos
    """
    # Si es nueva instalación, registrar el estado inicial
    if created:
        CambioEstadoInstalacion.objects.create(
            instalacion=instance,
            estado_anterior=None,  # None es válido ahora que el campo permite null
            estado_nuevo=instance.estado,
            usuario=getattr(instance, '_usuario_cambio', None),
            notas=f'Instalación creada con estado: {instance.get_estado_display()}'
        )
        
        # Si se crea directamente como activa, crear PlanPago
        # IMPORTANTE: fecha_activacion debe estar establecida (se hace en save())
        if instance.estado == 'activa':
            if instance.precio_mensual and instance.precio_mensual > 0:
                crear_plan_pago_automatico(instance)
            else:
                logger.warning(
                    f'⚠️ Instalación {instance.numero_contrato} se creó como activa pero '
                    f'no tiene precio_mensual válido. No se creará PlanPago.'
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
        
        # Si cambió a estado "activa", crear PlanPago automáticamente
        # IMPORTANTE: fecha_activacion ya debe estar establecida (se hace en save() del modelo)
        if instance.estado == 'activa' and estado_anterior != 'activa':
            logger.info(
                f'🔄 Instalación {instance.numero_contrato} cambió a estado ACTIVA. '
                f'Fecha de activación: {instance.fecha_activacion.strftime("%d/%m/%Y %H:%M") if instance.fecha_activacion else "No establecida"}. '
                f'Creando PlanPago automáticamente...'
            )
            crear_plan_pago_automatico(instance)
        
        # Si cambió a estado suspendida o cancelada, desactivar PlanPago
        elif instance.estado in ['suspendida', 'cancelada'] and estado_anterior == 'activa':
            desactivar_plan_pago_por_estado(instance, instance.estado)
        
        # Si cambió de suspendida/cancelada a activa, reactivar PlanPago
        elif instance.estado == 'activa' and estado_anterior in ['suspendida', 'cancelada']:
            reactivar_plan_pago(instance)
        
        # Si cambió el precio_mensual y tiene PlanPago, actualizarlo
        precio_anterior = getattr(instance, '_precio_anterior', None)
        if precio_anterior is not None and precio_anterior != instance.precio_mensual:
            sincronizar_precio_plan_pago(instance)


def crear_plan_pago_automatico(instalacion):
    """
    Crea automáticamente un PlanPago cuando una instalación se activa.
    
    FLUJO:
    1. Cliente se crea
    2. Instalación se crea (asociada al cliente)
    3. Cuando instalación se activa (estado = 'activa'):
       - Se establece fecha_activacion (si no existe)
       - Se crea PlanPago en tabla pagos_planpago
       - dia_vencimiento = día de fecha_activacion
       - monto_mensual = precio_mensual de la instalación
    4. A partir de fecha_activacion, el usuario tiene el servicio
    5. Se pueden generar pagos mensuales desde el PlanPago
    
    Args:
        instalacion: Instancia de Instalacion que se acaba de activar
    
    Returns:
        PlanPago: El plan de pago creado, o None si no se pudo crear
    """
    # Verificar que no tenga ya un PlanPago
    try:
        if hasattr(instalacion, 'plan_pago') and instalacion.plan_pago:
            logger.info(
                f'ℹ️ La instalación {instalacion.numero_contrato} (Cliente: {instalacion.cliente.nombre_completo}) '
                f'ya tiene un PlanPago registrado. No se creará uno nuevo.'
            )
            return instalacion.plan_pago
    except Exception as e:
        logger.warning(f'Error al verificar PlanPago existente: {e}')
    
    # Verificar que tenga precio_mensual válido
    if not instalacion.precio_mensual or instalacion.precio_mensual <= 0:
        logger.warning(
            f'⚠️ No se puede crear PlanPago para instalación {instalacion.numero_contrato}: '
            f'precio_mensual inválido (${instalacion.precio_mensual}). '
            f'El PlanPago solo se crea cuando precio_mensual > 0.'
        )
        return None
    
    # Verificar que tenga fecha_activacion (debería estar establecida antes de llegar aquí)
    if not instalacion.fecha_activacion:
        logger.warning(
            f'⚠️ Instalación {instalacion.numero_contrato} se activó pero no tiene fecha_activacion. '
            f'Se usará la fecha actual para calcular el día de vencimiento.'
        )
        fecha_referencia = timezone.now().date()
    else:
        fecha_referencia = instalacion.fecha_activacion.date()
    
    try:
        from pagos.models import PlanPago
        
        # El día de vencimiento se calcula desde la fecha de activación
        # Ejemplo: Si se activa el día 15, todos los meses vence el día 15
        dia_vencimiento = fecha_referencia.day
        
        # Crear el PlanPago (se registra en tabla pagos_planpago)
        plan_pago = PlanPago.objects.create(
            instalacion=instalacion,
            monto_mensual=instalacion.precio_mensual,
            dia_vencimiento=dia_vencimiento,
            activo=True
        )
        
        logger.info(
            f'✅ PlanPago creado automáticamente para instalación {instalacion.numero_contrato}:\n'
            f'   • Cliente: {instalacion.cliente.nombre_completo}\n'
            f'   • Fecha de activación: {fecha_referencia.strftime("%d/%m/%Y")}\n'
            f'   • Monto mensual: ${plan_pago.monto_mensual}/mes\n'
            f'   • Día de vencimiento: día {plan_pago.dia_vencimiento} de cada mes\n'
            f'   • A partir de {fecha_referencia.strftime("%d/%m/%Y")} el cliente tiene servicio activo'
        )
        
        return plan_pago
        
    except Exception as e:
        logger.error(
            f'❌ Error al crear PlanPago automático para instalación {instalacion.numero_contrato}: {str(e)}',
            exc_info=True
        )
        return None


def desactivar_plan_pago_por_estado(instalacion, nuevo_estado):
    """
    Desactiva el PlanPago cuando una instalación se suspende o cancela.
    
    Args:
        instalacion: Instancia de Instalacion
        nuevo_estado: Nuevo estado de la instalación
    """
    try:
        if hasattr(instalacion, 'plan_pago') and instalacion.plan_pago:
            plan_pago = instalacion.plan_pago
            if plan_pago.activo:
                plan_pago.activo = False
                plan_pago.save()
                logger.info(
                    f'PlanPago desactivado para instalación {instalacion.numero_contrato} '
                    f'debido a cambio de estado a: {nuevo_estado}'
                )
    except Exception as e:
        logger.error(
            f'Error al desactivar PlanPago para instalación {instalacion.numero_contrato}: {str(e)}',
            exc_info=True
        )


def reactivar_plan_pago(instalacion):
    """
    Reactiva el PlanPago cuando una instalación vuelve a estado activa.
    
    Args:
        instalacion: Instancia de Instalacion
    """
    try:
        if hasattr(instalacion, 'plan_pago') and instalacion.plan_pago:
            plan_pago = instalacion.plan_pago
            if not plan_pago.activo:
                plan_pago.activo = True
                plan_pago.save()
                logger.info(
                    f'PlanPago reactivado para instalación {instalacion.numero_contrato}'
                )
        else:
            # Si no tiene PlanPago, crearlo
            crear_plan_pago_automatico(instalacion)
    except Exception as e:
        logger.error(
            f'Error al reactivar PlanPago para instalación {instalacion.numero_contrato}: {str(e)}',
            exc_info=True
        )


def sincronizar_precio_plan_pago(instalacion):
    """
    Sincroniza el monto_mensual del PlanPago con el precio_mensual de la instalación.
    
    Args:
        instalacion: Instancia de Instalacion
    """
    try:
        if hasattr(instalacion, 'plan_pago') and instalacion.plan_pago:
            plan_pago = instalacion.plan_pago
            
            # Solo actualizar si el precio cambió y es válido
            if instalacion.precio_mensual and instalacion.precio_mensual > 0:
                if plan_pago.monto_mensual != instalacion.precio_mensual:
                    monto_anterior = plan_pago.monto_mensual
                    plan_pago.monto_mensual = instalacion.precio_mensual
                    plan_pago.save()
                    logger.info(
                        f'Precio de PlanPago actualizado para instalación {instalacion.numero_contrato}: '
                        f'${monto_anterior} → ${instalacion.precio_mensual}'
                    )
            else:
                logger.warning(
                    f'No se puede sincronizar precio: instalación {instalacion.numero_contrato} '
                    f'tiene precio_mensual inválido: ${instalacion.precio_mensual}'
                )
    except Exception as e:
        logger.error(
            f'Error al sincronizar precio de PlanPago para instalación {instalacion.numero_contrato}: {str(e)}',
            exc_info=True
        )

