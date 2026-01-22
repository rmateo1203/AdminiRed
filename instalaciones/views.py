from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
import logging
from .models import Instalacion, PlanInternet, ConfiguracionNumeroContrato, CambioEstadoInstalacion
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
    
    # Obtener historial de cambios de estado
    cambios_estado = instalacion.cambios_estado.all().select_related('usuario').order_by('-fecha_cambio')[:10]
    
    # Obtener historial completo (Simple History)
    historial = None
    if hasattr(instalacion, 'history'):
        historial = instalacion.history.all()[:20]
    
    context = {
        'instalacion': instalacion,
        'pagos': pagos,
        'cambios_estado': cambios_estado,
        'historial': historial,
        'estados': Instalacion.ESTADO_CHOICES,
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
    if request.method == 'GET':
        try:
            preview = NumeroContratoService.obtener_preview(config)
        except:
            preview = None
    elif form.is_valid():
        try:
            # Crear una instancia temporal con los datos del formulario para el preview
            config_preview = ConfiguracionNumeroContrato(
                prefijo=form.cleaned_data.get('prefijo', config.prefijo),
                separador=form.cleaned_data.get('separador', config.separador),
                sufijo=form.cleaned_data.get('sufijo', config.sufijo),
                incluir_anio=form.cleaned_data.get('incluir_anio', config.incluir_anio),
                formato_anio=form.cleaned_data.get('formato_anio', config.formato_anio),
                incluir_mes=form.cleaned_data.get('incluir_mes', config.incluir_mes),
                incluir_secuencia=form.cleaned_data.get('incluir_secuencia', config.incluir_secuencia),
                longitud_secuencia=form.cleaned_data.get('longitud_secuencia', config.longitud_secuencia),
                resetear_secuencia=form.cleaned_data.get('resetear_secuencia', config.resetear_secuencia),
                activa=True
            )
            preview = NumeroContratoService.obtener_preview(config_preview)
        except:
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
    prefijo = request.GET.get('prefijo', 'CONT')
    separador = request.GET.get('separador', '-')
    sufijo = request.GET.get('sufijo', '')
    incluir_anio = request.GET.get('incluir_anio', 'true').lower() == 'true'
    formato_anio = request.GET.get('formato_anio', 'completo')
    incluir_mes = request.GET.get('incluir_mes', 'true').lower() == 'true'
    incluir_secuencia = request.GET.get('incluir_secuencia', 'true').lower() == 'true'
    longitud_secuencia = int(request.GET.get('longitud_secuencia', 4))
    resetear_secuencia = request.GET.get('resetear_secuencia', 'mensual')
    
    try:
        # Crear una instancia temporal de configuración para el preview
        config_preview = ConfiguracionNumeroContrato(
            prefijo=prefijo,
            separador=separador,
            sufijo=sufijo,
            incluir_anio=incluir_anio,
            formato_anio=formato_anio,
            incluir_mes=incluir_mes,
            incluir_secuencia=incluir_secuencia,
            longitud_secuencia=longitud_secuencia,
            resetear_secuencia=resetear_secuencia,
            activa=True
        )
        preview = NumeroContratoService.obtener_preview(config_preview)
        return JsonResponse({'preview': preview, 'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False}, status=400)


@login_required
def instalacion_cambiar_estado(request, pk):
    """Cambia el estado de una instalación."""
    instalacion = get_object_or_404(Instalacion, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        notas = request.POST.get('notas', '')
        
        if not nuevo_estado:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Estado no proporcionado', 'success': False}, status=400)
            messages.error(request, 'Estado no proporcionado.')
            return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
        
        # Validar que el estado sea válido
        estados_validos = [choice[0] for choice in Instalacion.ESTADO_CHOICES]
        if nuevo_estado not in estados_validos:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Estado inválido', 'success': False}, status=400)
            messages.error(request, 'Estado inválido.')
            return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
        
        # Si el estado es el mismo, no hacer nada
        if instalacion.estado == nuevo_estado:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'La instalación ya tiene ese estado', 'success': False}, status=400)
            messages.warning(request, 'La instalación ya tiene ese estado.')
            return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
        
        # Guardar el estado anterior
        estado_anterior = instalacion.estado
        
        # Cambiar el estado
        instalacion.estado = nuevo_estado
        instalacion.save()
        
        # Registrar el cambio en el historial
        CambioEstadoInstalacion.objects.create(
            instalacion=instalacion,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=request.user,
            notas=notas
        )
        
        estado_anterior_display = instalacion._get_estado_display(estado_anterior)
        estado_nuevo_display = instalacion.get_estado_display()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Estado cambiado de {estado_anterior_display} a {estado_nuevo_display}',
                'nuevo_estado': nuevo_estado,
                'nuevo_estado_display': estado_nuevo_display
            })
        
        messages.success(request, f'Estado cambiado de {estado_anterior_display} a {estado_nuevo_display}.')
        return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
    
    # Si es GET, mostrar formulario para cambiar estado
    context = {
        'instalacion': instalacion,
        'estados': Instalacion.ESTADO_CHOICES,
        'estado_actual': instalacion.estado,
    }
    
    return render(request, 'instalaciones/cambiar_estado.html', context)


