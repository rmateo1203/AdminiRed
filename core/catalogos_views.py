from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Importar modelos de catálogos
from instalaciones.models import TipoInstalacion, PlanInternet
from inventario.models import CategoriaMaterial
from notificaciones.models import TipoNotificacion


@login_required
def catalogos_dashboard(request):
    """Dashboard principal de catálogos del sistema."""
    
    # Contar registros de cada catálogo
    tipos_instalacion_count = TipoInstalacion.objects.count()
    planes_internet_count = PlanInternet.objects.count()
    categorias_material_count = CategoriaMaterial.objects.count()
    tipos_notificacion_count = TipoNotificacion.objects.count()
    
    catalogos = [
        {
            'nombre': 'Tipos de Instalación',
            'modelo': 'tipo_instalacion',
            'descripcion': 'Gestiona los tipos de instalación disponibles (Fibra Óptica, Cable, etc.)',
            'count': tipos_instalacion_count,
            'icon': 'fas fa-wifi',
            'color': '#667eea',
            'url': 'core:catalogo_tipo_instalacion_list',
        },
        {
            'nombre': 'Planes de Internet',
            'modelo': 'plan_internet',
            'descripcion': 'Gestiona los planes de internet disponibles con velocidades y precios',
            'count': planes_internet_count,
            'icon': 'fas fa-tachometer-alt',
            'color': '#8b5cf6',
            'url': 'core:catalogo_plan_internet_list',
        },
        {
            'nombre': 'Categorías de Material',
            'modelo': 'categoria_material',
            'descripcion': 'Gestiona las categorías de materiales del inventario',
            'count': categorias_material_count,
            'icon': 'fas fa-boxes',
            'color': '#10b981',
            'url': 'core:catalogo_categoria_material_list',
        },
        {
            'nombre': 'Tipos de Notificación',
            'modelo': 'tipo_notificacion',
            'descripcion': 'Gestiona los tipos de notificaciones del sistema',
            'count': tipos_notificacion_count,
            'icon': 'fas fa-bell',
            'color': '#f59e0b',
            'url': 'core:catalogo_tipo_notificacion_list',
        },
    ]
    
    context = {
        'catalogos': catalogos,
        'total_catalogos': len(catalogos),
    }
    
    return render(request, 'core/catalogos_dashboard.html', context)


# ==================== TIPOS DE INSTALACIÓN ====================

