from django import forms
from .models import Pago, PlanPago
from clientes.models import Cliente
from instalaciones.models import Instalacion


class PagoForm(forms.ModelForm):
    """Formulario para crear y editar pagos."""
    
    class Meta:
        model = Pago
        fields = [
            'cliente',
            'instalacion',
            'monto',
            'concepto',
            'periodo_mes',
            'periodo_anio',
            'fecha_vencimiento',
            'fecha_pago',
            'estado',
            'metodo_pago',
            'referencia_pago',
            'notas',
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'instalacion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'placeholder': '0.00'
            }),
            'concepto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pago mensual de servicio'
            }),
            'periodo_mes': forms.Select(attrs={
                'class': 'form-control'
            }),
            'periodo_anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2000,
                'max': 2100,
                'placeholder': '2024'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_pago': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-control'
            }),
            'referencia_pago': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de transacción, referencia bancaria, etc.'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super().__init__(*args, **kwargs)
        
        # Ordenar clientes por nombre
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre', 'apellido1')
        
        # Configurar instalaciones basadas en el cliente seleccionado
        if cliente_id:
            self.fields['cliente'].initial = cliente_id
            self.fields['instalacion'].queryset = Instalacion.objects.filter(cliente_id=cliente_id)
        else:
            self.fields['instalacion'].queryset = Instalacion.objects.none()
        
        # Hacer campos opcionales
        self.fields['instalacion'].required = False
        self.fields['fecha_pago'].required = False
        self.fields['metodo_pago'].required = False
        self.fields['referencia_pago'].required = False
        self.fields['notas'].required = False


class PlanPagoForm(forms.ModelForm):
    """Formulario para crear y editar planes de pago."""
    
    class Meta:
        model = PlanPago
        fields = [
            'instalacion',
            'monto_mensual',
            'dia_vencimiento',
            'activo',
        ]
        widgets = {
            'instalacion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'monto_mensual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'placeholder': '0.00'
            }),
            'dia_vencimiento': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 31,
                'placeholder': '1-31'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instalacion'].queryset = Instalacion.objects.filter(
            estado='activa'
        ).order_by('cliente__nombre', 'cliente__apellido1')

