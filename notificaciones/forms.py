from django import forms
from .models import Notificacion
from clientes.models import Cliente
from pagos.models import Pago
from .models import TipoNotificacion


class NotificacionForm(forms.ModelForm):
    """Formulario para crear y editar notificaciones."""
    
    class Meta:
        model = Notificacion
        fields = [
            'cliente',
            'pago',
            'tipo',
            'asunto',
            'mensaje',
            'canal',
            'estado',
            'fecha_programada',
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'pago': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'asunto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Asunto de la notificación'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Mensaje de la notificación'
            }),
            'canal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_programada': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super().__init__(*args, **kwargs)
        
        # Ordenar clientes por nombre completo
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre', 'apellido1')
        
        # Hacer campos opcionales
        self.fields['cliente'].required = False
        self.fields['pago'].required = False
        self.fields['tipo'].required = False
        self.fields['fecha_programada'].required = False
        
        # Pre-seleccionar cliente si se proporciona
        if cliente_id:
            try:
                cliente = Cliente.objects.get(pk=cliente_id)
                self.fields['cliente'].initial = cliente
                self.fields['cliente'].widget.attrs['disabled'] = True
            except Cliente.DoesNotExist:
                pass

