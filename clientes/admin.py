from django.contrib import admin
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
        'fecha_registro',
        'estado_display'
    ]
    list_filter = [
        'estado_cliente',
        'ciudad',
        'estado',
        'fecha_registro',
    ]
    search_fields = ['nombre', 'apellido1', 'apellido2', 'telefono', 'email', 'direccion']
    readonly_fields = [
        'fecha_registro',
        'fecha_actualizacion',
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
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def nombre_completo_display(self, obj):
        """Muestra el nombre completo del cliente."""
        return obj.nombre_completo
    nombre_completo_display.short_description = 'Cliente'
    nombre_completo_display.admin_order_field = 'nombre'
    
    def estado_display(self, obj):
        """Muestra el estado del cliente con colores."""
        estado_colores = {
            'activo': '#10b981',
            'inactivo': '#6b7280',
            'suspendido': '#f59e0b',
            'cancelado': '#ef4444',
        }
        color = estado_colores.get(obj.estado_cliente, '#6b7280')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_cliente_display()
        )
    estado_display.short_description = 'Estado'
    estado_display.admin_order_field = 'estado_cliente'
