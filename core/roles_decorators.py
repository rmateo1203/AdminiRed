"""
Decoradores para control de acceso basado en roles y permisos.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .roles_utils import usuario_tiene_rol, usuario_tiene_permiso


def rol_required(*codigos_rol):
    """
    Decorador que requiere que el usuario tenga al menos uno de los roles especificados.
    
    Uso:
        @rol_required('admin', 'supervisor')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            # Verificar si el usuario tiene alguno de los roles requeridos
            tiene_rol = any(usuario_tiene_rol(request.user, codigo) for codigo in codigos_rol)
            
            # Los superusuarios siempre tienen acceso
            if not tiene_rol and not request.user.is_superuser:
                messages.warning(
                    request, 
                    'No tienes los permisos necesarios para acceder a esta sección. '
                    'Si crees que esto es un error, contacta al administrador del sistema.'
                )
                return redirect('core:sin_permisos')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def permiso_required(codigo_permiso):
    """
    Decorador que requiere que el usuario tenga un permiso específico.
    
    Uso:
        @permiso_required('ver_clientes')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            if not usuario_tiene_permiso(request.user, codigo_permiso):
                messages.warning(
                    request, 
                    'No tienes los permisos necesarios para acceder a esta sección. '
                    'Si crees que esto es un error, contacta al administrador del sistema.'
                )
                return redirect('core:sin_permisos')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def permisos_required(*codigos_permiso, require_all=False):
    """
    Decorador que requiere que el usuario tenga uno o todos los permisos especificados.
    
    Args:
        *codigos_permiso: Códigos de permisos requeridos
        require_all: Si es True, requiere todos los permisos. Si es False, requiere al menos uno.
    
    Uso:
        @permisos_required('ver_clientes', 'editar_clientes')  # Requiere al menos uno
        @permisos_required('ver_clientes', 'editar_clientes', require_all=True)  # Requiere ambos
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            # Verificar permisos
            if require_all:
                tiene_permisos = all(usuario_tiene_permiso(request.user, codigo) for codigo in codigos_permiso)
            else:
                tiene_permisos = any(usuario_tiene_permiso(request.user, codigo) for codigo in codigos_permiso)
            
            if not tiene_permisos:
                messages.warning(
                    request, 
                    'No tienes los permisos necesarios para acceder a esta sección. '
                    'Si crees que esto es un error, contacta al administrador del sistema.'
                )
                return redirect('core:sin_permisos')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


