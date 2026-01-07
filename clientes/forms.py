from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente


class ClienteForm(forms.ModelForm):
    """Formulario para crear y editar clientes."""
    
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'apellido1',
            'apellido2',
            'email',
            'telefono',
            'direccion',
            'ciudad',
            'estado',
            'codigo_postal',
            'estado_cliente',
            'notas',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'apellido1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primer apellido'
            }),
            'apellido2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Segundo apellido (opcional)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estado'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código postal'
            }),
            'estado_cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notas adicionales sobre el cliente'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos opcionales visualmente
        self.fields['apellido2'].required = False
        self.fields['codigo_postal'].required = False
        self.fields['notas'].required = False
        
        # Email es requerido (necesario para crear usuario del portal)
        self.fields['email'].required = True
        
        # Agregar ayuda para campos únicos
        self.fields['email'].help_text = 'El correo electrónico es requerido y debe ser único. Se usará como usuario para el portal.'
        self.fields['telefono'].help_text = 'El teléfono debe ser único en el sistema.'
    
    def clean_email(self):
        """Valida que el email sea único y requerido."""
        email = self.cleaned_data.get('email')
        
        # Validar que el email esté presente (es requerido)
        if not email or not email.strip():
            raise ValidationError('El correo electrónico es requerido.')
        
        email = email.strip()
        
        # Buscar en todos los registros (incluyendo eliminados) para evitar duplicados
        qs = Cliente.all_objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe un cliente con este correo electrónico.')
        
        return email
    
    def clean_telefono(self):
        """Valida que el teléfono sea único."""
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Buscar en todos los registros (incluyendo eliminados) para evitar duplicados
            qs = Cliente.all_objects.filter(telefono=telefono)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('Ya existe un cliente con este teléfono.')
        return telefono


