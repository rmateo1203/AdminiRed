from django.contrib import admin
from .models import TipoNotificacion, Notificacion, ConfiguracionNotificacion


@admin.register(TipoNotificacion)
class TipoNotificacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'descripcion']
    search_fields = ['nombre', 'codigo']


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = [
        'asunto',
        'cliente',
        'tipo',
        'canal',
        'estado',
        'fecha_creacion',
        'fecha_envio',
        'intentos'
    ]
    list_filter = ['estado', 'canal', 'tipo', 'fecha_creacion', 'fecha_envio']
    search_fields = ['asunto', 'cliente__nombre', 'cliente__telefono', 'mensaje']
    readonly_fields = ['fecha_creacion', 'intentos']
    date_hierarchy = 'fecha_creacion'
    fieldsets = (
        ('Destinatario', {
            'fields': ('cliente', 'pago', 'tipo')
        }),
        ('Contenido', {
            'fields': ('asunto', 'mensaje', 'canal')
        }),
        ('Programación', {
            'fields': ('fecha_programada',)
        }),
        ('Estado y Resultado', {
            'fields': ('estado', 'fecha_envio', 'intentos', 'resultado')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConfiguracionNotificacion)
class ConfiguracionNotificacionAdmin(admin.ModelAdmin):
    list_display = [
        'tipo_notificacion',
        'activa',
        'dias_antes_vencimiento',
        'dias_despues_vencimiento',
        'canal_preferido'
    ]
    list_filter = ['activa', 'canal_preferido']