@login_required
def instalacion_seguimiento_rapido(request, pk):
    """Vista para seguimiento rápido de instalaciones (cambiar estado y agregar notas sin editar)."""
    instalacion = get_object_or_404(Instalacion, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado', '').strip()
        notas = request.POST.get('notas', '').strip()
        
        if not nuevo_estado:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Debes seleccionar un nuevo estado.'
                }, status=400)
            messages.error(request, 'Debes seleccionar un nuevo estado.')
            return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
        
        # Validar que el estado sea válido
        estados_validos = [estado[0] for estado in Instalacion.ESTADO_CHOICES]
        if nuevo_estado not in estados_validos:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Estado inválido.'
                }, status=400)
            messages.error(request, 'Estado inválido.')
            return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
        
        # Guardar el estado anterior
        estado_anterior = instalacion.estado
        
        # Cambiar el estado
        instalacion.estado = nuevo_estado
        
        # Actualizar fechas según el nuevo estado
        from django.utils import timezone
        if nuevo_estado == 'programada' and not instalacion.fecha_programada:
            # Si se programa, actualizar fecha programada si no existe
            fecha_programada = request.POST.get('fecha_programada')
            if fecha_programada:
                try:
                    from django.utils.dateparse import parse_datetime
                    instalacion.fecha_programada = parse_datetime(fecha_programada)
                except:
                    pass
        elif nuevo_estado == 'activa':
            # Si se activa, establecer fecha_activacion si no existe
            if not instalacion.fecha_activacion:
                instalacion.fecha_activacion = timezone.now()
            # La señal creará automáticamente el PlanPago si no existe
        elif nuevo_estado == 'en_proceso' and not instalacion.fecha_instalacion:
            # Si está en proceso, podría ser el inicio de la instalación
            pass
        
        instalacion.save()
        
        # Registrar el cambio en el historial
        CambioEstadoInstalacion.objects.create(
            instalacion=instalacion,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=request.user,
            notas=notas
        )
        
        estado_anterior_display = dict(Instalacion.ESTADO_CHOICES).get(estado_anterior, estado_anterior)
        estado_nuevo_display = instalacion.get_estado_display()
        
        mensaje = f'Estado actualizado de {estado_anterior_display} a {estado_nuevo_display}.'
        
        # Si se activó la instalación, verificar si se creó PlanPago
        if nuevo_estado == 'activa':
            # Recargar la instalación para obtener el PlanPago si se creó
            instalacion.refresh_from_db()
            try:
                if hasattr(instalacion, 'plan_pago') and instalacion.plan_pago:
                    mensaje += f' Plan de pago creado automáticamente: ${instalacion.plan_pago.monto_mensual}/mes, día {instalacion.plan_pago.dia_vencimiento}.'
            except:
                pass
        
        if notas:
            mensaje += f' Notas: {notas}'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': mensaje,
                'nuevo_estado': nuevo_estado,
                'nuevo_estado_display': estado_nuevo_display
            })
        
        messages.success(request, mensaje)
        return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
    
    # Si es GET, redirigir al detalle
    return redirect('instalaciones:instalacion_detail', pk=instalacion.pk)
