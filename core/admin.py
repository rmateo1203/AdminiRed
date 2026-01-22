from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.urls import path
from .models import (
    ConfiguracionSistema, Rol, Permiso, PermisoRol,
    PerfilUsuario, UsuarioRol
)


@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ['nombre_empresa', 'activa', 'pagos_online_habilitados', 'fecha_actualizacion']
    list_filter = ['activa', 'pagos_online_habilitados']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'pagos_online_habilitados_display']
    
    
    # El JavaScript y estilos están ahora en el template personalizado
    # templates/admin/core/configuracionsistema/change_form.html
    
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('activa', 'nombre_empresa', 'descripcion_sistema', 'titulo_sistema', 'logo')
        }),
        ('Configuración de Pagos', {
            'fields': ('pagos_online_habilitados_display',),
            'description': 'Si los pagos en línea están deshabilitados, los clientes no podrán pagar online. Los administradores podrán registrar pagos manuales cuando los clientes traigan comprobantes de depósito.',
        }),
        ('Colores del Sistema', {
            'fields': (
                'color_primario',
                'color_secundario',
                'color_exito',
                'color_advertencia',
                'color_peligro',
                'color_info',
            )
        }),
        ('Información', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def pagos_online_habilitados_display(self, obj):
        """Muestra el campo de pagos como checkbox editable."""
        if obj:
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    if 'sqlite' in connection.vendor:
                        cursor.execute(
                            "SELECT pagos_online_habilitados FROM core_configuracionsistema WHERE id = ?",
                            [obj.pk]
                        )
                    else:
                        cursor.execute(
                            "SELECT pagos_online_habilitados FROM core_configuracionsistema WHERE id = %s",
                            [obj.pk]
                        )
                    result = cursor.fetchone()
                    valor_actual = bool(result[0]) if result else True
            except:
                valor_actual = True
        else:
            valor_actual = True
        
        checked = 'checked' if valor_actual else ''
        return format_html(
            '<div style="margin: 10px 0; padding: 10px; background: #f9f9f9; border: 1px solid #ddd; border-radius: 4px;">'
            '<input type="checkbox" name="pagos_online_habilitados" id="id_pagos_online_habilitados" value="1" {} style="margin-right: 8px;"> '
            '<label for="id_pagos_online_habilitados" style="font-weight: bold;">Pagos en línea habilitados</label>'
            '<p class="help" style="margin-top: 8px; color: #666;">{}</p>'
            '</div>',
            checked,
            'Si está desactivado, los clientes no podrán pagar en línea. Los administradores podrán registrar pagos manuales cuando los clientes traigan comprobantes de depósito.'
        )
    pagos_online_habilitados_display.short_description = 'Pagos en línea habilitados'
    pagos_online_habilitados_display.allow_tags = True
    
    def save_model(self, request, obj, form, change):
        """Guarda el modelo y el campo de pagos desde el POST."""
        super().save_model(request, obj, form, change)
        
        # Guardar el valor del checkbox de pagos_online_habilitados
        if 'pagos_online_habilitados' in request.POST:
            valor = request.POST.get('pagos_online_habilitados') == '1'
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    valor_int = 1 if valor else 0
                    if 'sqlite' in connection.vendor:
                        cursor.execute(
                            "UPDATE core_configuracionsistema SET pagos_online_habilitados = ? WHERE id = ?",
                            [valor_int, obj.pk]
                        )
                    else:
                        cursor.execute(
                            "UPDATE core_configuracionsistema SET pagos_online_habilitados = %s WHERE id = %s",
                            [valor_int, obj.pk]
                        )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error al guardar pagos_online_habilitados: {e}")
    


# =============================================================================
# ADMIN PARA SISTEMA DE ROLES Y PERMISOS
# =============================================================================


class PermisoRolInline(admin.TabularInline):
    """Inline para gestionar permisos de un rol."""
    model = PermisoRol
    extra = 0
    verbose_name = 'Permiso'
    verbose_name_plural = 'Permisos del Rol'


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo', 'es_sistema', 'cantidad_permisos', 'cantidad_usuarios', 'fecha_actualizacion']
    list_filter = ['activo', 'es_sistema']
    search_fields = ['nombre', 'codigo', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    inlines = [PermisoRolInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'descripcion')
        }),
        ('Estado', {
            'fields': ('activo', 'es_sistema')
        }),
        ('Información', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def cantidad_permisos(self, obj):
        """Muestra la cantidad de permisos del rol."""
        count = obj.permisos.count()
        return format_html('<span style="color: {};">{}</span>', 
                          '#10b981' if count > 0 else '#999', count)
    cantidad_permisos.short_description = 'Permisos'
    
    def cantidad_usuarios(self, obj):
        """Muestra la cantidad de usuarios con este rol."""
        count = obj.usuario_roles.filter(activo=True).count()
        return format_html('<span style="color: {};">{}</span>', 
                          '#3b82f6' if count > 0 else '#999', count)
    cantidad_usuarios.short_description = 'Usuarios'


@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'categoria', 'activo', 'cantidad_roles', 'fecha_actualizacion']
    list_filter = ['activo', 'categoria']
    search_fields = ['nombre', 'codigo', 'descripcion', 'categoria']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'categoria', 'descripcion')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Información', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def cantidad_roles(self, obj):
        """Muestra la cantidad de roles que tienen este permiso."""
        count = obj.roles.count()
        return format_html('<span style="color: {};">{}</span>', 
                          '#10b981' if count > 0 else '#999', count)
    cantidad_roles.short_description = 'Roles'


