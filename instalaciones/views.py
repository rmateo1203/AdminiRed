from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
import logging
from .models import Instalacion, PlanInternet, ConfiguracionNumeroContrato
from .forms import InstalacionForm, ConfiguracionNumeroContratoForm
from .services import NumeroContratoService
from clientes.models import Cliente

logger = logging.getLogger(__name__)


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
    
    # Calcular estadísticas (antes de paginación)
    total_instalaciones = instalaciones.count()
    activas = instalaciones.filter(estado='activa').count()
    pendientes = instalaciones.filter(estado__in=['pendiente', 'programada', 'en_proceso']).count()
    programadas = instalaciones.filter(estado='programada').count()
    suspendidas = instalaciones.filter(estado='suspendida').count()
    canceladas = instalaciones.filter(estado='cancelada').count()
    
    # Paginación
    paginator = Paginator(instalaciones, 20)  # 20 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado_filter': estado_filter,
        'orden': orden,
        'estados': Instalacion.ESTADO_CHOICES,
        'total_instalaciones': total_instalaciones,
        'activas': activas,
        'pendientes': pendientes,
        'programadas': programadas,
        'suspendidas': suspendidas,
        'canceladas': canceladas,
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
            try:
                instalacion = form.save()
                messages.success(request, f'Instalación "{instalacion}" creada exitosamente.')
                return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
            except Exception as e:
                messages.error(request, f'Error al crear la instalación: {str(e)}')
                logger.error(f'Error al crear instalación: {str(e)}')
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
    instalacion = get_object_or_404(Instalacion.objects.select_related('cliente'), pk=pk)
    
    if request.method == 'POST':
        form = InstalacionForm(request.POST, instance=instalacion)
        if form.is_valid():
            try:
                instalacion = form.save()
                messages.success(request, f'Instalación "{instalacion}" actualizada exitosamente.')
                return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
            except Exception as e:
                messages.error(request, f'Error al actualizar la instalación: {str(e)}')
                logger.error(f'Error al actualizar instalación {instalacion.pk}: {str(e)}')
    else:
        form = InstalacionForm(instance=instalacion)
        # Pre-llenar el cliente en el formulario
        if instalacion.cliente:
            form.fields['cliente'].initial = instalacion.cliente
    
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


# ============================================
# API para búsqueda de clientes
# ============================================

@login_required
def buscar_clientes_api(request):
    """API para buscar clientes por nombre, apellido, teléfono o email."""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'clientes': []})
    
    clientes = Cliente.objects.filter(
        Q(nombre__icontains=query) |
        Q(apellido1__icontains=query) |
        Q(apellido2__icontains=query) |
        Q(telefono__icontains=query) |
        Q(email__icontains=query)
    ).order_by('nombre', 'apellido1')[:15]
    
    data = {
        'clientes': [
            {
                'id': c.id,
                'nombre_completo': c.nombre_completo,
                'telefono': c.telefono,
                'email': c.email or '',
                'estado': c.get_estado_cliente_display(),
                'ciudad': c.ciudad or '',
            }
            for c in clientes
        ]
    }
    
    return JsonResponse(data)


@login_required
def get_cliente_instalaciones_api(request, cliente_id):
    """API para obtener las instalaciones de un cliente."""
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
        instalaciones = cliente.instalaciones.all().order_by('-fecha_solicitud')
        
        data = {
            'cliente': {
                'id': cliente.id,
                'nombre_completo': cliente.nombre_completo,
            },
            'instalaciones': [
                {
                    'id': inst.id,
                    'plan_nombre': inst.plan_nombre or f'Instalación #{inst.id}',
                    'estado': inst.get_estado_display(),
                    'precio_mensual': str(inst.precio_mensual),
                    'direccion': inst.direccion_instalacion or '',
                    'numero_contrato': inst.numero_contrato or '',
                    'fecha_solicitud': inst.fecha_solicitud.strftime('%d/%m/%Y') if inst.fecha_solicitud else '',
                }
                for inst in instalaciones
            ]
        }
        
        return JsonResponse(data)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


