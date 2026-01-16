from django.db import models
from django.core.cache import cache
from django.core.validators import RegexValidator


class ConfiguracionSistema(models.Model):
    """Configuración general del sistema: colores, logo, nombre de empresa."""
    
    activa = models.BooleanField(default=True, verbose_name='Configuración activa')
    
    # Información de la empresa
    nombre_empresa = models.CharField(
        max_length=100,
        default='AdminiRed',
        verbose_name='Nombre de la empresa',
        help_text='Nombre que aparecerá en el header y footer'
    )
    
    # Logo
    logo = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Logo de la empresa',
        help_text='Imagen del logo (recomendado: PNG transparente, máximo 200x60px)'
    )
    
    # Colores principales
    color_primario = models.CharField(
        max_length=7,
        default='#667eea',
        validators=[RegexValidator(regex=r'^#[0-9A-Fa-f]{6}$', message='Formato de color inválido. Use formato hexadecimal (#RRGGBB)')],
        verbose_name='Color primario',
        help_text='Color principal del sistema (header, botones principales)'
    )
    
    color_secundario = models.CharField(
        max_length=7,
        default='#764ba2',
        validators=[RegexValidator(regex=r'^#[0-9A-Fa-f]{6}$', message='Formato de color inválido. Use formato hexadecimal (#RRGGBB)')],
        verbose_name='Color secundario',
        help_text='Color secundario (gradientes, acentos)'
    )
    
    color_exito = models.CharField(
        max_length=7,
        default='#10b981',
        validators=[RegexValidator(regex=r'^#[0-9A-Fa-f]{6}$', message='Formato de color inválido. Use formato hexadecimal (#RRGGBB)')],
        verbose_name='Color de éxito',
        help_text='Color para acciones exitosas, badges de éxito'
    )
    
    color_advertencia = models.CharField(
        max_length=7,
        default='#f59e0b',
        validators=[RegexValidator(regex=r'^#[0-9A-Fa-f]{6}$', message='Formato de color inválido. Use formato hexadecimal (#RRGGBB)')],
        verbose_name='Color de advertencia',
        help_text='Color para advertencias, badges de advertencia'
    )
    
    color_peligro = models.CharField(
        max_length=7,
        default='#ef4444',
        validators=[RegexValidator(regex=r'^#[0-9A-Fa-f]{6}$', message='Formato de color inválido. Use formato hexadecimal (#RRGGBB)')],
        verbose_name='Color de peligro',
        help_text='Color para errores, badges de peligro'
    )
    
    color_info = models.CharField(
        max_length=7,
        default='#3b82f6',
        validators=[RegexValidator(regex=r'^#[0-9A-Fa-f]{6}$', message='Formato de color inválido. Use formato hexadecimal (#RRGGBB)')],
        verbose_name='Color de información',
        help_text='Color para información, badges de info'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Configuración del Sistema'
        verbose_name_plural = 'Configuraciones del Sistema'
    
    def __str__(self):
        return f"Configuración: {self.nombre_empresa}"
    
    def save(self, *args, **kwargs):
        # Solo permitir una configuración activa
        if self.activa:
            ConfiguracionSistema.objects.exclude(pk=self.pk).update(activa=False)
        # Limpiar caché al guardar
        cache.delete('config_sistema')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_activa(cls):
        """Obtiene la configuración activa, usando caché."""
        config = cache.get('config_sistema')
        if config is None:
            config = cls.objects.filter(activa=True).first()
            if config is None:
                # Crear configuración por defecto si no existe
                config = cls.objects.create(
                    activa=True,
                    nombre_empresa='AdminiRed',
                    color_primario='#667eea',
                    color_secundario='#764ba2',
                    color_exito='#10b981',
                    color_advertencia='#f59e0b',
                    color_peligro='#ef4444',
                    color_info='#3b82f6'
                )
            cache.set('config_sistema', config, 3600)  # Cache por 1 hora
        return config
