from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Cliente
from .forms import ClienteForm


@login_required
def cliente_list(request):
    """Lista todos los clientes con búsqueda y paginación."""
    clientes = Cliente.objects.all()
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(apellido1__icontains=query) |
            Q(apellido2__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query) |
            Q(ciudad__icontains=query)
        )
    
    # Filtro por estado
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        clientes = clientes.filter(estado_cliente=estado_filter)
    
    # Ordenamiento
    orden = request.GET.get('orden', '-fecha_registro')
    # Si el orden es por nombre, ordenar por apellido1 y luego nombre
    if orden in ['nombre', '-nombre']:
        if orden == 'nombre':
            clientes = clientes.order_by('apellido1', 'apellido2', 'nombre')
        else:
            clientes = clientes.order_by('-apellido1', '-apellido2', '-nombre')
    else:
        clientes = clientes.order_by(orden)
    
    # Paginación
    paginator = Paginator(clientes, 15)  # 15 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado_filter': estado_filter,
        'orden': orden,
        'estados': Cliente.ESTADO_CHOICES,
    }
    
    return render(request, 'clientes/cliente_list.html', context)


@login_required
def cliente_detail(request, pk):
    """Muestra el detalle de un cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Obtener instalaciones relacionadas
    instalaciones = cliente.instalaciones.all()[:5]
    
    # Obtener pagos relacionados
    pagos = cliente.pagos.all().order_by('-fecha_vencimiento')[:5]
    
    context = {
        'cliente': cliente,
        'instalaciones': instalaciones,
        'pagos': pagos,
    }
    
    return render(request, 'clientes/cliente_detail.html', context)


@login_required
def cliente_create(request):
    """Crea un nuevo cliente."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre_completo}" creado exitosamente.')
            return redirect('clientes:cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
        'title': 'Nuevo Cliente',
    }
    
    return render(request, 'clientes/cliente_form.html', context)


@login_required
def cliente_update(request, pk):
    """Actualiza un cliente existente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre_completo}" actualizado exitosamente.')
            return redirect('clientes:cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
        'title': f'Editar Cliente: {cliente.nombre_completo}',
    }
    
    return render(request, 'clientes/cliente_form.html', context)


@login_required
def cliente_delete(request, pk):
    """Elimina un cliente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        nombre_completo = cliente.nombre_completo
        cliente.delete()
        messages.success(request, f'Cliente "{nombre_completo}" eliminado exitosamente.')
        return redirect('cliente_list')
    
    context = {
        'cliente': cliente,
    }
    
    return render(request, 'clientes/cliente_confirm_delete.html', context)
