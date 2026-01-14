"""
Vistas para gestionar roles y permisos desde el admin personalizado.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from .models import Rol, Permiso, PermisoRol, UsuarioRol, PerfilUsuario
from .roles_decorators import permiso_required
from .roles_utils import obtener_roles_usuario, obtener_permisos_usuario
from .forms import RolForm, PermisoForm, UsuarioForm

User = get_user_model()


@login_required
@permiso_required('gestionar_roles_permisos')
def roles_list(request):
    """Lista todos los roles del sistema."""
    roles = Rol.objects.all().annotate(
        cantidad_permisos=Count('permisos'),
        cantidad_usuarios=Count('usuario_roles', filter=Q(usuario_roles__activo=True))
    ).order_by('nombre')
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        roles = roles.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    # Filtro por estado
    estado_filter = request.GET.get('estado', '')
    if estado_filter == 'activo':
        roles = roles.filter(activo=True)
    elif estado_filter == 'inactivo':
        roles = roles.filter(activo=False)
    
    # Paginación
    paginator = Paginator(roles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'estado_filter': estado_filter,
    }
    return render(request, 'core/roles/rol_list.html', context)


@login_required
@permiso_required('gestionar_roles_permisos')
def roles_dashboard(request):
    """Dashboard de gestión de roles y permisos."""
    total_roles = Rol.objects.count()
    roles_activos = Rol.objects.filter(activo=True).count()
    total_permisos = Permiso.objects.count()
    permisos_activos = Permiso.objects.filter(activo=True).count()
    total_asignaciones = UsuarioRol.objects.filter(activo=True).count()
    
    # Roles más usados
    roles_populares = Rol.objects.annotate(
        cantidad_usuarios=Count('usuario_roles', filter=Q(usuario_roles__activo=True))
    ).order_by('-cantidad_usuarios')[:5]
    
    # Permisos por categoría
    permisos_por_categoria = Permiso.objects.values('categoria').annotate(
        total=Count('id')
    ).order_by('categoria')
    
    context = {
        'total_roles': total_roles,
        'roles_activos': roles_activos,
        'total_permisos': total_permisos,
        'permisos_activos': permisos_activos,
        'total_asignaciones': total_asignaciones,
        'roles_populares': roles_populares,
        'permisos_por_categoria': permisos_por_categoria,
    }
    return render(request, 'core/roles/roles_dashboard.html', context)


@login_required
@permiso_required('gestionar_roles_permisos')
def rol_create(request):
    """Crear un nuevo rol."""
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            rol = form.save()
            messages.success(request, f'Rol "{rol.nombre}" creado exitosamente.')
            return redirect('core:rol_detail', pk=rol.pk)
    else:
        form = RolForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Rol',
    }
    return render(request, 'core/roles/rol_form.html', context)


@login_required
@permiso_required('gestionar_roles_permisos')
def rol_update(request, pk):
    """Editar un rol existente."""
    rol = get_object_or_404(Rol, pk=pk)
    
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            rol = form.save()
            messages.success(request, f'Rol "{rol.nombre}" actualizado exitosamente.')
            return redirect('core:rol_detail', pk=rol.pk)
    else:
        form = RolForm(instance=rol)
    
    context = {
        'form': form,
        'rol': rol,
        'titulo': f'Editar Rol: {rol.nombre}',
    }
    return render(request, 'core/roles/rol_form.html', context)


@login_required
@permiso_required('gestionar_roles_permisos')
def rol_detail(request, pk):
    """Detalle de un rol con sus permisos y usuarios asignados."""
    rol = get_object_or_404(Rol, pk=pk)
    
    # Permisos del rol
    permisos = rol.permisos.all().order_by('categoria', 'nombre')
    
    # Usuarios con este rol
    usuarios_con_rol = User.objects.filter(
        usuario_roles__rol=rol,
        usuario_roles__activo=True
    ).distinct().order_by('username')
    
    context = {
        'rol': rol,
        'permisos': permisos,
        'usuarios_con_rol': usuarios_con_rol,
    }
    return render(request, 'core/roles/rol_detail.html', context)


@login_required
@permiso_required('gestionar_roles_permisos')
def rol_permisos_update(request, pk):
    """Actualizar permisos de un rol."""
    rol = get_object_or_404(Rol, pk=pk)
    
    if request.method == 'POST':
        permisos_ids = request.POST.getlist('permisos')
        permisos = Permiso.objects.filter(pk__in=permisos_ids, activo=True)
        rol.permisos.set(permisos)
        messages.success(request, f'Permisos del rol "{rol.nombre}" actualizados exitosamente.')
        return redirect('core:rol_detail', pk=rol.pk)
    
    # GET: Mostrar formulario
    todos_los_permisos = Permiso.objects.filter(activo=True).order_by('categoria', 'nombre')
    permisos_por_categoria = {}
    for permiso in todos_los_permisos:
        if permiso.categoria not in permisos_por_categoria:
            permisos_por_categoria[permiso.categoria] = []
        permisos_por_categoria[permiso.categoria].append(permiso)
    
    permisos_rol = set(rol.permisos.filter(activo=True).values_list('pk', flat=True))
    
    context = {
        'rol': rol,
        'permisos_por_categoria': permisos_por_categoria,
        'permisos_rol': permisos_rol,
    }
    return render(request, 'core/roles/rol_permisos_form.html', context)


@login_required
@permiso_required('gestionar_usuarios')
def usuarios_roles_list(request):
    """Lista usuarios con sus roles asignados."""
    usuarios = User.objects.annotate(
        cantidad_roles=Count('usuario_roles', filter=Q(usuario_roles__activo=True))
    ).order_by('username')
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    # Obtener roles para cada usuario
    usuarios_con_roles = []
    for usuario in usuarios:
        roles = obtener_roles_usuario(usuario)
        usuarios_con_roles.append({
            'usuario': usuario,
            'roles': roles,
        })
    
    # Paginación
    paginator = Paginator(usuarios_con_roles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'core/roles/usuarios_roles_list.html', context)


@login_required
@permiso_required('gestionar_usuarios')
def usuario_roles_manage(request, user_id):
    """Gestionar roles de un usuario específico."""
    usuario = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        # Procesar asignación/remoción de roles
        roles_seleccionados = request.POST.getlist('roles')
        
        # Obtener todos los roles activos
        todos_los_roles = Rol.objects.filter(activo=True)
        
        # Actualizar asignaciones
        for rol in todos_los_roles:
            usuario_rol, created = UsuarioRol.objects.get_or_create(
                usuario=usuario,
                rol=rol,
                defaults={'asignado_por': request.user, 'activo': True}
            )
            
            if str(rol.id) in roles_seleccionados:
                # Activar si está seleccionado
                if not usuario_rol.activo:
                    usuario_rol.activo = True
                    usuario_rol.asignado_por = request.user
                    usuario_rol.save()
            else:
                # Desactivar si no está seleccionado
                if usuario_rol.activo:
                    usuario_rol.activo = False
                    usuario_rol.save()
        
        messages.success(request, f'Roles actualizados para {usuario.username}')
        return redirect('core:usuario_roles_manage', user_id=user_id)
    
    # GET: Mostrar formulario
    todos_los_roles = Rol.objects.filter(activo=True).order_by('nombre')
    roles_activos_usuario = obtener_roles_usuario(usuario)
    ids_roles_activos = [r.id for r in roles_activos_usuario]
    
    context = {
        'usuario': usuario,
        'todos_los_roles': todos_los_roles,
        'roles_activos_usuario': roles_activos_usuario,
        'ids_roles_activos': ids_roles_activos,
    }
    return render(request, 'core/roles/usuario_roles_manage.html', context)


@login_required
@permiso_required('gestionar_usuarios')
def usuario_create(request):
    """Crear un nuevo usuario del sistema."""
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request_user=request.user)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.username}" creado exitosamente.')
            return redirect('core:usuario_update', user_id=usuario.pk)
    else:
        form = UsuarioForm(request_user=request.user)
    
    context = {
        'form': form,
        'titulo': 'Crear Usuario',
    }
    return render(request, 'core/roles/usuario_form.html', context)


@login_required
@permiso_required('gestionar_usuarios')
def usuario_update(request, user_id):
    """Editar un usuario del sistema."""
    usuario = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario, request_user=request.user)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.username}" actualizado exitosamente.')
            return redirect('core:usuarios_roles_list')
    else:
        form = UsuarioForm(instance=usuario, request_user=request.user)
    
    context = {
        'form': form,
        'usuario': usuario,
        'titulo': f'Editar Usuario: {usuario.username}',
    }
    return render(request, 'core/roles/usuario_form.html', context)


# ==================== PERMISOS ====================

@login_required
@permiso_required('gestionar_roles_permisos')
def permisos_list(request):
    """Lista todos los permisos del sistema."""
    permisos = Permiso.objects.all().order_by('categoria', 'nombre')
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        permisos = permisos.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(categoria__icontains=query)
        )
    
    # Filtro por categoría
    categoria_filter = request.GET.get('categoria', '')
    if categoria_filter:
        permisos = permisos.filter(categoria=categoria_filter)
    
    # Filtro por estado
    estado_filter = request.GET.get('estado', '')
    if estado_filter == 'activo':
        permisos = permisos.filter(activo=True)
    elif estado_filter == 'inactivo':
        permisos = permisos.filter(activo=False)
    
    # Obtener categorías únicas para el filtro
    categorias = Permiso.objects.values_list('categoria', flat=True).distinct().order_by('categoria')
    
    # Paginación
    paginator = Paginator(permisos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'categoria_filter': categoria_filter,
        'estado_filter': estado_filter,
        'categorias': categorias,
    }
    return render(request, 'core/roles/permiso_list.html', context)


@login_required
@permiso_required('gestionar_roles_permisos')
def permiso_create(request):
    """Crear un nuevo permiso."""
    if request.method == 'POST':
        form = PermisoForm(request.POST)
        if form.is_valid():
            permiso = form.save()
            messages.success(request, f'Permiso "{permiso.nombre}" creado exitosamente.')
            return redirect('core:permisos_list')
    else:
        form = PermisoForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Permiso',
    }
    return render(request, 'core/roles/permiso_form.html', context)


@login_required
@permiso_required('gestionar_roles_permisos')
def permiso_update(request, pk):
    """Editar un permiso existente."""
    permiso = get_object_or_404(Permiso, pk=pk)
    
    if request.method == 'POST':
        form = PermisoForm(request.POST, instance=permiso)
        if form.is_valid():
            permiso = form.save()
            messages.success(request, f'Permiso "{permiso.nombre}" actualizado exitosamente.')
            return redirect('core:permisos_list')
    else:
        form = PermisoForm(instance=permiso)
    
    context = {
        'form': form,
        'permiso': permiso,
        'titulo': f'Editar Permiso: {permiso.nombre}',
    }
    return render(request, 'core/roles/permiso_form.html', context)


@login_required
@permiso_required('gestionar_roles_permisos')
def permiso_detail(request, pk):
    """Detalle de un permiso con los roles que lo tienen."""
    permiso = get_object_or_404(Permiso, pk=pk)
    
    # Roles que tienen este permiso
    roles_con_permiso = Rol.objects.filter(
        permisos=permiso,
        activo=True
    ).distinct().order_by('nombre')
    
    context = {
        'permiso': permiso,
        'roles_con_permiso': roles_con_permiso,
    }
    return render(request, 'core/roles/permiso_detail.html', context)
