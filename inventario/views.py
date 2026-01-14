from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, F
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Material, MovimientoInventario, CategoriaMaterial
from .forms import MaterialForm, MovimientoInventarioForm, CategoriaMaterialForm


@login_required
def material_list(request):
    """Lista todos los materiales con búsqueda y filtros."""
    materiales = Material.objects.select_related('categoria').all()
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        materiales = materiales.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    # Filtro por estado
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        materiales = materiales.filter(estado=estado_filter)
    
    # Filtro por categoría
    categoria_filter = request.GET.get('categoria', '')
    if categoria_filter:
        materiales = materiales.filter(categoria_id=categoria_filter)
    
    # Filtro por unidad de medida
    unidad_filter = request.GET.get('unidad', '')
    if unidad_filter:
        materiales = materiales.filter(unidad_medida=unidad_filter)
    
    # Filtro por stock bajo
    stock_bajo = request.GET.get('stock_bajo', '')
    if stock_bajo == '1':
        materiales = materiales.filter(stock_actual__lte=F('stock_minimo'))
    
    # Ordenamiento
    orden = request.GET.get('orden', 'nombre')
    materiales = materiales.order_by(orden)
    
    # Calcular estadísticas
    total_materiales = materiales.count()
    materiales_bajo_stock = materiales.filter(stock_actual__lte=F('stock_minimo')).count()
    materiales_agotados = materiales.filter(estado='agotado').count()
    materiales_disponibles = materiales.filter(estado='disponible').count()
    
    # Valor total del inventario
    valor_total = materiales.aggregate(
        total=Sum(F('stock_actual') * F('precio_compra'))
    )['total'] or 0
    
    # Paginación
    paginator = Paginator(materiales, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener categorías para el filtro
    categorias = CategoriaMaterial.objects.all().order_by('nombre')
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado_filter': estado_filter,
        'categoria_filter': categoria_filter,
        'unidad_filter': unidad_filter,
        'stock_bajo': stock_bajo,
        'orden': orden,
        'estados': Material.ESTADO_CHOICES,
        'unidades': Material.UNIDAD_MEDIDA_CHOICES,
        'categorias': categorias,
        'total_materiales': total_materiales,
        'materiales_bajo_stock': materiales_bajo_stock,
        'materiales_agotados': materiales_agotados,
        'materiales_disponibles': materiales_disponibles,
        'valor_total': valor_total,
    }
    
    return render(request, 'inventario/material_list.html', context)


@login_required
def material_detail(request, pk):
    """Muestra los detalles de un material."""
    material = get_object_or_404(Material.objects.select_related('categoria'), pk=pk)
    
    # Obtener últimos movimientos
    movimientos = material.movimientos.all()[:10]
    
    context = {
        'material': material,
        'movimientos': movimientos,
    }
    
    return render(request, 'inventario/material_detail.html', context)


@login_required
def material_create(request):
    """Crea un nuevo material."""
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save()
            # Actualizar estado según stock
            material.actualizar_estado()
            material.save()
            messages.success(request, f'Material "{material.nombre}" creado exitosamente.')
            return redirect('inventario:material_detail', pk=material.pk)
    else:
        form = MaterialForm()
    
    context = {
        'form': form,
        'title': 'Nuevo Material',
    }
    
    return render(request, 'inventario/material_form.html', context)


@login_required
def material_update(request, pk):
    """Actualiza un material existente."""
    material = get_object_or_404(Material, pk=pk)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            material = form.save()
            # Actualizar estado según stock
            material.actualizar_estado()
            material.save()
            messages.success(request, f'Material "{material.nombre}" actualizado exitosamente.')
            return redirect('inventario:material_detail', pk=material.pk)
    else:
        form = MaterialForm(instance=material)
    
    context = {
        'form': form,
        'material': material,
        'title': 'Editar Material',
    }
    
    return render(request, 'inventario/material_form.html', context)


@login_required
def material_delete(request, pk):
    """Elimina un material."""
    material = get_object_or_404(Material, pk=pk)
    
    if request.method == 'POST':
        material_str = material.nombre
        material.delete()
        messages.success(request, f'Material "{material_str}" eliminado exitosamente.')
        return redirect('inventario:material_list')
    
    context = {
        'material': material,
    }
    
    return render(request, 'inventario/material_confirm_delete.html', context)


@login_required
def movimiento_list(request):
    """Lista todos los movimientos de inventario."""
    movimientos = MovimientoInventario.objects.select_related('material', 'material__categoria').all()
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        movimientos = movimientos.filter(
            Q(material__nombre__icontains=query) |
            Q(material__codigo__icontains=query) |
            Q(motivo__icontains=query) |
            Q(notas__icontains=query)
        )
    
    # Filtro por tipo
    tipo_filter = request.GET.get('tipo', '')
    if tipo_filter:
        movimientos = movimientos.filter(tipo=tipo_filter)
    
    # Filtro por material
    material_filter = request.GET.get('material', '')
    if material_filter:
        movimientos = movimientos.filter(material_id=material_filter)
    
    # Ordenamiento
    orden = request.GET.get('orden', '-fecha')
    movimientos = movimientos.order_by(orden)
    
    # Paginación
    paginator = Paginator(movimientos, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener materiales para el filtro
    materiales = Material.objects.all().order_by('nombre')
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'tipo_filter': tipo_filter,
        'material_filter': material_filter,
        'orden': orden,
        'tipos': MovimientoInventario.TIPO_CHOICES,
        'materiales': materiales,
    }
    
    return render(request, 'inventario/movimiento_list.html', context)


