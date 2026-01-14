from django.db import models
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


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
    
    descripcion_sistema = models.CharField(
        max_length=200,
        default='Sistema para el control total de instalaciones de internet',
        blank=True,
        verbose_name='Descripción del sistema',
        help_text='Descripción corta que aparecerá como subtítulo en el home y footer'
    )
    
    titulo_sistema = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Título del sistema (opcional)',
        help_text='Título del sistema. Si está vacío, se usará el nombre de la empresa'
    )
    
    # Logo
    logo = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Logo de la empresa',
        help_text='Imagen del logo (recomendado: PNG transparente, máximo 200x60px)'
    )
    
    # Imagen Hero
    imagen_hero = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Imagen del Hero (Página de Inicio)',
        help_text='Imagen de fondo para la sección hero en la página de inicio (recomendado: 1920x400px o similar)'
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
    
    @property
    def titulo_para_mostrar(self):
        """Retorna el título del sistema o el nombre de la empresa si el título está vacío."""
        return self.titulo_sistema if self.titulo_sistema else self.nombre_empresa
    
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
                    descripcion_sistema='Sistema para el control total de instalaciones de internet',
                    titulo_sistema=None,
                    color_primario='#667eea',
                    color_secundario='#764ba2',
                    color_exito='#10b981',
                    color_advertencia='#f59e0b',
                    color_peligro='#ef4444',
                    color_info='#3b82f6'
                )
            cache.set('config_sistema', config, 3600)  # Cache por 1 hora
        return config


# =============================================================================
# SISTEMA DE ROLES Y PERMISOS
# =============================================================================



class Rol(models.Model):
    """
    Modelo para definir roles del sistema (Administrador, Supervisor, Instalador, etc.).
    Los roles son configurables desde el admin.
    """
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del rol',
        help_text='Nombre único del rol (ej: Administrador, Supervisor, Instalador)'
    )
    
    codigo = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Código del rol',
        help_text='Código único para referencia programática (ej: admin, supervisor, instalador). Solo letras, números y guiones bajos.'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción del rol y sus responsabilidades'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el rol está activo y puede ser asignado a usuarios'
    )
    
    es_sistema = models.BooleanField(
        default=False,
        verbose_name='Es rol de sistema',
        help_text='Si está marcado, es un rol especial del sistema y no puede ser eliminado'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    # Relación Many-to-Many con Permiso
    permisos = models.ManyToManyField(
        'Permiso',
        through='PermisoRol',
        related_name='roles',
        blank=True,
        verbose_name='Permisos'
    )
    
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['codigo', 'activo']),
            models.Index(fields=['activo']),
        ]
    
    def __str__(self):
        return self.nombre
    
    def clean(self):
        """Validación: el código solo puede contener letras, números y guiones bajos."""
        if self.codigo:
            import re
            if not re.match(r'^[a-zA-Z0-9_]+$', self.codigo):
                raise ValidationError({
                    'codigo': 'El código solo puede contener letras, números y guiones bajos.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def tiene_permiso(self, codigo_permiso):
        """Verifica si el rol tiene un permiso específico."""
        return self.permisos.filter(codigo=codigo_permiso, activo=True).exists()


class Permiso(models.Model):
    """
    Modelo para definir permisos específicos del sistema.
    Los permisos son configurables desde el admin.
    """
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del permiso',
        help_text='Nombre descriptivo del permiso (ej: Ver clientes, Editar pagos)'
    )
    
    codigo = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Código del permiso',
        help_text='Código único para referencia programática (ej: ver_clientes, editar_pagos). Solo letras, números y guiones bajos.'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del permiso'
    )
    
    categoria = models.CharField(
        max_length=50,
        verbose_name='Categoría',
        help_text='Categoría del permiso para agruparlos (ej: clientes, pagos, instalaciones)',
        db_index=True
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el permiso está activo'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        ordering = ['categoria', 'nombre']
        indexes = [
            models.Index(fields=['codigo', 'activo']),
            models.Index(fields=['categoria', 'activo']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria})"
    
    def clean(self):
        """Validación: el código solo puede contener letras, números y guiones bajos."""
        if self.codigo:
            import re
            if not re.match(r'^[a-zA-Z0-9_]+$', self.codigo):
                raise ValidationError({
                    'codigo': 'El código solo puede contener letras, números y guiones bajos.'
                })


class PermisoRol(models.Model):
    """
    Modelo intermedio para la relación Many-to-Many entre Rol y Permiso.
    Permite agregar información adicional a la relación.
    """
    
    rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        related_name='permiso_roles',
        verbose_name='Rol'
    )
    
    permiso = models.ForeignKey(
        Permiso,
        on_delete=models.CASCADE,
        related_name='permiso_roles',
        verbose_name='Permiso'
    )
    
    fecha_asignacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    
    class Meta:
        verbose_name = 'Permiso de Rol'
        verbose_name_plural = 'Permisos de Roles'
        unique_together = [['rol', 'permiso']]
        ordering = ['rol', 'permiso']
    
    def __str__(self):
        return f"{self.rol.nombre} - {self.permiso.nombre}"


class PerfilUsuario(models.Model):
    """
    Perfil extendido para usuarios del sistema.
    Almacena información adicional que no está en el modelo User de Django.
    """
    
    TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('instalador', 'Instalador'),
        ('tecnico', 'Técnico'),
        ('otro', 'Otro'),
    ]
    
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuario'
    )
    
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='otro',
        verbose_name='Tipo de usuario',
        help_text='Tipo general de usuario (puede ser más específico con roles)'
    )
    
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Teléfono',
        help_text='Teléfono de contacto'
    )
    
    foto = models.ImageField(
        upload_to='perfiles/',
        blank=True,
        null=True,
        verbose_name='Foto de perfil',
        help_text='Foto de perfil del usuario'
    )
    
    fecha_nacimiento = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de nacimiento'
    )
    
    direccion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dirección'
    )
    
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas',
        help_text='Notas adicionales sobre el usuario'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
        ordering = ['usuario__username']
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario."""
        if self.usuario.first_name or self.usuario.last_name:
            return f"{self.usuario.first_name} {self.usuario.last_name}".strip()
        return self.usuario.username


class UsuarioRol(models.Model):
    """
    Modelo intermedio para la relación Many-to-Many entre Usuario y Rol.
    Permite que un usuario tenga múltiples roles y rastrear cuándo se asignaron.
    """
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='usuario_roles',
        verbose_name='Usuario'
    )
    
    rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        related_name='usuario_roles',
        verbose_name='Rol'
    )
    
    asignado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='roles_asignados',
        verbose_name='Asignado por'
    )
    
    fecha_asignacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el rol está activo para este usuario'
    )
    
    class Meta:
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuario'
        unique_together = [['usuario', 'rol']]
        ordering = ['usuario', 'rol']
        indexes = [
            models.Index(fields=['usuario', 'activo']),
        ]
    
    def __str__(self):
        return f"{self.usuario.username} - {self.rol.nombre}"
