from django import forms
from .models import ConfiguracionSistema


class ConfiguracionSistemaForm(forms.ModelForm):
    """Formulario para configurar el sistema (logo, colores, nombre)."""
    
    class Meta:
        model = ConfiguracionSistema
        fields = [
            'activa',
            'nombre_empresa',
            'logo',
            'pagos_online_habilitados',
            'color_primario',
            'color_secundario',
            'color_exito',
            'color_advertencia',
            'color_peligro',
            'color_info',
        ]
        widgets = {
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'pagos_online_habilitados': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'nombre_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de tu empresa'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'color_primario': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'style': 'width: 100px; height: 40px;'
            }),
            'color_secundario': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'style': 'width: 100px; height: 40px;'
            }),
            'color_exito': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'style': 'width: 100px; height: 40px;'
            }),
            'color_advertencia': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'style': 'width: 100px; height: 40px;'
            }),
            'color_peligro': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'style': 'width: 100px; height: 40px;'
            }),
            'color_info': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'style': 'width: 100px; height: 40px;'
            }),
        }
    
    def clean_color_primario(self):
        """Valida el formato del color primario."""
        color = self.cleaned_data.get('color_primario')
        if color and not color.startswith('#'):
            color = '#' + color
        return color
    
    def clean_color_secundario(self):
        """Valida el formato del color secundario."""
        color = self.cleaned_data.get('color_secundario')
        if color and not color.startswith('#'):
            color = '#' + color
        return color


