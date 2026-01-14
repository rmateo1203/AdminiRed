"""
Template tags para verificar permisos y roles en templates.
"""
from django import template
from ..roles_utils import usuario_tiene_permiso, usuario_tiene_rol, obtener_permisos_usuario

register = template.Library()


@register.filter(name='has_permiso')
def has_permiso(user, codigo_permiso):
    """
    Template filter para verificar si un usuario tiene un permiso.
    
    Uso:
        {% load roles_tags %}
        {% if user|has_permiso:'ver_clientes' %}
            <a href="...">Ver Clientes</a>
        {% endif %}
    """
    if not user or not user.is_authenticated:
        return False
    
    # Los superusuarios siempre tienen todos los permisos
    if user.is_superuser:
        return True
    
    return usuario_tiene_permiso(user, codigo_permiso)


@register.filter(name='has_rol')
def has_rol(user, codigo_rol):
    """
    Template filter para verificar si un usuario tiene un rol.
    
    Uso:
        {% load roles_tags %}
        {% if user|has_rol:'administrador' %}
            <a href="...">Configuración</a>
        {% endif %}
    """
    if not user or not user.is_authenticated:
        return False
    
    # Los superusuarios siempre tienen todos los roles (lógica especial)
    if user.is_superuser:
        return True
    
    return usuario_tiene_rol(user, codigo_rol)


@register.filter(name='tiene_permiso')
def tiene_permiso(user, codigo_permiso):
    """
    Alias de has_permiso para compatibilidad.
    Verifica si el usuario tiene un permiso específico.
    """
    return has_permiso(user, codigo_permiso)


@register.filter(name='puede_ver_modulo')
def puede_ver_modulo(user, categoria):
    """
    Verifica si el usuario puede ver un módulo completo (tiene al menos un permiso de esa categoría).
    
    Uso:
        {% load roles_tags %}
        {% if user|puede_ver_modulo:'clientes' %}
            <li><a href="{% url 'clientes:cliente_list' %}">Clientes</a></li>
        {% endif %}
    """
    if not user or not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    permisos = obtener_permisos_usuario(user)
    return permisos.filter(categoria=categoria).exists()


@register.simple_tag
def permisos_usuario(user, categoria=None):
    """
    Obtiene los permisos del usuario, opcionalmente filtrados por categoría.
    
    Uso:
        {% load roles_tags %}
        {% permisos_usuario user 'clientes' as permisos_clientes %}
        {% for permiso in permisos_clientes %}
            <span>{{ permiso.nombre }}</span>
        {% endfor %}
    """
    if not user or not user.is_authenticated:
        return []
    
    permisos = obtener_permisos_usuario(user)
    if categoria:
        permisos = permisos.filter(categoria=categoria)
    return permisos


