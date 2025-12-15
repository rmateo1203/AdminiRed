from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Pago, PlanPago
from .forms import PagoForm, PlanPagoForm
from clientes.models import Cliente


@login_required
def pago_list(request):
    """Lista todos los pagos con búsqueda y filtros."""
    pagos = Pago.objects.select_related('cliente', 'instalacion').all()
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        pagos = pagos.filter(
            Q(cliente__nombre__icontains=query) |
            Q(cliente__apellido1__icontains=query) |
            Q(cliente__apellido2__icontains=query) |
            Q(cliente__telefono__icontains=query) |
            Q(concepto__icontains=query) |
            Q(referencia_pago__icontains=query)
        )
    
    # Filtro por estado
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        pagos = pagos.filter(estado=estado_filter)
    
    # Filtro por método de pago
    metodo_filter = request.GET.get('metodo', '')
    if metodo_filter:
        pagos = pagos.filter(metodo_pago=metodo_filter)
    
    # Filtro por período
    periodo_anio = request.GET.get('anio', '')
    periodo_mes = request.GET.get('mes', '')
    if periodo_anio:
        pagos = pagos.filter(periodo_anio=periodo_anio)
    if periodo_mes:
        pagos = pagos.filter(periodo_mes=periodo_mes)
    
    # Ordenamiento
    orden = request.GET.get('orden', '-fecha_vencimiento')
    pagos = pagos.order_by(orden)
    
    # Calcular estadísticas
    total_pagos = pagos.count()
    total_monto = pagos.aggregate(Sum('monto'))['monto__sum'] or 0
    pagos_pendientes = pagos.filter(estado='pendiente').count()
    pagos_vencidos = pagos.filter(estado='vencido').count()
    pagos_pagados = pagos.filter(estado='pagado').count()
    
    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(pagos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado_filter': estado_filter,
        'metodo_filter': metodo_filter,
        'periodo_anio': periodo_anio,
        'periodo_mes': periodo_mes,
        'orden': orden,
        'estados': Pago.ESTADO_CHOICES,
        'metodos': Pago.METODO_PAGO_CHOICES,
        'total_pagos': total_pagos,
        'total_monto': total_monto,
        'pagos_pendientes': pagos_pendientes,
        'pagos_vencidos': pagos_vencidos,
        'pagos_pagados': pagos_pagados,
    }
    
    return render(request, 'pagos/pago_list.html', context)


@login_required
def pago_detail(request, pk):
    """Muestra los detalles de un pago."""
    pago = get_object_or_404(Pago.objects.select_related('cliente', 'instalacion'), pk=pk)
    
    # Obtener notificaciones relacionadas si existen
    notificaciones = pago.notificaciones.all() if hasattr(pago, 'notificaciones') else []
    
    context = {
        'pago': pago,
        'notificaciones': notificaciones,
    }
    
    return render(request, 'pagos/pago_detail.html', context)


@login_required
def pago_create(request, cliente_id=None):
    """Crea un nuevo pago."""
    cliente_pre_seleccionado = None
    if cliente_id:
        try:
            cliente_pre_seleccionado = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente no encontrado.')
            return redirect('pagos:pago_list')
    
    if request.method == 'POST':
        form = PagoForm(request.POST, cliente_id=cliente_id)
        if form.is_valid():
            pago = form.save()
            messages.success(request, f'Pago de ${pago.monto} creado exitosamente.')
            return redirect('pagos:pago_detail', pk=pago.pk)
    else:
        form = PagoForm(cliente_id=cliente_id)
        if cliente_pre_seleccionado:
            form.fields['cliente'].initial = cliente_pre_seleccionado
            form.fields['instalacion'].queryset = cliente_pre_seleccionado.instalaciones.all()
    
    context = {
        'form': form,
        'title': 'Nuevo Pago',
        'cliente_pre_seleccionado': cliente_pre_seleccionado,
    }
    
    return render(request, 'pagos/pago_form.html', context)


@login_required
def pago_update(request, pk):
    """Actualiza un pago existente."""
    pago = get_object_or_404(Pago, pk=pk)
    
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            pago = form.save()
            messages.success(request, f'Pago actualizado exitosamente.')
            return redirect('pagos:pago_detail', pk=pago.pk)
    else:
        form = PagoForm(instance=pago)
        # Cargar instalaciones del cliente si existe
        if pago.cliente:
            form.fields['instalacion'].queryset = pago.cliente.instalaciones.all()
    
    context = {
        'form': form,
        'pago': pago,
        'title': 'Editar Pago',
    }
    
    return render(request, 'pagos/pago_form.html', context)


@login_required
def pago_delete(request, pk):
    """Elimina un pago."""
    pago = get_object_or_404(Pago, pk=pk)
    
    if request.method == 'POST':
        pago_str = f"${pago.monto} - {pago.cliente.nombre_completo}"
        pago.delete()
        messages.success(request, f'Pago "{pago_str}" eliminado exitosamente.')
        return redirect('pagos:pago_list')
    
    context = {
        'pago': pago,
    }
    
    return render(request, 'pagos/pago_confirm_delete.html', context)


@login_required
def pago_marcar_pagado(request, pk):
    """Marca un pago como pagado."""
    pago = get_object_or_404(Pago, pk=pk)
    
    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago', '')
        referencia_pago = request.POST.get('referencia_pago', '')
        
        pago.marcar_como_pagado(
            metodo_pago=metodo_pago if metodo_pago else None,
            referencia=referencia_pago if referencia_pago else None
        )
        messages.success(request, f'Pago marcado como pagado exitosamente.')
        return redirect('pagos:pago_detail', pk=pago.pk)
    
    context = {
        'pago': pago,
        'metodos': Pago.METODO_PAGO_CHOICES,
    }
    
    return render(request, 'pagos/pago_marcar_pagado.html', context)
