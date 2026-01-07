from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
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
            'cliente': forms.HiddenInput(),  # Campo oculto, se maneja con el buscador
            'instalacion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'placeholder': '0.00',
                'style': 'padding-left: 1.75rem;'
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
        elif self.instance and self.instance.pk and self.instance.cliente:
            # Modo edición: cargar instalaciones del cliente actual
            self.fields['instalacion'].queryset = Instalacion.objects.filter(cliente=self.instance.cliente)
        else:
            self.fields['instalacion'].queryset = Instalacion.objects.all()
        
        # Hacer campos opcionales
        self.fields['instalacion'].required = False
        self.fields['fecha_pago'].required = False
        self.fields['metodo_pago'].required = False
        self.fields['referencia_pago'].required = False
        self.fields['notas'].required = False
        
        # Si el estado es 'pagado', hacer fecha_pago requerida
        if self.instance and self.instance.pk and self.instance.estado == 'pagado':
            self.fields['fecha_pago'].required = True
        
        # Establecer valor máximo para fecha_pago (hasta 1 hora en el futuro para ajustes de zona horaria)
        if 'fecha_pago' in self.fields:
            ahora = timezone.now()
            max_datetime = ahora + timedelta(hours=1)
            self.fields['fecha_pago'].widget.attrs['max'] = max_datetime.strftime('%Y-%m-%dT%H:%M')
    
    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        instalacion = cleaned_data.get('instalacion')
        periodo_mes = cleaned_data.get('periodo_mes')
        periodo_anio = cleaned_data.get('periodo_anio')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')
        fecha_pago = cleaned_data.get('fecha_pago')
        estado = cleaned_data.get('estado')
        monto = cleaned_data.get('monto')
        
        # Validación crítica: Instalación debe pertenecer al cliente
        if instalacion and cliente:
            if instalacion.cliente != cliente:
                raise ValidationError({
                    'instalacion': 'La instalación seleccionada no pertenece al cliente seleccionado.'
                })
        
        # Validación de monto razonable
        if monto is not None:
            if monto <= 0:
                raise ValidationError({
                    'monto': 'El monto debe ser mayor a cero.'
                })
            if monto > 1000000:  # Límite máximo de $1,000,000
                raise ValidationError({
                    'monto': 'El monto no puede ser mayor a $1,000,000. Por favor, verifique el valor.'
                })
            if monto < 0.01:  # Mínimo $0.01
                raise ValidationError({
                    'monto': 'El monto debe ser al menos $0.01.'
                })
        
        # Validación de períodos duplicados (excluyendo cancelados)
        if cliente and periodo_mes and periodo_anio:
            existing = Pago.objects.filter(
                cliente=cliente,
                periodo_mes=periodo_mes,
                periodo_anio=periodo_anio
            ).exclude(estado='cancelado')  # Excluir pagos cancelados
            
            # Si hay instalación, también validar por instalación
            if instalacion:
                existing = existing.filter(instalacion=instalacion)
            else:
                # Si no hay instalación, validar que no haya otro sin instalación
                existing = existing.filter(instalacion__isnull=True)
            
            # Excluir el pago actual si estamos editando
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                pago_duplicado = existing.first()
                mensaje = f'Ya existe un pago activo para este cliente'
                if instalacion:
                    mensaje += f' e instalación ({instalacion.numero_contrato})'
                mensaje += f' en el período {dict(Pago.PERIODO_MES_CHOICES).get(periodo_mes, periodo_mes)} {periodo_anio}.'
                if pago_duplicado:
                    mensaje += f' Pago existente: {pago_duplicado.concepto} (${pago_duplicado.monto}) - Estado: {pago_duplicado.get_estado_display()}'
                
                raise ValidationError({
                    'periodo_mes': mensaje,
                    'periodo_anio': mensaje,
                })
        
        # Validación de fechas
        if fecha_vencimiento:
            # Validar que fecha_vencimiento no sea muy antigua (más de 10 años)
            if fecha_vencimiento < (date.today() - timedelta(days=3650)):
                raise ValidationError({
                    'fecha_vencimiento': 'La fecha de vencimiento no puede ser anterior a hace 10 años.'
                })
            
            # Validar que fecha_vencimiento no sea muy futura (más de 5 años)
            if fecha_vencimiento > (date.today() + timedelta(days=1825)):
                raise ValidationError({
                    'fecha_vencimiento': 'La fecha de vencimiento no puede ser posterior a 5 años.'
                })
        
        # Validar que fecha_pago >= fecha_vencimiento
        if fecha_pago and fecha_vencimiento:
            if fecha_pago.date() < fecha_vencimiento:
                raise ValidationError({
                    'fecha_pago': 'La fecha de pago no puede ser anterior a la fecha de vencimiento.'
                })
        
        # Validar que fecha_pago no sea futura
        # Permitir hasta el final del día actual (considerando la hora)
        if fecha_pago:
            ahora = timezone.now()
            # Permitir hasta 1 hora en el futuro para ajustes de zona horaria
            if fecha_pago > (ahora + timedelta(hours=1)):
                raise ValidationError({
                    'fecha_pago': f'La fecha de pago no puede ser futura. La fecha/hora actual es {ahora.strftime("%d/%m/%Y %H:%M")}.'
                })
        
        # Validación de estado
        if estado == 'pagado':
            if not fecha_pago:
                raise ValidationError({
                    'fecha_pago': 'La fecha de pago es requerida cuando el estado es "Pagado".'
                })
        
        return cleaned_data


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



