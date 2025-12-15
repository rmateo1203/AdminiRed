from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Instalacion, PlanInternet
from .forms import InstalacionForm


@login_required
def instalacion_list(request):
    """Lista todas las instalaciones con búsqueda y filtros."""
    instalaciones = Instalacion.objects.select_related('cliente', 'tipo_instalacion').all()
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        instalaciones = instalaciones.filter(
            Q(cliente__nombre__icontains=query) |
            Q(cliente__apellido1__icontains=query) |
            Q(cliente__apellido2__icontains=query) |
            Q(plan_nombre__icontains=query) |
            Q(numero_contrato__icontains=query) |
            Q(direccion_instalacion__icontains=query)
        )
    
    # Filtro por estado
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        instalaciones = instalaciones.filter(estado=estado_filter)
    
    # Ordenamiento
    orden = request.GET.get('orden', '-fecha_solicitud')
    instalaciones = instalaciones.order_by(orden)
    
    # Calcular estadísticas
    total_instalaciones = instalaciones.count()
    activas = instalaciones.filter(estado='activa').count()
    pendientes = instalaciones.filter(estado__in=['pendiente', 'programada', 'en_proceso']).count()
    
    context = {
        'instalaciones': instalaciones,
        'query': query,
        'estado_filter': estado_filter,
        'orden': orden,
        'estados': Instalacion.ESTADO_CHOICES,
        'total_instalaciones': total_instalaciones,
        'activas': activas,
        'pendientes': pendientes,
    }
    
    return render(request, 'instalaciones/instalacion_list.html', context)


@login_required
def instalacion_detail(request, pk):
    """Muestra los detalles de una instalación."""
    instalacion = get_object_or_404(Instalacion.objects.select_related('cliente', 'tipo_instalacion'), pk=pk)
    
    # Obtener pagos relacionados si existen
    pagos = instalacion.pagos.all() if hasattr(instalacion, 'pagos') else []
    
    context = {
        'instalacion': instalacion,
        'pagos': pagos,
    }
    
    return render(request, 'instalaciones/instalacion_detail.html', context)


@login_required
def instalacion_create(request, cliente_id=None):
    """Crea una nueva instalación."""
    from clientes.models import Cliente
    
    cliente_pre_seleccionado = None
    if cliente_id:
        try:
            cliente_pre_seleccionado = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente no encontrado.')
            return redirect('instalaciones:instalacion_list')
    
    if request.method == 'POST':
        form = InstalacionForm(request.POST)
        # Si viene de un cliente específico, forzar el cliente en el formulario
        if cliente_pre_seleccionado:
            form.data = form.data.copy()
            form.data['cliente'] = cliente_pre_seleccionado.pk
        
        if form.is_valid():
            instalacion = form.save()
            # Si se seleccionó un plan del catálogo, actualizar el plan_nombre si está vacío
            if instalacion.plan and not instalacion.plan_nombre:
                instalacion.plan_nombre = instalacion.plan.nombre
                instalacion.save()
            messages.success(request, f'Instalación "{instalacion}" creada exitosamente.')
            return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
    else:
        form = InstalacionForm()
        # Pre-llenar el cliente si se proporciona
        if cliente_pre_seleccionado:
            form.fields['cliente'].initial = cliente_pre_seleccionado
            form.fields['cliente'].widget.attrs['disabled'] = True
            form.fields['cliente'].widget.attrs['style'] = 'background-color: #f3f4f6; cursor: not-allowed;'
    
    context = {
        'form': form,
        'title': 'Nueva Instalación',
        'cliente_pre_seleccionado': cliente_pre_seleccionado,
    }
    
    return render(request, 'instalaciones/instalacion_form.html', context)


@login_required
def instalacion_update(request, pk):
    """Actualiza una instalación existente."""
    instalacion = get_object_or_404(Instalacion, pk=pk)
    
    if request.method == 'POST':
        form = InstalacionForm(request.POST, instance=instalacion)
        if form.is_valid():
            instalacion = form.save()
            # Si se seleccionó un plan del catálogo, actualizar el plan_nombre si está vacío
            if instalacion.plan and not instalacion.plan_nombre:
                instalacion.plan_nombre = instalacion.plan.nombre
                instalacion.save()
            messages.success(request, f'Instalación "{instalacion}" actualizada exitosamente.')
            return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
    else:
        form = InstalacionForm(instance=instalacion)
    
    context = {
        'form': form,
        'instalacion': instalacion,
        'title': 'Editar Instalación',
    }
    
    return render(request, 'instalaciones/instalacion_form.html', context)


@login_required
def instalacion_delete(request, pk):
    """Elimina una instalación."""
    instalacion = get_object_or_404(Instalacion, pk=pk)
    
    if request.method == 'POST':
        instalacion_str = str(instalacion)
        instalacion.delete()
        messages.success(request, f'Instalación "{instalacion_str}" eliminada exitosamente.')
        return redirect('instalaciones:instalacion_list')
    
    context = {
        'instalacion': instalacion,
    }
    
    return render(request, 'instalaciones/instalacion_confirm_delete.html', context)


@login_required
def get_plan_data(request, plan_id):
    """Obtiene los datos de un plan en formato JSON."""
    try:
        plan = get_object_or_404(PlanInternet, pk=plan_id)
        return JsonResponse({
            'nombre': plan.nombre,
            'velocidad_descarga': plan.velocidad_descarga,
            'velocidad_subida': plan.velocidad_subida or '',
            'precio_mensual': float(plan.precio_mensual),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
