from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from datetime import timedelta, date, datetime
from calendar import monthrange
import json
from .models import Pago, PlanPago
from .forms import PagoForm, PlanPagoForm
from clientes.models import Cliente
from instalaciones.models import Instalacion


@login_required
def pago_list(request):
    """Lista todos los pagos con búsqueda y filtros."""
    # Actualizar automáticamente pagos vencidos
    Pago.actualizar_pagos_vencidos()
    
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
        'cliente_pre_seleccionado': pago.cliente,  # Para mostrar en el buscador
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


# ============================================
# API para búsqueda de clientes
# ============================================

@login_required
def buscar_clientes(request):
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
def obtener_instalaciones_cliente(request, cliente_id):
    """API para obtener las instalaciones de un cliente con información de PlanPago."""
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
        instalaciones = cliente.instalaciones.all()
        
        instalaciones_data = []
        for inst in instalaciones:
            # Obtener PlanPago si existe
            plan_pago = None
            try:
                plan_pago = inst.plan_pago
            except:
                pass
            
            instalacion_data = {
                'id': inst.id,
                'plan_nombre': inst.plan_nombre or f'Instalación #{inst.id}',
                'estado': inst.get_estado_display(),
                'precio_mensual': float(inst.precio_mensual) if inst.precio_mensual else None,
                'direccion': inst.direccion_instalacion or '',
            }
            
            # Agregar información del PlanPago si existe
            if plan_pago and plan_pago.activo:
                instalacion_data['plan_pago'] = {
                    'monto_mensual': float(plan_pago.monto_mensual),
                    'dia_vencimiento': plan_pago.dia_vencimiento,
                    'activo': plan_pago.activo,
                }
            
            instalaciones_data.append(instalacion_data)
        
        data = {
            'cliente': {
                'id': cliente.id,
                'nombre_completo': cliente.nombre_completo,
            },
            'instalaciones': instalaciones_data
        }
        
        return JsonResponse(data)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


# ============================================
# Exportación de Pagos
# ============================================

