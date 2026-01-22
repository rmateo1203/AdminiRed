"""
Utilidades y funciones helper para el sistema de roles y permisos.
"""
from django.contrib.auth import get_user_model
from .models import Rol, Permiso, PerfilUsuario, UsuarioRol

User = get_user_model()


def obtener_roles_usuario(user):
    """Obtiene todos los roles activos de un usuario."""
    if not user or not user.is_authenticated:
        return Rol.objects.none()
    
    return Rol.objects.filter(
        usuario_roles__usuario=user,
        usuario_roles__activo=True,
        activo=True
    ).distinct()


def usuario_tiene_rol(user, codigo_rol):
    """Verifica si un usuario tiene un rol específico."""
    if not user or not user.is_authenticated:
        return False
    
    return UsuarioRol.objects.filter(
        usuario=user,
        rol__codigo=codigo_rol,
        rol__activo=True,
        activo=True
    ).exists()


def usuario_tiene_permiso(user, codigo_permiso):
    """
    Verifica si un usuario tiene un permiso específico.
    Un usuario tiene un permiso si alguno de sus roles tiene ese permiso.
    Los superusuarios tienen todos los permisos.
    """
    if not user or not user.is_authenticated:
        return False
    
    # Los superusuarios tienen todos los permisos
    if user.is_superuser:
        return True
    
    # Obtener todos los roles activos del usuario
    roles_usuario = obtener_roles_usuario(user)
    
    # Verificar si alguno de los roles tiene el permiso
    return Permiso.objects.filter(
        codigo=codigo_permiso,
        activo=True,
        roles__in=roles_usuario
    ).exists()


def obtener_permisos_usuario(user):
    """Obtiene todos los permisos de un usuario (a través de sus roles)."""
    if not user or not user.is_authenticated:
        return Permiso.objects.none()
    
    # Los superusuarios tienen todos los permisos
    if user.is_superuser:
        return Permiso.objects.filter(activo=True)
    
    roles_usuario = obtener_roles_usuario(user)
    return Permiso.objects.filter(
        roles__in=roles_usuario,
        activo=True
    ).distinct()


def obtener_o_crear_perfil(user):
    """Obtiene el perfil de un usuario o lo crea si no existe."""
    if not user or not user.is_authenticated:
        return None
    
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
    return perfil


def asignar_rol_usuario(user, codigo_rol, asignado_por=None):
    """
    Asigna un rol a un usuario.
    
    Args:
        user: Usuario al que se asignará el rol
        codigo_rol: Código del rol a asignar
        asignado_por: Usuario que asigna el rol (opcional)
    
    Returns:
        UsuarioRol: La instancia creada o actualizada
    """
    try:
        rol = Rol.objects.get(codigo=codigo_rol, activo=True)
    except Rol.DoesNotExist:
        raise ValueError(f"El rol con código '{codigo_rol}' no existe o está inactivo.")
    
    usuario_rol, created = UsuarioRol.objects.get_or_create(
        usuario=user,
        rol=rol,
        defaults={'asignado_por': asignado_por, 'activo': True}
    )
    
    if not created and not usuario_rol.activo:
        usuario_rol.activo = True
        usuario_rol.asignado_por = asignado_por
        usuario_rol.save()
    
    return usuario_rol


def remover_rol_usuario(user, codigo_rol):
    """
    Remueve un rol de un usuario (marca como inactivo).
    
    Args:
        user: Usuario del que se removerá el rol
        codigo_rol: Código del rol a remover
    
    Returns:
        bool: True si se removió, False si no existía
    """
    try:
        rol = Rol.objects.get(codigo=codigo_rol)
        usuario_rol = UsuarioRol.objects.get(usuario=user, rol=rol)
        usuario_rol.activo = False
        usuario_rol.save()
        return True
    except (Rol.DoesNotExist, UsuarioRol.DoesNotExist):
        return False