@login_required
def movimiento_create(request):
    """Crea un nuevo movimiento de inventario."""
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            try:
                movimiento = form.save()
                messages.success(request, f'Movimiento registrado exitosamente.')
                return redirect('inventario:movimiento_detail', pk=movimiento.pk)
            except Exception as e:
                messages.error(request, f'Error al registrar movimiento: {str(e)}')
    else:
        form = MovimientoInventarioForm()
    
    context = {
        'form': form,
        'title': 'Nuevo Movimiento de Inventario',
    }
    
    return render(request, 'inventario/movimiento_form.html', context)


@login_required
def movimiento_detail(request, pk):
    """Muestra los detalles de un movimiento."""
    movimiento = get_object_or_404(
        MovimientoInventario.objects.select_related('material', 'material__categoria'),
        pk=pk
    )
    
    context = {
        'movimiento': movimiento,
    }
    
    return render(request, 'inventario/movimiento_detail.html', context)


@login_required
def movimiento_delete(request, pk):
    """Elimina un movimiento de inventario."""
    movimiento = get_object_or_404(MovimientoInventario, pk=pk)
    
    if request.method == 'POST':
        # Revertir el efecto del movimiento en el stock
        material = movimiento.material
        if movimiento.tipo == 'entrada':
            # Si fue una entrada, reducimos el stock
            material.stock_actual = max(0, material.stock_actual - movimiento.cantidad)
        elif movimiento.tipo == 'salida':
            # Si fue una salida, aumentamos el stock
            material.stock_actual += movimiento.cantidad
        elif movimiento.tipo == 'devolucion':
            # Si fue una devolución (entrada), reducimos el stock
            material.stock_actual = max(0, material.stock_actual - movimiento.cantidad)
        
        material.actualizar_estado()
        material.save()
        
        movimiento_str = f"{movimiento.get_tipo_display()} de {movimiento.cantidad} {material.nombre}"
        movimiento.delete()
        messages.success(request, f'Movimiento "{movimiento_str}" eliminado y stock revertido.')
        return redirect('inventario:movimiento_list')
    
    context = {
        'movimiento': movimiento,
    }
    
    return render(request, 'inventario/movimiento_confirm_delete.html', context)


# ============================================
# CRUD de Categorías de Material
# ============================================

@login_required
def categoria_list(request):
    """Lista todas las categorías de materiales."""
    categorias = CategoriaMaterial.objects.annotate(
        num_materiales=Count('materiales')
    ).order_by('nombre')
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        categorias = categorias.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(categorias, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categorias': page_obj,
        'page_obj': page_obj,
        'query': query,
    }
    
    return render(request, 'inventario/categoria_list.html', context)


@login_required
def categoria_create(request):
    """Crea una nueva categoría de material."""
    if request.method == 'POST':
        form = CategoriaMaterialForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente.')
            return redirect('inventario:categoria_list')
    else:
        form = CategoriaMaterialForm()
    
    context = {
        'form': form,
        'title': 'Nueva Categoría',
    }
    
    return render(request, 'inventario/categoria_form.html', context)


@login_required
def categoria_update(request, pk):
    """Actualiza una categoría existente."""
    categoria = get_object_or_404(CategoriaMaterial, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaMaterialForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada exitosamente.')
            return redirect('inventario:categoria_list')
    else:
        form = CategoriaMaterialForm(instance=categoria)
    
    context = {
        'form': form,
        'categoria': categoria,
        'title': 'Editar Categoría',
    }
    
    return render(request, 'inventario/categoria_form.html', context)


@login_required
def categoria_delete(request, pk):
    """Elimina una categoría de material."""
    categoria = get_object_or_404(CategoriaMaterial, pk=pk)
    
    # Verificar si tiene materiales asociados
    num_materiales = categoria.materiales.count()
    
    if request.method == 'POST':
        if num_materiales > 0:
            messages.error(request, f'No se puede eliminar la categoría "{categoria.nombre}" porque tiene {num_materiales} material(es) asociado(s).')
            return redirect('inventario:categoria_list')
        
        categoria_str = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{categoria_str}" eliminada exitosamente.')
        return redirect('inventario:categoria_list')
    
    context = {
        'categoria': categoria,
        'num_materiales': num_materiales,
    }
    
    return render(request, 'inventario/categoria_confirm_delete.html', context)


# ============================================
# API para búsqueda
# ============================================

@login_required
def api_buscar_categorias(request):
    """API para buscar categorías por nombre."""
    query = request.GET.get('q', '').strip()
    
    categorias = CategoriaMaterial.objects.annotate(
        num_materiales=Count('materiales')
    ).order_by('nombre')
    
    if query:
        categorias = categorias.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    # Limitar resultados
    categorias = categorias[:20]
    
    data = {
        'categorias': [
            {
                'id': c.id,
                'nombre': c.nombre,
                'descripcion': c.descripcion or '',
                'num_materiales': c.num_materiales,
            }
            for c in categorias
        ]
    }
    
    return JsonResponse(data)
