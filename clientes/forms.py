from django import forms
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
                'placeholder': 'correo@ejemplo.com'
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
        self.fields['email'].required = False
        self.fields['codigo_postal'].required = False
        self.fields['notas'].required = False


