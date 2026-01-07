from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

User = get_user_model()


class ClienteManager(models.Manager):
    """Manager personalizado para filtrar clientes activos por defecto."""
    
    def get_queryset(self):
        """Retorna solo clientes no eliminados (soft delete)."""
        return super().get_queryset().filter(is_deleted=False)
    
    def all_with_deleted(self):
        """Retorna todos los clientes incluyendo eliminados."""
        return super().get_queryset()
    
    def deleted_only(self):
        """Retorna solo clientes eliminados."""
        return super().get_queryset().filter(is_deleted=True)


class Cliente(models.Model):
    """Modelo para gestionar información de clientes."""
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Información básica
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido1 = models.CharField(max_length=50, verbose_name='Primer apellido')
    apellido2 = models.CharField(max_length=50, verbose_name='Segundo apellido', blank=True, null=True)
    email = models.EmailField(
        verbose_name='Correo electrónico',
        blank=True,
        null=True,
        help_text='El correo electrónico debe ser único (si se proporciona)'
    )
    telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Formato de teléfono inválido')],
        verbose_name='Teléfono',
        help_text='El teléfono debe ser único'
    )
    
    # Dirección
    direccion = models.TextField(verbose_name='Dirección')
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    estado = models.CharField(max_length=100, verbose_name='Estado')
    codigo_postal = models.CharField(max_length=10, verbose_name='Código postal', blank=True, null=True)
    
    # Estado del cliente
    estado_cliente = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activo',
        verbose_name='Estado del cliente'
    )
    
    # Información adicional
    notas = models.TextField(blank=True, null=True, verbose_name='Notas adicionales')
    
    # Soft delete
    is_deleted = models.BooleanField(default=False, verbose_name='Eliminado')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de eliminación')
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes_creados',
        verbose_name='Creado por'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes_actualizados',
        verbose_name='Actualizado por'
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes_eliminados',
        verbose_name='Eliminado por'
    )
    
    # Usuario del sistema (para acceso al portal)
    usuario = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cliente_perfil',
        verbose_name='Usuario del sistema',
        help_text='Usuario que puede acceder al portal de cliente'
    )
    
    # Historial
    history = HistoricalRecords()
    
    # Managers
    objects = ClienteManager()
    all_objects = models.Manager()  # Manager sin filtros
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellido1', 'apellido2', 'nombre']
        indexes = [
            models.Index(fields=['email', 'is_deleted']),
            models.Index(fields=['telefono', 'is_deleted']),
            models.Index(fields=['estado_cliente']),
            models.Index(fields=['is_deleted']),
        ]
        constraints = [
            # Permitir email duplicado solo si está eliminado
            models.UniqueConstraint(
                fields=['email'],
                condition=models.Q(is_deleted=False, email__isnull=False),
                name='unique_email_when_not_deleted'
            ),
            # Permitir teléfono duplicado solo si está eliminado
            models.UniqueConstraint(
                fields=['telefono'],
                condition=models.Q(is_deleted=False, telefono__isnull=False),
                name='unique_telefono_when_not_deleted'
            ),
        ]
    
    def __str__(self):
        return self.nombre_completo
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del cliente."""
        partes = [self.nombre, self.apellido1]
        if self.apellido2:
            partes.append(self.apellido2)
        return ' '.join(partes)
    
    @property
    def tiene_acceso_portal(self):
        """Verifica si el cliente tiene usuario para acceder al portal."""
        return self.usuario is not None and self.usuario.is_active
    
    def crear_usuario_portal(self, password=None, enviar_email=True):
        """
        Crea un usuario para que el cliente acceda al portal.
        
        Args:
            password: Contraseña personalizada (opcional). Si no se proporciona, se genera automáticamente.
            enviar_email: Si es True y el cliente tiene email, se envía un email con las credenciales.
        
        Returns:
            User: El usuario creado o existente.
        """
        from django.contrib.auth import get_user_model
        from django.core.mail import send_mail
        from django.conf import settings
        import secrets
        import string
        
        User = get_user_model()
        
        # Si ya tiene usuario, no crear otro
        if self.usuario:
            return self.usuario
        
        # Validar que el cliente tenga email (requerido para crear usuario)
        if not self.email:
            raise ValueError(
                'El cliente debe tener un correo electrónico para crear un usuario del portal. '
                'Por favor, actualiza el email del cliente primero.'
            )
        
        # Usar email como username
        username = self.email
        
        # Verificar que el username no exista
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        
        # Generar contraseña si no se proporciona
        password_generada = False
        if not password:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(12))
            password_generada = True
        
        # Crear usuario
        usuario = User.objects.create_user(
            username=username,
            email=self.email,
            password=password,
            is_staff=False,  # No es staff (no accede al admin)
            is_superuser=False  # No es superusuario
        )
        
        self.usuario = usuario
        self.save()
        
        # Enviar email con credenciales si está habilitado y el cliente tiene email
        if enviar_email and self.email:
            try:
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                
                # Obtener URL del portal desde settings o usar default
                portal_url = getattr(settings, 'SITE_URL', 'http://localhost:8000') + '/clientes/portal/login/'
                
                # Preparar mensaje
                subject = f'Credenciales de acceso - Portal de Clientes {getattr(settings, "SISTEMA_NOMBRE", "AdminiRed")}'
                
                mensaje_texto = f"""
Hola {self.nombre_completo},

Se ha creado tu cuenta de acceso al portal de clientes.

Tus credenciales de acceso son:
- Usuario: {usuario.username}
- Contraseña: {password}

Puedes acceder al portal en: {portal_url}

Por seguridad, te recomendamos cambiar tu contraseña después del primer acceso.

Si no solicitaste esta cuenta, por favor contacta con nosotros.

Saludos,
Equipo de {getattr(settings, "SISTEMA_NOMBRE", "AdminiRed")}
"""
                
                # Intentar enviar email
                send_mail(
                    subject=subject,
                    message=mensaje_texto,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@adminired.com'),
                    recipient_list=[self.email],
                    fail_silently=False,  # Lanzar excepción si falla
                )
            except Exception as e:
                # Si falla el envío de email, registrar el error pero no fallar la creación del usuario
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Error al enviar email de credenciales a {self.email}: {str(e)}')
                # Si la contraseña fue generada y no se pudo enviar el email, 
                # esto es un problema porque el cliente no sabrá su contraseña
                if password_generada:
                    raise ValueError(
                        f'Se creó el usuario pero no se pudo enviar el email con las credenciales. '
                        f'Por favor, comunica manualmente al cliente: Usuario: {usuario.username}, Contraseña: {password}'
                    )
        
        return usuario
    
    def save(self, *args, **kwargs):
        """Guarda el cliente con auditoría."""
        user = kwargs.pop('user', None)
        
        # Auditoría para creación
        if not self.pk and user:
            self.created_by = user
        
        # Auditoría para actualización
        if self.pk and user:
            self.updated_by = user
        
        super().save(*args, **kwargs)
    
    def soft_delete(self, user=None):
        """Eliminación suave del cliente."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save(user=user)
    
    def restore(self, user=None):
        """Restaura un cliente eliminado."""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        if user:
            self.updated_by = user
        self.save(user=user)
