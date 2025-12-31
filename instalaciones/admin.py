from django.contrib import admin
from .models import TipoInstalacion, PlanInternet, Instalacion, ConfiguracionNumeroContrato


@admin.register(TipoInstalacion)
class TipoInstalacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']


@admin.register(PlanInternet)
class PlanInternetAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'velocidad_descarga', 'velocidad_subida', 'precio_mensual', 'activo']
    list_filter = ['activo', 'velocidad_descarga']
    search_fields = ['nombre', 'descripcion']
    ordering = ['precio_mensual', 'velocidad_descarga']


@admin.register(ConfiguracionNumeroContrato)
class ConfiguracionNumeroContratoAdmin(admin.ModelAdmin):
    list_display = ['formato', 'prefijo', 'numero_inicial', 'digitos_secuencia', 'reiniciar_diario', 'activa', 'fecha_actualizacion']
    list_filter = ['activa', 'reiniciar_diario']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Configuración General', {
            'fields': ('activa', 'formato', 'prefijo')
        }),
        ('Secuencia', {
            'fields': ('numero_inicial', 'digitos_secuencia', 'reiniciar_diario')
        }),
        ('Información', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Instalacion)
class InstalacionAdmin(admin.ModelAdmin):
    list_display = [
        'numero_contrato',
        'cliente',
        'plan_nombre',
        'velocidad_descarga',
        'precio_mensual',
        'estado',
        'fecha_solicitud',
        'fecha_instalacion'
    ]
    list_filter = ['estado', 'tipo_instalacion', 'fecha_solicitud', 'fecha_instalacion']
    search_fields = ['numero_contrato', 'cliente__nombre', 'cliente__telefono', 'direccion_instalacion']
    readonly_fields = ['fecha_solicitud']
    date_hierarchy = 'fecha_solicitud'
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('cliente', 'numero_contrato')
        }),
        ('Detalles de la Instalación', {
            'fields': (
                'tipo_instalacion',
                'direccion_instalacion',
                'coordenadas',
                'plan_nombre',
                'velocidad_descarga',
                'velocidad_subida',
                'precio_mensual'
            )
        }),
        ('Estado y Fechas', {
            'fields': (
                'estado',
                'fecha_solicitud',
                'fecha_programada',
                'fecha_instalacion',
                'fecha_activacion'
            )
        }),
        ('Información Técnica', {
            'fields': ('ip_asignada', 'mac_equipo'),
            'classes': ('collapse',)
        }),
        ('Notas', {
            'fields': ('notas_instalacion', 'notas_tecnicas'),
            'classes': ('collapse',)
        }),
    )
