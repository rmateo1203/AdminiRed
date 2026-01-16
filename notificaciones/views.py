from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Notificacion
from .forms import NotificacionForm
from .services import NotificationService


@login_required
def notificacion_list(request):
    """Lista todas las notificaciones con búsqueda y filtros."""
    notificaciones = Notificacion.objects.select_related('cliente', 'tipo', 'pago').all()
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        notificaciones = notificaciones.filter(
            Q(asunto__icontains=query) |
            Q(mensaje__icontains=query) |
            Q(cliente__nombre__icontains=query) |
            Q(cliente__apellido1__icontains=query) |
            Q(cliente__apellido2__icontains=query)
        )
    
    # Filtro por estado
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        notificaciones = notificaciones.filter(estado=estado_filter)
    
    # Filtro por canal
    canal_filter = request.GET.get('canal', '')
    if canal_filter:
        notificaciones = notificaciones.filter(canal=canal_filter)
    
    # Ordenamiento
    orden = request.GET.get('orden', '-fecha_creacion')
    notificaciones = notificaciones.order_by(orden)
    
    # Calcular estadísticas
    total_notificaciones = notificaciones.count()
    pendientes = notificaciones.filter(estado='pendiente').count()
    enviadas = notificaciones.filter(estado='enviada').count()
    
    context = {
        'notificaciones': notificaciones,
        'query': query,
        'estado_filter': estado_filter,
        'canal_filter': canal_filter,
        'orden': orden,
        'estados': Notificacion.ESTADO_CHOICES,
        'canales': Notificacion.CANAL_CHOICES,
        'total_notificaciones': total_notificaciones,
        'pendientes': pendientes,
        'enviadas': enviadas,
    }
    
    return render(request, 'notificaciones/notificacion_list.html', context)


@login_required
def notificacion_detail(request, pk):
    """Muestra los detalles de una notificación."""
    notificacion = get_object_or_404(
        Notificacion.objects.select_related('cliente', 'tipo', 'pago'),
        pk=pk
    )
    
    context = {
        'notificacion': notificacion,
    }
    
    return render(request, 'notificaciones/notificacion_detail.html', context)


@login_required
def notificacion_create(request, cliente_id=None):
    """Crea una nueva notificación."""
    cliente_pre_seleccionado = None
    if cliente_id:
        from clientes.models import Cliente
        try:
            cliente_pre_seleccionado = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente no encontrado.')
            return redirect('notificaciones:notificacion_list')
    
    if request.method == 'POST':
        form = NotificacionForm(request.POST, cliente_id=cliente_id)
        # Si viene de un cliente específico, forzar el cliente en el formulario
        if cliente_pre_seleccionado:
            form.data = form.data.copy()
            form.data['cliente'] = cliente_pre_seleccionado.pk
        
        if form.is_valid():
            notificacion = form.save()
            messages.success(request, f'Notificación "{notificacion.asunto}" creada exitosamente.')
            return redirect('notificaciones:notificacion_detail', pk=notificacion.pk)
    else:
        form = NotificacionForm(cliente_id=cliente_id)
    
    context = {
        'form': form,
        'title': 'Nueva Notificación',
        'cliente_pre_seleccionado': cliente_pre_seleccionado,
    }
    
    return render(request, 'notificaciones/notificacion_form.html', context)


@login_required
def notificacion_update(request, pk):
    """Actualiza una notificación existente."""
    notificacion = get_object_or_404(Notificacion, pk=pk)
    
    if request.method == 'POST':
        form = NotificacionForm(request.POST, instance=notificacion)
        if form.is_valid():
            notificacion = form.save()
            messages.success(request, f'Notificación "{notificacion.asunto}" actualizada exitosamente.')
            return redirect('notificaciones:notificacion_detail', pk=notificacion.pk)
    else:
        form = NotificacionForm(instance=notificacion)
    
    context = {
        'form': form,
        'notificacion': notificacion,
        'title': 'Editar Notificación',
    }
    
    return render(request, 'notificaciones/notificacion_form.html', context)


@login_required
def notificacion_delete(request, pk):
    """Elimina una notificación."""
    notificacion = get_object_or_404(Notificacion, pk=pk)
    
    if request.method == 'POST':
        notificacion_str = str(notificacion)
        notificacion.delete()
        messages.success(request, f'Notificación "{notificacion_str}" eliminada exitosamente.')
        return redirect('notificaciones:notificacion_list')
    
    context = {
        'notificacion': notificacion,
    }
    
    return render(request, 'notificaciones/notificacion_confirm_delete.html', context)


@login_required
def notificacion_send(request, pk):
    """Envía una notificación manualmente."""
    notificacion = get_object_or_404(Notificacion, pk=pk)
    
    if notificacion.estado != 'pendiente':
        messages.warning(request, f'La notificación ya fue procesada (estado: {notificacion.get_estado_display()}).')
        return redirect('notificaciones:notificacion_detail', pk=notificacion.pk)
    
    # Enviar notificación
    resultado = NotificationService.send_notification(notificacion)
    
    if resultado.get('success'):
        messages.success(request, f'Notificación enviada exitosamente: {resultado.get("message", "Enviado")}')
    else:
        messages.error(request, f'Error al enviar notificación: {resultado.get("error", "Error desconocido")}')
    
    return redirect('notificaciones:notificacion_detail', pk=notificacion.pk)
