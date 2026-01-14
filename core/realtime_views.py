"""
Vistas para actualizaciones en tiempo real.
Proporciona endpoints JSON para verificar cambios en los modelos.
"""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from clientes.models import Cliente
from pagos.models import Pago
from instalaciones.models import Instalacion
from notificaciones.models import Notificacion


@login_required
def check_updates(request):
    """
    Endpoint para verificar actualizaciones recientes.
    Retorna un JSON con información sobre cambios recientes.
    """
    # Obtener el timestamp de la última actualización del cliente
    last_check = request.GET.get('last_check')
    if last_check:
        try:
            last_check = timezone.datetime.fromisoformat(last_check.replace('Z', '+00:00'))
        except:
            last_check = timezone.now() - timedelta(minutes=5)
    else:
        last_check = timezone.now() - timedelta(minutes=5)
    
    updates = {
        'has_updates': False,
        'timestamp': timezone.now().isoformat(),
        'changes': {}
    }
    
    # Verificar cambios en clientes (últimos 5 minutos)
    clientes_updated = Cliente.objects.filter(
        updated_at__gte=last_check
    ).count()
    if clientes_updated > 0:
        updates['has_updates'] = True
        updates['changes']['clientes'] = {
            'count': clientes_updated,
            'message': f'{clientes_updated} cliente(s) actualizado(s)'
        }
    
    # Verificar cambios en pagos (últimos 5 minutos)
    # Pago solo tiene fecha_registro, no updated_at
    pagos_updated = Pago.objects.filter(
        fecha_registro__gte=last_check
    ).count()
    if pagos_updated > 0:
        updates['has_updates'] = True
        updates['changes']['pagos'] = {
            'count': pagos_updated,
            'message': f'{pagos_updated} pago(s) actualizado(s)'
        }
    
    # Verificar cambios en instalaciones (últimos 5 minutos)
    # Instalacion puede no tener updated_at, usar fecha_solicitud como fallback
    try:
        instalaciones_updated = Instalacion.objects.filter(
            fecha_solicitud__gte=last_check
        ).count()
    except:
        instalaciones_updated = 0
    if instalaciones_updated > 0:
        updates['has_updates'] = True
        updates['changes']['instalaciones'] = {
            'count': instalaciones_updated,
            'message': f'{instalaciones_updated} instalación(es) actualizada(s)'
        }
    
    # Verificar nuevas notificaciones (últimos 5 minutos)
    notificaciones_nuevas = Notificacion.objects.filter(
        fecha_creacion__gte=last_check
    ).count()
    if notificaciones_nuevas > 0:
        updates['has_updates'] = True
        updates['changes']['notificaciones'] = {
            'count': notificaciones_nuevas,
            'message': f'{notificaciones_nuevas} notificación(es) nueva(s)'
        }
    
    return JsonResponse(updates)


@login_required
def get_model_updates(request, model_name):
    """
    Endpoint para obtener actualizaciones de un modelo específico.
    """
    model_name = model_name.lower()
    last_check = request.GET.get('last_check')
    
    if last_check:
        try:
            last_check = timezone.datetime.fromisoformat(last_check.replace('Z', '+00:00'))
        except:
            last_check = timezone.now() - timedelta(minutes=5)
    else:
        last_check = timezone.now() - timedelta(minutes=5)
    
    updates = {
        'model': model_name,
        'timestamp': timezone.now().isoformat(),
        'items': []
    }
    
    if model_name == 'clientes':
        items = Cliente.objects.filter(updated_at__gte=last_check)[:50]
        updates['items'] = [
            {
                'id': item.id,
                'nombre': item.nombre_completo,
                'updated_at': item.updated_at.isoformat()
            }
            for item in items
        ]
    elif model_name == 'pagos':
        items = Pago.objects.filter(fecha_registro__gte=last_check)[:50]
        updates['items'] = [
            {
                'id': item.id,
                'cliente': item.cliente.nombre_completo,
                'monto': str(item.monto),
                'estado': item.estado,
                'updated_at': item.fecha_registro.isoformat()
            }
            for item in items
        ]
    elif model_name == 'instalaciones':
        items = Instalacion.objects.filter(fecha_solicitud__gte=last_check)[:50]
        updates['items'] = [
            {
                'id': item.id,
                'cliente': item.cliente.nombre_completo,
                'estado': item.estado,
                'updated_at': item.fecha_solicitud.isoformat()
            }
            for item in items
        ]
    
    return JsonResponse(updates)

