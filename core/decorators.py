"""
Decoradores personalizados para permisos y seguridad.
"""
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def staff_required(view_func):
    """
    Decorador que requiere que el usuario sea staff.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def superuser_required(view_func):
    """
    Decorador que requiere que el usuario sea superusuario.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_superuser:
            messages.error(request, 'Solo los administradores pueden acceder a esta sección.')
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def permission_required(permission):
    """
    Decorador que requiere un permiso específico.
    
    Uso:
        @permission_required('app.permission')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not request.user.has_perm(permission):
                messages.error(request, 'No tienes permisos para realizar esta acción.')
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