@login_required
def configurar_numero_contrato(request):
    """Vista para configurar la generación automática de números de contrato."""
    config = ConfiguracionNumeroContrato.get_activa()
    
    if request.method == 'POST':
        form = ConfiguracionNumeroContratoForm(request.POST, instance=config)
        if form.is_valid():
            config = form.save()
            messages.success(request, 'Configuración de número de contrato actualizada exitosamente.')
            return redirect('instalaciones:configurar_numero_contrato')
    else:
        form = ConfiguracionNumeroContratoForm(instance=config)
    
    # Generar preview del formato
    preview = None
    try:
        # Si el formulario es válido, usar la instancia guardada
        if form.is_valid() and form.instance.pk:
            preview = NumeroContratoService.obtener_preview(config=form.instance)
        elif config:
            # Usar la configuración actual o los valores del formulario si están presentes
            temp_config = ConfiguracionNumeroContrato()
            temp_config.activa = form['activa'].value() if form['activa'].value() is not None else (config.activa if config else True)
            temp_config.prefijo = form['prefijo'].value() or (config.prefijo if config else 'CONT')
            temp_config.incluir_anio = form['incluir_anio'].value() if form['incluir_anio'].value() is not None else (config.incluir_anio if config else True)
            temp_config.formato_anio = form['formato_anio'].value() or (config.formato_anio if config else 'completo')
            temp_config.incluir_mes = form['incluir_mes'].value() if form['incluir_mes'].value() is not None else (config.incluir_mes if config else True)
            temp_config.incluir_secuencia = form['incluir_secuencia'].value() if form['incluir_secuencia'].value() is not None else (config.incluir_secuencia if config else True)
            temp_config.longitud_secuencia = form['longitud_secuencia'].value() or (config.longitud_secuencia if config else 4)
            temp_config.resetear_secuencia = form['resetear_secuencia'].value() or (config.resetear_secuencia if config else 'mensual')
            temp_config.separador = form['separador'].value() or (config.separador if config else '-')
            temp_config.sufijo = form['sufijo'].value() or (config.sufijo if config else '')
            preview = NumeroContratoService.obtener_preview(config=temp_config)
        else:
            preview = NumeroContratoService.obtener_preview()
    except Exception as e:
        logger.error(f"Error generando preview: {e}")
        preview = None
    
    # Ejemplos de formatos
    ejemplos_formatos = [
        {
            'formato': 'INST-{YYYY}{MM}{DD}-{####}',
            'descripcion': 'INST-20241215-0001',
            'ejemplo': 'Con año completo, mes y día'
        },
        {
            'formato': '{PREFIJO}-{YY}{MM}{DD}-{####}',
            'descripcion': 'INST-241215-0001',
            'ejemplo': 'Con año de 2 dígitos'
        },
        {
            'formato': 'CONTRATO-{YYYY}-{####}',
            'descripcion': 'CONTRATO-2024-0001',
            'ejemplo': 'Solo año y número secuencial'
        },
        {
            'formato': '{PREFIJO}{YYYY}{MM}{DD}{####}',
            'descripcion': 'INST202412150001',
            'ejemplo': 'Sin separadores'
        },
    ]
    
    context = {
        'form': form,
        'config': config,
        'preview': preview,
        'ejemplos_formatos': ejemplos_formatos,
    }
    
    return render(request, 'instalaciones/configurar_numero_contrato.html', context)


@login_required
def preview_numero_contrato(request):
    """API para obtener preview del número de contrato."""
    formato = request.GET.get('formato', '')
    prefijo = request.GET.get('prefijo', 'INST')
    numero_inicial = int(request.GET.get('numero_inicial', 1))
    digitos_secuencia = int(request.GET.get('digitos_secuencia', 4))
    reiniciar_diario = request.GET.get('reiniciar_diario', 'true').lower() == 'true'
    
    try:
        preview = NumeroContratoService.obtener_preview(
            formato=formato,
            prefijo=prefijo,
            numero_inicial=numero_inicial,
            digitos_secuencia=digitos_secuencia,
            reiniciar_diario=reiniciar_diario
        )
        return JsonResponse({'preview': preview, 'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False}, status=400)