@login_required
def pago_exportar_excel(request):
    """Exporta los pagos filtrados a Excel."""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter
    except ImportError:
        messages.error(request, 'La librería openpyxl no está instalada. Ejecuta: pip install openpyxl')
        return redirect('pagos:pago_list')
    
    # Obtener los mismos filtros que en pago_list
    pagos = Pago.objects.select_related('cliente', 'instalacion').all()
    
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
    
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        pagos = pagos.filter(estado=estado_filter)
    
    metodo_filter = request.GET.get('metodo', '')
    if metodo_filter:
        pagos = pagos.filter(metodo_pago=metodo_filter)
    
    periodo_anio = request.GET.get('anio', '')
    periodo_mes = request.GET.get('mes', '')
    if periodo_anio:
        pagos = pagos.filter(periodo_anio=periodo_anio)
    if periodo_mes:
        pagos = pagos.filter(periodo_mes=periodo_mes)
    
    orden = request.GET.get('orden', '-fecha_vencimiento')
    pagos = pagos.order_by(orden)
    
    # Crear workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Pagos"
    
    # Estilos
    header_fill = PatternFill(start_color="667eea", end_color="667eea", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    # Encabezados
    headers = ['Cliente', 'Instalación', 'Concepto', 'Monto', 'Período', 
               'Fecha Vencimiento', 'Fecha Pago', 'Estado', 'Método Pago', 
               'Referencia', 'Notas']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # Datos
    for row, pago in enumerate(pagos, 2):
        ws.cell(row=row, column=1, value=pago.cliente.nombre_completo)
        ws.cell(row=row, column=2, value=pago.instalacion.plan_nombre if pago.instalacion else '')
        ws.cell(row=row, column=3, value=pago.concepto)
        ws.cell(row=row, column=4, value=float(pago.monto))
        ws.cell(row=row, column=5, value=f"{pago.get_periodo_mes_display()} {pago.periodo_anio}")
        ws.cell(row=row, column=6, value=pago.fecha_vencimiento.strftime('%d/%m/%Y'))
        ws.cell(row=row, column=7, value=pago.fecha_pago.strftime('%d/%m/%Y %H:%M') if pago.fecha_pago else '')
        ws.cell(row=row, column=8, value=pago.get_estado_display())
        ws.cell(row=row, column=9, value=pago.get_metodo_pago_display() if pago.metodo_pago else '')
        ws.cell(row=row, column=10, value=pago.referencia_pago or '')
        ws.cell(row=row, column=11, value=pago.notas or '')
    
    # Ajustar ancho de columnas
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 20
    
    # Crear respuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f'pagos_export_{date.today().strftime("%Y%m%d")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb.save(response)
    return response


@login_required
def pago_exportar_pdf(request):
    """Exporta los pagos filtrados a PDF."""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    except ImportError:
        messages.error(request, 'La librería reportlab no está instalada. Ejecuta: pip install reportlab')
        return redirect('pagos:pago_list')
    
    # Obtener los mismos filtros que en pago_list
    pagos = Pago.objects.select_related('cliente', 'instalacion').all()
    
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
    
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        pagos = pagos.filter(estado=estado_filter)
    
    metodo_filter = request.GET.get('metodo', '')
    if metodo_filter:
        pagos = pagos.filter(metodo_pago=metodo_filter)
    
    periodo_anio = request.GET.get('anio', '')
    periodo_mes = request.GET.get('mes', '')
    if periodo_anio:
        pagos = pagos.filter(periodo_anio=periodo_anio)
    if periodo_mes:
        pagos = pagos.filter(periodo_mes=periodo_mes)
    
    orden = request.GET.get('orden', '-fecha_vencimiento')
    pagos = pagos.order_by(orden)
    
    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f'pagos_export_{date.today().strftime("%Y%m%d")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Crear documento
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
    )
    
    # Título
    elements.append(Paragraph('Reporte de Pagos', title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Información del reporte
    info_text = f"<b>Fecha de generación:</b> {date.today().strftime('%d/%m/%Y')}<br/>"
    info_text += f"<b>Total de pagos:</b> {pagos.count()}<br/>"
    if query:
        info_text += f"<b>Búsqueda:</b> {query}<br/>"
    if estado_filter:
        info_text += f"<b>Estado:</b> {dict(Pago.ESTADO_CHOICES).get(estado_filter, estado_filter)}<br/>"
    
    elements.append(Paragraph(info_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Preparar datos de la tabla
    data = [['Cliente', 'Concepto', 'Monto', 'Período', 'Vencimiento', 'Estado']]
    
    for pago in pagos[:100]:  # Limitar a 100 para no sobrecargar el PDF
        data.append([
            pago.cliente.nombre_completo[:30],  # Truncar nombres largos
            pago.concepto[:25],
            f"${pago.monto:.2f}",
            f"{pago.get_periodo_mes_display()} {pago.periodo_anio}",
            pago.fecha_vencimiento.strftime('%d/%m/%Y'),
            pago.get_estado_display()
        ])
    
    # Crear tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    
    # Construir PDF
    doc.build(elements)
    return response


# ============================================
# Vista de Calendario
# ============================================

@login_required
def pago_calendario(request):
    """Vista de calendario mensual de pagos."""
    # Obtener mes y año de la URL o usar el actual
    hoy = date.today()
    try:
        anio = int(request.GET.get('anio', hoy.year))
        mes = int(request.GET.get('mes', hoy.month))
    except (ValueError, TypeError):
        anio = hoy.year
        mes = hoy.month
    
    # Validar mes y año
    if mes < 1 or mes > 12:
        mes = hoy.month
    if anio < 2000 or anio > 2100:
        anio = hoy.year
    
    # Obtener pagos del mes
    pagos = Pago.objects.filter(
        fecha_vencimiento__year=anio,
        fecha_vencimiento__month=mes
    ).select_related('cliente', 'instalacion').order_by('fecha_vencimiento')
    
    # Organizar pagos por día
    pagos_por_dia = {}
    for pago in pagos:
        dia = pago.fecha_vencimiento.day
        if dia not in pagos_por_dia:
            pagos_por_dia[dia] = []
        pagos_por_dia[dia].append(pago)
    
    # Calcular días del mes y primer día de la semana
    dias_en_mes = monthrange(anio, mes)[1]
    primer_dia = date(anio, mes, 1)
    primer_dia_semana = primer_dia.weekday()  # 0 = Lunes, 6 = Domingo
    
    # Meses en español
    meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    # Calcular mes anterior y siguiente
    if mes == 1:
        mes_anterior = 12
        anio_anterior = anio - 1
    else:
        mes_anterior = mes - 1
        anio_anterior = anio
    
    if mes == 12:
        mes_siguiente = 1
        anio_siguiente = anio + 1
    else:
        mes_siguiente = mes + 1
        anio_siguiente = anio
    
    # Estadísticas del mes
    total_pagos = pagos.count()
    total_monto = pagos.aggregate(Sum('monto'))['monto__sum'] or 0
    pagos_pendientes = pagos.filter(estado='pendiente').count()
    pagos_vencidos = pagos.filter(estado='vencido').count()
    pagos_pagados = pagos.filter(estado='pagado').count()
    
    context = {
        'anio': anio,
        'mes': mes,
        'mes_nombre': meses[mes],
        'dias_en_mes': dias_en_mes,
        'primer_dia_semana': primer_dia_semana,
        'pagos_por_dia': pagos_por_dia,
        'mes_anterior': mes_anterior,
        'anio_anterior': anio_anterior,
        'mes_siguiente': mes_siguiente,
        'anio_siguiente': anio_siguiente,
        'total_pagos': total_pagos,
        'total_monto': total_monto,
        'pagos_pendientes': pagos_pendientes,
        'pagos_vencidos': pagos_vencidos,
        'pagos_pagados': pagos_pagados,
        'hoy': hoy,
    }
    
    return render(request, 'pagos/pago_calendario.html', context)


# ============================================
# Reportes Financieros
# ============================================

@login_required
def pago_reportes(request):
    """Vista de reportes financieros."""
    # Obtener año de la URL o usar el actual
    hoy = date.today()
    try:
        anio = int(request.GET.get('anio', hoy.year))
    except (ValueError, TypeError):
        anio = hoy.year
    
    # Generar lista de años disponibles (2020-2030)
    años_disponibles = list(range(2020, 2031))
    
    # Validar año
    if anio < 2000 or anio > 2100:
        anio = hoy.year
    
    # Obtener todos los pagos del año
    pagos = Pago.objects.filter(periodo_anio=anio).select_related('cliente', 'instalacion')
    
    # Estadísticas generales
    total_pagos = pagos.count()
    total_monto = pagos.aggregate(Sum('monto'))['monto__sum'] or 0
    monto_pagado = pagos.filter(estado='pagado').aggregate(Sum('monto'))['monto__sum'] or 0
    monto_pendiente = pagos.filter(estado__in=['pendiente', 'vencido']).aggregate(Sum('monto'))['monto__sum'] or 0
    
    # Ingresos por mes
    ingresos_por_mes = []
    for mes in range(1, 13):
        pagos_mes = pagos.filter(periodo_mes=mes, estado='pagado')
        monto_mes = pagos_mes.aggregate(Sum('monto'))['monto__sum'] or 0
        cantidad_mes = pagos_mes.count()
        ingresos_por_mes.append({
            'mes': mes,
            'mes_nombre': ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][mes],
            'monto': monto_mes,
            'cantidad': cantidad_mes
        })
    
    # Top 10 clientes por monto pagado
    top_clientes = pagos.filter(estado='pagado').values(
        'cliente__nombre', 'cliente__apellido1', 'cliente__id'
    ).annotate(
        total_pagado=Sum('monto'),
        cantidad_pagos=Count('id')
    ).order_by('-total_pagado')[:10]
    
    # Clientes morosos (con pagos vencidos)
    clientes_morosos = pagos.filter(estado='vencido').values(
        'cliente__nombre', 'cliente__apellido1', 'cliente__id'
    ).annotate(
        total_vencido=Sum('monto'),
        cantidad_vencidos=Count('id')
    ).order_by('-total_vencido')[:10]
    
    # Métodos de pago más usados
    metodos_pago = pagos.filter(estado='pagado', metodo_pago__isnull=False).values(
        'metodo_pago'
    ).annotate(
        total=Sum('monto'),
        cantidad=Count('id')
    ).order_by('-total')
    
    # Promedio de pago
    promedio_pago = pagos.filter(estado='pagado').aggregate(Avg('monto'))['monto__avg'] or 0
    
    context = {
        'anio': anio,
        'años_disponibles': años_disponibles,
        'total_pagos': total_pagos,
        'total_monto': total_monto,
        'monto_pagado': monto_pagado,
        'monto_pendiente': monto_pendiente,
        'ingresos_por_mes': ingresos_por_mes,
        'top_clientes': top_clientes,
        'clientes_morosos': clientes_morosos,
        'metodos_pago': metodos_pago,
        'promedio_pago': promedio_pago,
    }
    
    return render(request, 'pagos/pago_reportes.html', context)
