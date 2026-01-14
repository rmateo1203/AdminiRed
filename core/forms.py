"""
Formularios para modelos de core.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import ConfiguracionSistema, Rol, Permiso, PermisoRol

User = get_user_model()


class ConfiguracionSistemaForm(forms.ModelForm):
    """Formulario para la configuración del sistema."""
    
    class Meta:
        model = ConfiguracionSistema
        fields = [
            'activa', 'nombre_empresa', 'descripcion_sistema', 'titulo_sistema',
            'logo', 'imagen_hero', 'color_primario', 'color_secundario', 'color_exito',
            'color_advertencia', 'color_peligro', 'color_info'
        ]
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_sistema': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'titulo_sistema': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'imagen_hero': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'color_primario': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'color_secundario': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'color_exito': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'color_advertencia': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'color_peligro': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'color_info': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }


class UsuarioForm(forms.ModelForm):
    """Formulario para crear y editar usuarios del sistema."""
    
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
                'class': 'form-control',
            'placeholder': 'Dejar en blanco para no cambiar'
        }),
        label='Contraseña',
        help_text='Mínimo 8 caracteres. Dejar en blanco si no deseas cambiar la contraseña (al editar).'
    )
    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
                'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        }),
        label='Confirmar contraseña'
    )
    roles = forms.ModelMultipleChoiceField(
        queryset=Rol.objects.filter(activo=True).order_by('nombre'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Roles',
        help_text='Selecciona los roles que tendrá este usuario. Nota: Los roles del sistema (excepto Cliente) activarán automáticamente is_staff.'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        # Si estamos editando, preseleccionar roles actuales
        if self.instance and self.instance.pk:
            from .roles_utils import obtener_roles_usuario
            roles_actuales = obtener_roles_usuario(self.instance)
            self.fields['roles'].initial = [r.id for r in roles_actuales]
            # Hacer password opcional al editar
            self.fields['password'].required = False
        else:
            # Al crear, password es requerido
            self.fields['password'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Solo validar contraseña si se está creando un usuario nuevo o se está cambiando
        if not self.instance.pk:  # Creando nuevo usuario
            if not password:
                raise ValidationError({'password': 'La contraseña es requerida para crear un nuevo usuario.'})
            if password and len(password) < 8:
                raise ValidationError({'password': 'La contraseña debe tener al menos 8 caracteres.'})
        elif password:  # Editando y se proporcionó contraseña
            if len(password) < 8:
                raise ValidationError({'password': 'La contraseña debe tener al menos 8 caracteres.'})
        
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError({'password_confirm': 'Las contraseñas no coinciden.'})
        
        return cleaned_data
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        
        # Establecer contraseña si se proporcionó
        password = self.cleaned_data.get('password')
        if password:
            usuario.set_password(password)
        
        if commit:
            usuario.save()
            
            # Asignar roles
            roles_seleccionados = self.cleaned_data.get('roles', [])
            from .roles_utils import obtener_roles_usuario
            from .models import UsuarioRol
            
            # Obtener roles actuales
            roles_actuales = obtener_roles_usuario(usuario)
            ids_roles_actuales = {r.id for r in roles_actuales}
            ids_roles_seleccionados = {r.id for r in roles_seleccionados}
            
            # Remover roles que ya no están seleccionados
            for rol in roles_actuales:
                if rol.id not in ids_roles_seleccionados:
                    # Usar save() en lugar de update() para que las señales se disparen
                    usuario_rol = UsuarioRol.objects.filter(usuario=usuario, rol=rol).first()
                    if usuario_rol:
                        usuario_rol.activo = False
                        usuario_rol.save()
            
            # Agregar nuevos roles
            for rol in roles_seleccionados:
                if rol.id not in ids_roles_actuales:
                    # Crear nuevo UsuarioRol - las señales se dispararán automáticamente
                    UsuarioRol.objects.get_or_create(
                        usuario=usuario,
                        rol=rol,
                        defaults={
                            'activo': True, 
                            'asignado_por': self.request_user if self.request_user else None
                        }
                    )
                else:
                    # Reactivar si estaba inactivo - usar save() para que las señales se disparen
                    usuario_rol = UsuarioRol.objects.filter(usuario=usuario, rol=rol).first()
                    if usuario_rol and not usuario_rol.activo:
                        usuario_rol.activo = True
                        if not usuario_rol.asignado_por and self.request_user:
                            usuario_rol.asignado_por = self.request_user
                        usuario_rol.save()
        
        return usuario


class RolForm(forms.ModelForm):
    """Formulario para crear/editar roles."""
    
    class Meta:
        model = Rol
        fields = ['nombre', 'codigo', 'descripcion', 'activo', 'es_sistema']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: administrador, supervisor'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'es_sistema': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'codigo': 'Código único para referencia programática (solo letras, números y guiones bajos)',
            'es_sistema': 'Los roles del sistema no pueden ser eliminados',
        }
    
    def clean_codigo(self):
        """Validar que el código tenga el formato correcto."""
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            import re
            if not re.match(r'^[a-zA-Z0-9_]+$', codigo):
                raise forms.ValidationError('El código solo puede contener letras, números y guiones bajos.')
        return codigo


class RolPermisosForm(forms.ModelForm):
    """Formulario para gestionar permisos de un rol."""
    
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.filter(activo=True).order_by('categoria', 'nombre'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        help_text='Selecciona los permisos que tendrá este rol'
    )
    
    class Meta:
        model = Rol
        fields = ['permisos']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Preseleccionar permisos actuales del rol
            self.fields['permisos'].initial = self.instance.permisos.all()
    
    def save(self, commit=True):
        """Guardar el rol y actualizar sus permisos."""
        rol = super().save(commit=False)
        
        if commit:
            rol.save()
            
            # Actualizar permisos
            permisos_seleccionados = self.cleaned_data.get('permisos', [])
            permisos_actuales = set(rol.permisos.all())
            
            # Remover permisos que ya no están seleccionados
            for permiso in permisos_actuales:
                if permiso not in permisos_seleccionados:
                    PermisoRol.objects.filter(rol=rol, permiso=permiso).delete()
            
            # Agregar nuevos permisos
            for permiso in permisos_seleccionados:
                if permiso not in permisos_actuales:
                    PermisoRol.objects.get_or_create(rol=rol, permiso=permiso)
        
        return rol


class PermisoForm(forms.ModelForm):
    """Formulario para crear/editar permisos."""
    
    class Meta:
        model = Permiso
        fields = ['nombre', 'codigo', 'descripcion', 'categoria', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: ver_clientes, editar_pagos'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: clientes, pagos, sistema'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_codigo(self):
        """Validar que el código tenga el formato correcto."""
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            import re
            if not re.match(r'^[a-zA-Z0-9_]+$', codigo):
                raise forms.ValidationError('El código solo puede contener letras, números y guiones bajos.')
        return codigo
