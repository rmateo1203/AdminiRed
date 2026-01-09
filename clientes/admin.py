from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(SimpleHistoryAdmin):
    list_display = [
        'nombre_completo_display',
        'telefono',
        'email',
        'ciudad',
        'estado_cliente',
        'created_at',
        'is_deleted_display',
        'auditoria_display'
    ]
    list_filter = [
        'estado_cliente',
        'ciudad',
        'estado',
        'created_at',
        'is_deleted',
        'created_by',
    ]
    search_fields = ['nombre', 'apellido1', 'apellido2', 'telefono', 'email', 'direccion']
    readonly_fields = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'deleted_at',
        'deleted_by',
        'is_deleted',
        'usuario',
    ]
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido1', 'apellido2', 'email', 'telefono')
        }),
        ('Dirección', {
            'fields': ('direccion', 'ciudad', 'estado', 'codigo_postal')
        }),
        ('Estado', {
            'fields': ('estado_cliente',)
        }),
        ('Información Adicional', {
            'fields': ('notas',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Portal de Cliente', {
            'fields': ('usuario', 'debe_cambiar_password'),
            'classes': ('collapse',),
            'description': 'Usuario que puede acceder al portal de cliente'
        }),
        ('Soft Delete', {
            'fields': ('is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filtrar eliminados por defecto, pero permitir verlos con filtro."""
        qs = super().get_queryset(request)
        # Si hay filtro de is_deleted, mostrar todos
        if 'is_deleted__exact' in request.GET:
            return qs
        # Por defecto, mostrar solo no eliminados
        return qs.filter(is_deleted=False)
    
    def nombre_completo_display(self, obj):
        """Muestra el nombre completo del cliente."""
        return obj.nombre_completo
    nombre_completo_display.short_description = 'Cliente'
    nombre_completo_display.admin_order_field = 'nombre'
    
    def is_deleted_display(self, obj):
        """Muestra si el cliente está eliminado."""
        if obj.is_deleted:
            return format_html(
                '<span style="color: red; font-weight: bold;">✓ Eliminado</span>'
            )
        return format_html('<span style="color: green;">Activo</span>')
    is_deleted_display.short_description = 'Estado'
    is_deleted_display.admin_order_field = 'is_deleted'
    
    def auditoria_display(self, obj):
        """Muestra información de auditoría."""
        info = []
        if obj.created_by:
            info.append(f'Creado por: {obj.created_by.username}')
        if obj.updated_by:
            info.append(f'Actualizado por: {obj.updated_by.username}')
        if obj.deleted_by:
            info.append(f'Eliminado por: {obj.deleted_by.username}')
        return format_html('<br>'.join(info)) if info else '-'
    auditoria_display.short_description = 'Auditoría'
    
    def save_model(self, request, obj, form, change):
        """Sobrescribe save_model para agregar auditoría."""
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Sobrescribe delete_model para usar soft delete."""
        obj.soft_delete(user=request.user)
    
    def delete_queryset(self, request, queryset):
        """Sobrescribe delete_queryset para usar soft delete."""
        for obj in queryset:
            obj.soft_delete(user=request.user)
    
    actions = ['restaurar_clientes', 'eliminar_permanentemente', 'crear_usuario_portal', 'forzar_cambio_password']
    
    def restaurar_clientes(self, request, queryset):
        """Acción para restaurar clientes eliminados."""
        restaurados = 0
        for cliente in queryset.filter(is_deleted=True):
            cliente.restore(user=request.user)
            restaurados += 1
        self.message_user(
            request,
            f'{restaurados} cliente(s) restaurado(s) exitosamente.'
        )
    restaurar_clientes.short_description = 'Restaurar clientes seleccionados'
    
    def eliminar_permanentemente(self, request, queryset):
        """Acción para eliminar permanentemente (hard delete)."""
        eliminados = 0
        for cliente in queryset:
            cliente.delete(hard_delete=True)
            eliminados += 1
        self.message_user(
            request,
            f'{eliminados} cliente(s) eliminado(s) permanentemente.'
        )
    eliminar_permanentemente.short_description = 'Eliminar permanentemente (¡CUIDADO!)'
    
    def crear_usuario_portal(self, request, queryset):
        """Acción para crear usuarios del portal para clientes seleccionados."""
        import secrets
        import string
        
        creados = 0
        ya_tienen = 0
        errores = 0
        
        for cliente in queryset:
            if cliente.usuario:
                ya_tienen += 1
                continue  # Ya tiene usuario
            
            if cliente.is_deleted:
                continue  # No crear usuarios para eliminados
            
            try:
                # Crear usuario (generará contraseña automáticamente y enviará email)
                usuario = cliente.crear_usuario_portal(enviar_email=True)
                creados += 1
                
                # Obtener la contraseña generada (si fue generada automáticamente)
                # Nota: No podemos obtener la contraseña después de crearla por seguridad
                # El email se envió automáticamente con las credenciales
                self.message_user(
                    request,
                    f'✅ Usuario creado para {cliente.nombre_completo} ({usuario.username}). '
                    f'Las credenciales se han enviado por email a {cliente.email}',
                    level=messages.SUCCESS
                )
            except Exception as e:
                errores += 1
                self.message_user(
                    request,
                    f'❌ Error al crear usuario para {cliente.nombre_completo}: {str(e)}',
                    level=messages.ERROR
                )
        
        # Mensaje resumen
        if creados > 0:
            self.message_user(
                request,
                f'✅ {creados} usuario(s) creado(s) exitosamente. {ya_tienen} cliente(s) ya tenían usuario. {errores} error(es).',
                level=messages.SUCCESS
            )
        elif ya_tienen > 0:
            self.message_user(
                request,
                f'ℹ️ {ya_tienen} cliente(s) seleccionado(s) ya tienen usuario asignado.',
                level=messages.INFO
            )
    
    crear_usuario_portal.short_description = '🔐 Crear usuario para portal (clientes seleccionados)'
    
    def forzar_cambio_password(self, request, queryset):
        """Acción para forzar el cambio de contraseña a los clientes seleccionados."""
        count = queryset.update(debe_cambiar_password=True)
        self.message_user(
            request,
            f'{count} cliente(s) deberán cambiar su contraseña en el próximo inicio de sesión.',
            messages.SUCCESS
        )
    forzar_cambio_password.short_description = '🔒 Forzar cambio de contraseña'
