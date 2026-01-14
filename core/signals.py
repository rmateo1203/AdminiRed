# -*- coding: utf-8 -*-
"""
Señales para el sistema de roles y permisos.
Activa automáticamente is_staff cuando se asigna un rol del sistema.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UsuarioRol


@receiver(post_save, sender=UsuarioRol)
def activar_is_staff_al_asignar_rol(sender, instance, created, **kwargs):
    """
    Activa automáticamente is_staff cuando se asigna un rol del sistema
    (cualquier rol excepto 'cliente') a un usuario.
    """
    usuario = instance.usuario
    rol = instance.rol
    
    # Si el rol es 'cliente', no activar is_staff (los clientes no son staff)
    if rol.codigo == 'cliente':
        # Asegurar que los clientes NO sean staff
        if usuario.is_staff and not usuario.is_superuser:
            usuario.is_staff = False
            usuario.save(update_fields=['is_staff'])
        return
    
    # Si el rol está activo y el rol no es 'cliente', activar is_staff
    if instance.activo and rol.activo:
        if not usuario.is_staff:
            usuario.is_staff = True
            usuario.save(update_fields=['is_staff'])


@receiver(post_save, sender=UsuarioRol)
def actualizar_is_staff_al_cambiar_estado_rol(sender, instance, **kwargs):
    """
    Actualiza is_staff cuando se cambia el estado activo de un rol.
    Si se desactiva un rol del sistema, verifica si el usuario tiene otros roles activos.
    """
    usuario = instance.usuario
    rol = instance.rol
    
    # Si el rol es 'cliente', no hacer nada
    if rol.codigo == 'cliente':
        return
    
    # Si se desactiva el rol, verificar si el usuario tiene otros roles activos del sistema
    if not instance.activo:
        # Verificar si tiene otros roles activos del sistema (no cliente)
        otros_roles_activos = UsuarioRol.objects.filter(
            usuario=usuario,
            activo=True
        ).exclude(rol__codigo='cliente').exclude(pk=instance.pk).exists()
        
        # Si no tiene otros roles activos del sistema, desactivar is_staff
        if not otros_roles_activos and not usuario.is_superuser:
            usuario.is_staff = False
            usuario.save(update_fields=['is_staff'])
    else:
        # Si se activa el rol, activar is_staff
        if not usuario.is_staff:
            usuario.is_staff = True
            usuario.save(update_fields=['is_staff'])


@receiver(post_delete, sender=UsuarioRol)
def actualizar_is_staff_al_eliminar_rol(sender, instance, **kwargs):
    """
    Actualiza is_staff cuando se elimina un rol de un usuario.
    Si era el único rol del sistema activo, desactiva is_staff.
    """
    usuario = instance.usuario
    rol = instance.rol
    
    # Si el rol es 'cliente', no hacer nada
    if rol.codigo == 'cliente':
        return
    
    # Verificar si el usuario tiene otros roles activos del sistema (no cliente)
    otros_roles_activos = UsuarioRol.objects.filter(
        usuario=usuario,
        activo=True
    ).exclude(rol__codigo='cliente').exists()
    
    # Si no tiene otros roles activos del sistema, desactivar is_staff
    if not otros_roles_activos and not usuario.is_superuser:
        usuario.is_staff = False
        usuario.save(update_fields=['is_staff'])

