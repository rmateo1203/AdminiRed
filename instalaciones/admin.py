from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import TipoInstalacion, PlanInternet, Instalacion, MaterialInstalacion, CambioEstadoInstalacion


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


@admin.register(Instalacion)
class InstalacionAdmin(SimpleHistoryAdmin):
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


@admin.register(MaterialInstalacion)
class MaterialInstalacionAdmin(admin.ModelAdmin):
    list_display = ['instalacion', 'material', 'cantidad', 'material_stock']
    list_filter = ['instalacion__estado', 'material__categoria']
    search_fields = ['instalacion__numero_contrato', 'material__nombre', 'material__codigo']
    readonly_fields = ['material_stock']
    
    def material_stock(self, obj):
        """Muestra el stock disponible del material."""
        if obj.material:
            return f"{obj.material.stock_actual} {obj.material.get_unidad_medida_display()}"
        return '-'
    material_stock.short_description = 'Stock Disponible'


@admin.register(CambioEstadoInstalacion)
class CambioEstadoInstalacionAdmin(admin.ModelAdmin):
    list_display = ['instalacion', 'estado_anterior', 'estado_nuevo', 'fecha_cambio', 'usuario']
    list_filter = ['estado_anterior', 'estado_nuevo', 'fecha_cambio']
    search_fields = ['instalacion__numero_contrato', 'instalacion__cliente__nombre', 'notas']
    readonly_fields = ['fecha_cambio']
    date_hierarchy = 'fecha_cambio'
    ordering = ['-fecha_cambio']
