from django.contrib import admin
from .models import CategoriaMaterial, Material, MovimientoInventario


@admin.register(CategoriaMaterial)
class CategoriaMaterialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'codigo',
        'categoria',
        'stock_actual',
        'stock_minimo',
        'unidad_medida',
        'estado',
        'precio_compra',
        'precio_venta'
    ]
    list_filter = ['estado', 'categoria', 'unidad_medida']
    search_fields = ['nombre', 'codigo', 'descripcion']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'categoria', 'descripcion')
        }),
        ('Stock', {
            'fields': ('stock_actual', 'stock_minimo', 'unidad_medida', 'estado')
        }),
        ('Precios', {
            'fields': ('precio_compra', 'precio_venta')
        }),
        ('Ubicación', {
            'fields': ('ubicacion',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = [
        'material',
        'tipo',
        'cantidad',
        'motivo',
        'fecha'
    ]
    list_filter = ['tipo', 'fecha', 'material__categoria']
    search_fields = ['material__nombre', 'material__codigo', 'motivo', 'notas']
    readonly_fields = ['fecha']
    date_hierarchy = 'fecha'
