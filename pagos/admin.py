from django.contrib import admin
from .models import Pago, PlanPago, TransaccionPago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = [
        'cliente',
        'monto',
        'concepto',
        'periodo_mes',
        'periodo_anio',
        'fecha_vencimiento',
        'estado',
        'fecha_pago'
    ]
    list_filter = ['estado', 'metodo_pago', 'periodo_anio', 'periodo_mes', 'fecha_vencimiento']
    search_fields = ['cliente__nombre', 'cliente__telefono', 'referencia_pago', 'concepto']
    readonly_fields = ['fecha_registro']
    date_hierarchy = 'fecha_vencimiento'
    fieldsets = (
        ('Información del Pago', {
            'fields': ('cliente', 'instalacion', 'concepto', 'monto')
        }),
        ('Período', {
            'fields': ('periodo_mes', 'periodo_anio')
        }),
        ('Fechas', {
            'fields': ('fecha_vencimiento', 'fecha_pago', 'fecha_registro')
        }),
        ('Estado y Método', {
            'fields': ('estado', 'metodo_pago', 'referencia_pago')
        }),
        ('Notas', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )
    actions = ['marcar_como_pagado']
    
    def marcar_como_pagado(self, request, queryset):
        """Acción para marcar pagos como pagados."""
        updated = queryset.update(estado='pagado')
        self.message_user(request, f'{updated} pago(s) marcado(s) como pagado(s).')
    marcar_como_pagado.short_description = 'Marcar como pagado'


@admin.register(PlanPago)
class PlanPagoAdmin(admin.ModelAdmin):
    list_display = ['instalacion', 'monto_mensual', 'dia_vencimiento', 'activo']
    list_filter = ['activo', 'dia_vencimiento']
    search_fields = ['instalacion__cliente__nombre', 'instalacion__numero_contrato']


@admin.register(TransaccionPago)
class TransaccionPagoAdmin(admin.ModelAdmin):
    list_display = [
        'pago',
        'pasarela',
        'estado',
        'monto',
        'moneda',
        'fecha_creacion',
        'fecha_completada',
    ]
    list_filter = ['pasarela', 'estado', 'fecha_creacion']
    search_fields = ['pago__cliente__nombre', 'id_transaccion_pasarela', 'id_pago_intento']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'fecha_completada', 'datos_respuesta']
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información de la Transacción', {
            'fields': ('pago', 'pasarela', 'estado', 'monto', 'moneda')
        }),
        ('IDs de la Pasarela', {
            'fields': ('id_transaccion_pasarela', 'id_pago_intento')
        }),
        ('Información del Método de Pago', {
            'fields': ('metodo_pago_tipo', 'ultimos_digitos')
        }),
        ('Información Adicional', {
            'fields': ('mensaje_error', 'datos_respuesta')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion', 'fecha_completada')
        }),
    )
