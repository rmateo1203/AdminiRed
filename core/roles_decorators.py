# -*- coding: utf-8 -*-
"""
Decoradores para el sistema de roles y permisos.
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from .roles_utils import usuario_tiene_permiso


def permiso_required(codigo_permiso, redirect_url=None, ajax_403=True):
    """
    Decorador que verifica si un usuario tiene un permiso específico.
    
    Args:
        codigo_permiso: Código del permiso requerido (ej: 'ver_pagos', 'crear_clientes')
        redirect_url: URL a la que redirigir si no tiene permiso (por defecto: home)
        ajax_403: Si es True, devuelve JSON 403 para peticiones AJAX
    
    Uso:
        @permiso_required('ver_pagos')
        def pago_list(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            # Verificar si el usuario tiene el permiso
            if not usuario_tiene_permiso(request.user, codigo_permiso):
                # Si es una petición AJAX, devolver JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and ajax_403:
                    return JsonResponse({
                        'error': 'No tienes permiso para realizar esta acción.',
                        'permiso_requerido': codigo_permiso
                    }, status=403)
                
                # Mostrar mensaje de error
                messages.error(
                    request,
                    f'No tienes permiso para acceder a esta sección. '
                    f'Se requiere el permiso: {codigo_permiso}'
                )
                
                # Redirigir a la URL especificada o a home
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    # Intentar redirigir a home
                    try:
                        return redirect('home')
                    except:
                        # Si no existe la URL home, devolver 403
                        return HttpResponseForbidden(
                            f'No tienes permiso para acceder a esta sección. '
                            f'Se requiere el permiso: {codigo_permiso}'
                        )
            
            # Si tiene permiso, ejecutar la vista normalmente
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    return decorator


def rol_required(codigo_rol, redirect_url=None, ajax_403=True):
    """
    Decorador que verifica si un usuario tiene un rol específico.
    
    Args:
        codigo_rol: Código del rol requerido (ej: 'administrador', 'supervisor')
        redirect_url: URL a la que redirigir si no tiene el rol
        ajax_403: Si es True, devuelve JSON 403 para peticiones AJAX
    
    Uso:
        @rol_required('administrador')
        def admin_view(request):
            ...
    """
    from .roles_utils import usuario_tiene_rol
    
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            # Verificar si el usuario tiene el rol
            if not usuario_tiene_rol(request.user, codigo_rol):
                # Si es una petición AJAX, devolver JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and ajax_403:
                    return JsonResponse({
                        'error': 'No tienes el rol necesario para realizar esta acción.',
                        'rol_requerido': codigo_rol
                    }, status=403)
                
                # Mostrar mensaje de error
                messages.error(
                    request,
                    f'No tienes el rol necesario para acceder a esta sección. '
                    f'Se requiere el rol: {codigo_rol}'
                )
                
                # Redirigir a la URL especificada o a home
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    try:
                        return redirect('home')
                    except:
                        return HttpResponseForbidden(
                            f'No tienes el rol necesario para acceder a esta sección. '
                            f'Se requiere el rol: {codigo_rol}'
                        )
            
            # Si tiene el rol, ejecutar la vista normalmente
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    return decorator


def permisos_required(*codigos_permisos, redirect_url=None, ajax_403=True, require_all=False):
    """
    Decorador que verifica si un usuario tiene uno o más permisos.
    
    Args:
        *codigos_permisos: Códigos de permisos requeridos (uno o más)
        redirect_url: URL a la que redirigir si no tiene los permisos
        ajax_403: Si es True, devuelve JSON 403 para peticiones AJAX
        require_all: Si es True, requiere todos los permisos. Si es False, requiere al menos uno.
    
    Uso:
        @permisos_required('ver_pagos', 'editar_pagos')  # Requiere al menos uno
        @permisos_required('ver_pagos', 'editar_pagos', require_all=True)  # Requiere ambos
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            # Verificar permisos
            tiene_permisos = []
            for codigo_permiso in codigos_permisos:
                tiene_permisos.append(usuario_tiene_permiso(request.user, codigo_permiso))
            
            # Si require_all=True, todos deben ser True. Si False, al menos uno debe ser True.
            if require_all:
                tiene_acceso = all(tiene_permisos)
            else:
                tiene_acceso = any(tiene_permisos)
            
            if not tiene_acceso:
                # Si es una petición AJAX, devolver JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and ajax_403:
                    return JsonResponse({
                        'error': 'No tienes los permisos necesarios para realizar esta acción.',
                        'permisos_requeridos': list(codigos_permisos),
                        'require_all': require_all
                    }, status=403)
                
                # Mostrar mensaje de error
                permisos_str = ', '.join(codigos_permisos)
                modo = 'todos' if require_all else 'al menos uno'
                messages.error(
                    request,
                    f'No tienes los permisos necesarios para acceder a esta sección. '
                    f'Se requiere {modo} de: {permisos_str}'
                )
                
                # Redirigir
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    try:
                        return redirect('home')
                    except:
                        return HttpResponseForbidden(
                            f'No tienes los permisos necesarios para acceder a esta sección. '
                            f'Se requiere {modo} de: {permisos_str}'
                        )
            
            # Si tiene acceso, ejecutar la vista normalmente
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    return decorator