@admin.register(PermisoRol)
class PermisoRolAdmin(admin.ModelAdmin):
    list_display = ['rol', 'permiso', 'fecha_asignacion']
    list_filter = ['rol', 'permiso', 'fecha_asignacion']
    search_fields = ['rol__nombre', 'permiso__nombre', 'permiso__codigo']
    readonly_fields = ['fecha_asignacion']


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo_usuario', 'telefono', 'fecha_actualizacion']
    list_filter = ['tipo_usuario']
    search_fields = ['usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name', 'telefono']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('usuario',)
        }),
        ('Información Personal', {
            'fields': ('tipo_usuario', 'telefono', 'foto', 'fecha_nacimiento', 'direccion')
        }),
        ('Información Adicional', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
        ('Información', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UsuarioRol)
class UsuarioRolAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol', 'activo', 'usuario_is_staff', 'asignado_por', 'fecha_asignacion']
    list_filter = ['rol', 'activo', 'fecha_asignacion']
    search_fields = ['usuario__username', 'usuario__email', 'rol__nombre', 'rol__codigo']
    readonly_fields = ['fecha_asignacion']
    list_editable = ['activo']
    
    fieldsets = (
        ('Asignación', {
            'fields': ('usuario', 'rol', 'activo', 'asignado_por'),
            'description': 'Nota: Al asignar un rol del sistema (excepto Cliente), el usuario automáticamente obtendrá is_staff=True para poder acceder al sistema.'
        }),
        ('Información', {
            'fields': ('fecha_asignacion',),
            'classes': ('collapse',)
        }),
    )
    
    def usuario_is_staff(self, obj):
        """Muestra si el usuario tiene is_staff activo."""
        if obj.usuario.is_staff:
            return format_html('<span style="color: #10b981;">✓ Sí</span>')
        return format_html('<span style="color: #ef4444;">✗ No</span>')
    usuario_is_staff.short_description = 'Usuario Staff'
    
    def save_model(self, request, obj, form, change):
        """Guarda el modelo y actualiza is_staff si es necesario."""
        # Establecer asignado_por si no está establecido
        if not obj.asignado_por:
            obj.asignado_por = request.user
        
        super().save_model(request, obj, form, change)
        
        # Las señales se encargarán de actualizar is_staff automáticamente
        # pero podemos forzar una actualización aquí como respaldo
        usuario = obj.usuario
        rol = obj.rol
        
        # Si el rol es 'cliente', no activar is_staff
        if rol.codigo == 'cliente':
            if usuario.is_staff and not usuario.is_superuser:
                usuario.is_staff = False
                usuario.save(update_fields=['is_staff'])
        # Si el rol está activo y no es 'cliente', activar is_staff
        elif obj.activo and rol.activo:
            if not usuario.is_staff:
                usuario.is_staff = True
                usuario.save(update_fields=['is_staff'])
