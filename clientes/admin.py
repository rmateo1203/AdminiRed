from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'email', 'ciudad', 'estado_cliente', 'fecha_registro']
    list_filter = ['estado_cliente', 'ciudad', 'estado', 'fecha_registro']
    search_fields = ['nombre', 'telefono', 'email', 'direccion']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'email', 'telefono')
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