@login_required
def catalogo_tipo_instalacion_list(request):
    """Lista todos los tipos de instalación."""
    from instalaciones.models import Instalacion
    from django.core.paginator import Paginator
    
    tipos = TipoInstalacion.objects.all().order_by('nombre')
    
    query = request.GET.get('q', '')
    if query:
        tipos = tipos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(tipos, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Agregar estadísticas de uso para cada tipo
    tipos_con_estadisticas = []
    for tipo in page_obj:
        count_instalaciones = Instalacion.objects.filter(tipo_instalacion=tipo).count()
        tipos_con_estadisticas.append({
            'tipo': tipo,
            'count_instalaciones': count_instalaciones
        })
    
    context = {
        'tipos': page_obj,
        'tipos_con_estadisticas': tipos_con_estadisticas,
        'page_obj': page_obj,
        'query': query,
        'catalogo_nombre': 'Tipos de Instalación',
        'modelo': 'tipo_instalacion',
        'total_tipos': tipos.count(),
    }
    
    return render(request, 'core/catalogo_list.html', context)


@login_required
def catalogo_tipo_instalacion_create(request):
    """Crea un nuevo tipo de instalación."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        if nombre:
            try:
                tipo = TipoInstalacion.objects.create(
                    nombre=nombre,
                    descripcion=descripcion
                )
                messages.success(request, f'Tipo de instalación "{tipo.nombre}" creado exitosamente.')
                return redirect('core:catalogo_tipo_instalacion_list')
            except Exception as e:
                messages.error(request, f'Error al crear: {str(e)}')
        else:
            messages.error(request, 'El nombre es requerido.')
    
    return redirect('core:catalogo_tipo_instalacion_list')


@login_required
def catalogo_tipo_instalacion_update(request, pk):
    """Actualiza un tipo de instalación."""
    tipo = get_object_or_404(TipoInstalacion, pk=pk)
    
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id', '')
        if registro_id and int(registro_id) != pk:
            pk = int(registro_id)
            tipo = get_object_or_404(TipoInstalacion, pk=pk)
        
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        if nombre:
            try:
                tipo.nombre = nombre
                tipo.descripcion = descripcion
                tipo.save()
                messages.success(request, f'Tipo de instalación "{tipo.nombre}" actualizado exitosamente.')
                return redirect('core:catalogo_tipo_instalacion_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')
        else:
            messages.error(request, 'El nombre es requerido.')
    
    return redirect('core:catalogo_tipo_instalacion_list')


@login_required
def catalogo_tipo_instalacion_delete(request, pk):
    """Elimina un tipo de instalación."""
    from instalaciones.models import Instalacion
    
    tipo = get_object_or_404(TipoInstalacion, pk=pk)
    
    if request.method == 'POST':
        # Verificar si hay instalaciones asociadas
        count_instalaciones = Instalacion.objects.filter(tipo_instalacion=tipo).count()
        if count_instalaciones > 0:
            messages.error(request, f'No se puede eliminar el tipo de instalación "{tipo.nombre}" porque tiene {count_instalaciones} instalación(es) asociada(s).')
            return redirect('core:catalogo_tipo_instalacion_list')
        
        nombre = str(tipo)
        tipo.delete()
        messages.success(request, f'Tipo de instalación "{nombre}" eliminado exitosamente.')
        return redirect('core:catalogo_tipo_instalacion_list')
    
    return redirect('core:catalogo_tipo_instalacion_list')


# ==================== CATEGORÍAS DE MATERIAL ====================

@login_required
def catalogo_categoria_material_list(request):
    """Lista todas las categorías de material."""
    from django.core.paginator import Paginator
    
    categorias = CategoriaMaterial.objects.all().order_by('nombre')
    
    query = request.GET.get('q', '')
    if query:
        categorias = categorias.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(categorias, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tipos': page_obj,
        'page_obj': page_obj,
        'query': query,
        'catalogo_nombre': 'Categorías de Material',
        'modelo': 'categoria_material',
    }
    
    return render(request, 'core/catalogo_list.html', context)


@login_required
def catalogo_categoria_material_create(request):
    """Crea una nueva categoría de material."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        if nombre:
            try:
                categoria = CategoriaMaterial.objects.create(
                    nombre=nombre,
                    descripcion=descripcion
                )
                messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente.')
                return redirect('core:catalogo_categoria_material_list')
            except Exception as e:
                messages.error(request, f'Error al crear: {str(e)}')
        else:
            messages.error(request, 'El nombre es requerido.')
    
    return redirect('core:catalogo_categoria_material_list')


@login_required
def catalogo_categoria_material_update(request, pk):
    """Actualiza una categoría de material."""
    categoria = get_object_or_404(CategoriaMaterial, pk=pk)
    
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id', '')
        if registro_id and int(registro_id) != pk:
            pk = int(registro_id)
            categoria = get_object_or_404(CategoriaMaterial, pk=pk)
        
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        if nombre:
            try:
                categoria.nombre = nombre
                categoria.descripcion = descripcion
                categoria.save()
                messages.success(request, f'Categoría "{categoria.nombre}" actualizada exitosamente.')
                return redirect('core:catalogo_categoria_material_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')
        else:
            messages.error(request, 'El nombre es requerido.')
    
    return redirect('core:catalogo_categoria_material_list')


@login_required
def catalogo_categoria_material_delete(request, pk):
    """Elimina una categoría de material."""
    categoria = get_object_or_404(CategoriaMaterial, pk=pk)
    
    if request.method == 'POST':
        nombre = str(categoria)
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada exitosamente.')
        return redirect('core:catalogo_categoria_material_list')
    
    return redirect('core:catalogo_categoria_material_list')


# ==================== TIPOS DE NOTIFICACIÓN ====================

@login_required
def catalogo_tipo_notificacion_list(request):
    """Lista todos los tipos de notificación."""
    from django.core.paginator import Paginator
    
    tipos = TipoNotificacion.objects.all().order_by('nombre')
    
    query = request.GET.get('q', '')
    if query:
        tipos = tipos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(tipos, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tipos': page_obj,
        'page_obj': page_obj,
        'query': query,
        'catalogo_nombre': 'Tipos de Notificación',
        'modelo': 'tipo_notificacion',
    }
    
    return render(request, 'core/catalogo_list.html', context)


@login_required
def catalogo_tipo_notificacion_create(request):
    """Crea un nuevo tipo de notificación."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        codigo = request.POST.get('codigo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        plantilla = request.POST.get('plantilla', '').strip()
        
        if nombre and codigo:
            try:
                tipo = TipoNotificacion.objects.create(
                    nombre=nombre,
                    codigo=codigo,
                    descripcion=descripcion,
                    plantilla=plantilla
                )
                messages.success(request, f'Tipo de notificación "{tipo.nombre}" creado exitosamente.')
                return redirect('core:catalogo_tipo_notificacion_list')
            except Exception as e:
                messages.error(request, f'Error al crear: {str(e)}')
        else:
            messages.error(request, 'El nombre y código son requeridos.')
    
    return redirect('core:catalogo_tipo_notificacion_list')


@login_required
def catalogo_tipo_notificacion_update(request, pk):
    """Actualiza un tipo de notificación."""
    tipo = get_object_or_404(TipoNotificacion, pk=pk)
    
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id', '')
        if registro_id and int(registro_id) != pk:
            pk = int(registro_id)
            tipo = get_object_or_404(TipoNotificacion, pk=pk)
        
        nombre = request.POST.get('nombre', '').strip()
        codigo = request.POST.get('codigo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        plantilla = request.POST.get('plantilla', '').strip()
        
        if nombre and codigo:
            try:
                tipo.nombre = nombre
                tipo.codigo = codigo
                tipo.descripcion = descripcion
                tipo.plantilla = plantilla
                tipo.save()
                messages.success(request, f'Tipo de notificación "{tipo.nombre}" actualizado exitosamente.')
                return redirect('core:catalogo_tipo_notificacion_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')
        else:
            messages.error(request, 'El nombre y código son requeridos.')
    
    return redirect('core:catalogo_tipo_notificacion_list')


@login_required
def catalogo_tipo_notificacion_delete(request, pk):
    """Elimina un tipo de notificación."""
    tipo = get_object_or_404(TipoNotificacion, pk=pk)
    
    if request.method == 'POST':
        nombre = str(tipo)
        tipo.delete()
        messages.success(request, f'Tipo de notificación "{nombre}" eliminado exitosamente.')
        return redirect('core:catalogo_tipo_notificacion_list')
    
    return redirect('core:catalogo_tipo_notificacion_list')


# ==================== PLANES DE INTERNET ====================

@login_required
def catalogo_plan_internet_list(request):
    """Lista todos los planes de internet."""
    from django.core.paginator import Paginator
    
    planes = PlanInternet.objects.all().order_by('precio_mensual', 'velocidad_descarga')
    
    query = request.GET.get('q', '')
    if query:
        planes = planes.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(planes, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tipos': page_obj,
        'page_obj': page_obj,
        'query': query,
        'catalogo_nombre': 'Planes de Internet',
        'modelo': 'plan_internet',
    }
    
    return render(request, 'core/catalogo_plan_list.html', context)


@login_required
def catalogo_plan_internet_create(request):
    """Crea un nuevo plan de internet."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        velocidad_descarga = request.POST.get('velocidad_descarga', '').strip()
        velocidad_subida = request.POST.get('velocidad_subida', '').strip()
        precio_mensual = request.POST.get('precio_mensual', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        activo = request.POST.get('activo', '') == 'on'
        
        if nombre and velocidad_descarga and precio_mensual:
            try:
                plan = PlanInternet.objects.create(
                    nombre=nombre,
                    velocidad_descarga=int(velocidad_descarga),
                    velocidad_subida=int(velocidad_subida) if velocidad_subida else None,
                    precio_mensual=float(precio_mensual),
                    descripcion=descripcion,
                    activo=activo
                )
                messages.success(request, f'Plan de internet "{plan.nombre}" creado exitosamente.')
                return redirect('core:catalogo_plan_internet_list')
            except Exception as e:
                messages.error(request, f'Error al crear: {str(e)}')
        else:
            messages.error(request, 'El nombre, velocidad de descarga y precio mensual son requeridos.')
    
    return redirect('core:catalogo_plan_internet_list')


@login_required
def catalogo_plan_internet_update(request, pk):
    """Actualiza un plan de internet."""
    plan = get_object_or_404(PlanInternet, pk=pk)
    
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id', '')
        if registro_id and int(registro_id) != pk:
            pk = int(registro_id)
            plan = get_object_or_404(PlanInternet, pk=pk)
        
        nombre = request.POST.get('nombre', '').strip()
        velocidad_descarga = request.POST.get('velocidad_descarga', '').strip()
        velocidad_subida = request.POST.get('velocidad_subida', '').strip()
        precio_mensual = request.POST.get('precio_mensual', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        activo = request.POST.get('activo', '') == 'on'
        
        if nombre and velocidad_descarga and precio_mensual:
            try:
                plan.nombre = nombre
                plan.velocidad_descarga = int(velocidad_descarga)
                plan.velocidad_subida = int(velocidad_subida) if velocidad_subida else None
                plan.precio_mensual = float(precio_mensual)
                plan.descripcion = descripcion
                plan.activo = activo
                plan.save()
                messages.success(request, f'Plan de internet "{plan.nombre}" actualizado exitosamente.')
                return redirect('core:catalogo_plan_internet_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')
        else:
            messages.error(request, 'El nombre, velocidad de descarga y precio mensual son requeridos.')
    
    return redirect('core:catalogo_plan_internet_list')


@login_required
def catalogo_plan_internet_delete(request, pk):
    """Elimina un plan de internet."""
    plan = get_object_or_404(PlanInternet, pk=pk)
    
    if request.method == 'POST':
        nombre = str(plan)
        plan.delete()
        messages.success(request, f'Plan de internet "{nombre}" eliminado exitosamente.')
        return redirect('core:catalogo_plan_internet_list')
    
    return redirect('core:catalogo_plan_internet_list')

