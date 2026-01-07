from django.contrib import admin
from .models import ConfiguracionSistema


@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ['nombre_empresa', 'activa', 'fecha_actualizacion']
    list_filter = ['activa']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('activa', 'nombre_empresa', 'logo')
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
