from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from .models import Pago, PlanPago
from clientes.models import Cliente
from instalaciones.models import Instalacion


class DateInput(forms.DateInput):
    """Widget personalizado para campos de fecha que asegura el formato correcto para HTML5 date input."""
    input_type = 'date'
    
    def format_value(self, value):
        """Formatea el valor de fecha en formato YYYY-MM-DD para el input type='date'."""
        if value is None:
            return ''
        if isinstance(value, str):
            return value
        # Si es un objeto date o datetime, formatearlo como YYYY-MM-DD
        if hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d')
        return value


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
            'fecha_vencimiento': DateInput(attrs={
                'class': 'form-control'
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
            self.fields['cliente'].initial = self.instance.cliente.pk
            self.fields['instalacion'].queryset = Instalacion.objects.filter(cliente=self.instance.cliente)
            # Asegurar que la instalación actual esté en el queryset si existe
            if self.instance.instalacion:
                # Agregar la instalación actual si no está en el queryset (por ejemplo, si fue eliminada)
                if not self.fields['instalacion'].queryset.filter(pk=self.instance.instalacion.pk).exists():
                    # Crear un queryset que incluya la instalación actual
                    from django.db.models import Q
                    self.fields['instalacion'].queryset = Instalacion.objects.filter(
                        Q(cliente=self.instance.cliente) | Q(pk=self.instance.instalacion.pk)
                    )
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
            
            # Si estamos editando y hay una fecha_pago, formatearla correctamente para datetime-local
            if self.instance and self.instance.pk and self.instance.fecha_pago:
                # Convertir a formato datetime-local (YYYY-MM-DDTHH:MM)
                fecha_pago_str = self.instance.fecha_pago.strftime('%Y-%m-%dT%H:%M')
                self.fields['fecha_pago'].widget.attrs['value'] = fecha_pago_str
    
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
                mensaje = "Ya existe un pago activo para este cliente"
                if instalacion:
                    mensaje += " e instalacion ({})".format(instalacion.numero_contrato)
                mensaje += " en el periodo {} {}.".format(
                    dict(Pago.PERIODO_MES_CHOICES).get(periodo_mes, periodo_mes),
                    periodo_anio
                )
                if pago_duplicado:
                    mensaje += " Pago existente: {} (${}) - Estado: {}".format(
                        pago_duplicado.concepto,
                        pago_duplicado.monto,
                        pago_duplicado.get_estado_display()
                    )
                
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
                    'fecha_pago': 'La fecha de pago no puede ser futura. La fecha/hora actual es {}.'.format(ahora.strftime("%d/%m/%Y %H:%M"))
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
        # Si estamos editando, permitir la instalación actual aunque tenga plan
        if self.instance and self.instance.pk:
            # Al editar, permitir la instalación actual
            self.fields['instalacion'].queryset = Instalacion.objects.filter(
                estado='activa'
            ).order_by('cliente__nombre', 'cliente__apellido1')
        else:
            # Al crear, excluir instalaciones que ya tienen plan
            self.fields['instalacion'].queryset = Instalacion.objects.filter(
                estado='activa'
            ).exclude(plan_pago__isnull=False).order_by('cliente__nombre', 'cliente__apellido1')


class PagoMarcarPagadoForm(forms.Form):
    """Formulario para marcar un pago como pagado con todos los datos del pago manual."""
    
    metodo_pago = forms.ChoiceField(
        choices=Pago.METODO_PAGO_CHOICES,
        required=True,
        label='Método de Pago',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    referencia_pago = forms.CharField(
        max_length=100,
        required=False,
        label='Referencia de Pago',
        help_text='Número de transacción, referencia bancaria, folio, etc.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: TRANS-123456, Folio 789, etc.'
        })
    )
    fecha_pago = forms.DateTimeField(
        required=True,
        label='Fecha y Hora de Pago',
        help_text='Fecha y hora en que se realizó el pago',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'required': True
        })
    )
    notas = forms.CharField(
        required=False,
        label='Notas Adicionales',
        help_text='Información adicional sobre el pago (opcional)',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas sobre el pago manual...'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fecha y hora actual como valor por defecto
        if not self.is_bound:
            self.fields['fecha_pago'].initial = timezone.now()
            # Formatear para datetime-local
            if self.fields['fecha_pago'].initial:
                dt = self.fields['fecha_pago'].initial
                if isinstance(dt, timezone.datetime):
                    self.fields['fecha_pago'].initial = dt.strftime('%Y-%m-%dT%H:%M')


class PagoManualForm(forms.ModelForm):
    """Formulario para registrar pagos manuales (depósitos/comprobantes)."""
    
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
            'metodo_pago',
            'referencia_pago',
            'notas',
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'instalacion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0.01,
                'placeholder': '0.00',
                'required': True
            }),
            'concepto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pago mensual de servicio - Depósito en tienda',
                'required': True
            }),
            'periodo_mes': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'periodo_anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2000,
                'max': 2100,
                'placeholder': '2024',
                'required': True
            }),
            'fecha_vencimiento': DateInput(attrs={
                'class': 'form-control',
                'required': True
            }),
            'fecha_pago': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'referencia_pago': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de comprobante, referencia de depósito, etc.',
                'required': True
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales sobre el pago (ej: nombre de la tienda donde se realizó el depósito)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super().__init__(*args, **kwargs)
        
        # Ordenar clientes por nombre
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre', 'apellido1')
        
        # Establecer valores por defecto para pago manual
        self.fields['estado'] = forms.CharField(
            initial='pagado',
            widget=forms.HiddenInput()
        )
        
        # Configurar instalaciones basadas en el cliente
        if cliente_id:
            self.fields['cliente'].initial = cliente_id
            self.fields['instalacion'].queryset = Instalacion.objects.filter(cliente_id=cliente_id)
        elif self.instance and self.instance.pk and self.instance.cliente:
            self.fields['instalacion'].queryset = Instalacion.objects.filter(cliente=self.instance.cliente)
        else:
            self.fields['instalacion'].queryset = Instalacion.objects.none()
        
        # Hacer instalación opcional
        self.fields['instalacion'].required = False
        
        # Establecer fecha_pago por defecto a ahora
        if not self.instance.pk:
            ahora = timezone.now()
            self.fields['fecha_pago'].initial = ahora
            self.fields['fecha_pago'].widget.attrs['value'] = ahora.strftime('%Y-%m-%dT%H:%M')
        
        # Establecer método de pago por defecto a depósito
        if not self.instance.pk:
            self.fields['metodo_pago'].initial = 'deposito'
        
        # Establecer año por defecto al año actual
        if not self.instance.pk:
            self.fields['periodo_anio'].initial = timezone.now().year
        
        # Establecer mes por defecto al mes actual
        if not self.instance.pk:
            self.fields['periodo_mes'].initial = timezone.now().month
        
        # Hacer notas opcional
        self.fields['notas'].required = False
        
        # Limitar fecha_pago a no más de 1 hora en el futuro
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
        metodo_pago = cleaned_data.get('metodo_pago')
        referencia_pago = cleaned_data.get('referencia_pago')
        monto = cleaned_data.get('monto')
        
        # Validación: Instalación debe pertenecer al cliente
        if instalacion and cliente:
            if instalacion.cliente != cliente:
                raise ValidationError({
                    'instalacion': 'La instalación seleccionada no pertenece al cliente seleccionado.'
                })
        
        # Validación de monto
        if monto is not None:
            if monto <= 0:
                raise ValidationError({
                    'monto': 'El monto debe ser mayor a cero.'
                })
            if monto > 1000000:
                raise ValidationError({
                    'monto': 'El monto no puede ser mayor a $1,000,000.'
                })
        
        # Validación de períodos duplicados (excluyendo cancelados)
        if cliente and periodo_mes and periodo_anio:
            existing = Pago.objects.filter(
                cliente=cliente,
                periodo_mes=periodo_mes,
                periodo_anio=periodo_anio
            ).exclude(estado='cancelado')
            
            if instalacion:
                existing = existing.filter(instalacion=instalacion)
            else:
                existing = existing.filter(instalacion__isnull=True)
            
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                pago_duplicado = existing.first()
                mensaje = "Ya existe un pago activo para este cliente"
                if instalacion:
                    mensaje += f" e instalación ({instalacion.numero_contrato})"
                mensaje += f" en el período {dict(Pago.PERIODO_MES_CHOICES).get(periodo_mes, periodo_mes)} {periodo_anio}."
                
                raise ValidationError({
                    'periodo_mes': mensaje,
                    'periodo_anio': mensaje,
                })
        
        # Validación de fechas
        if fecha_vencimiento:
            if fecha_vencimiento < (date.today() - timedelta(days=3650)):
                raise ValidationError({
                    'fecha_vencimiento': 'La fecha de vencimiento no puede ser anterior a hace 10 años.'
                })
            if fecha_vencimiento > (date.today() + timedelta(days=1825)):
                raise ValidationError({
                    'fecha_vencimiento': 'La fecha de vencimiento no puede ser posterior a 5 años.'
                })
        
        # Validar que fecha_pago no sea muy futura
        if fecha_pago:
            ahora = timezone.now()
            if fecha_pago > (ahora + timedelta(hours=1)):
                raise ValidationError({
                    'fecha_pago': 'La fecha de pago no puede ser futura.'
                })
        
        # Validar que se proporcione referencia de pago para depósitos
        if metodo_pago in ['deposito', 'transferencia'] and not referencia_pago:
            raise ValidationError({
                'referencia_pago': 'La referencia de pago es requerida para depósitos y transferencias.'
            })
        
        return cleaned_data
    
    def save(self, commit=True):
        """Guarda el pago con estado 'pagado' automáticamente."""
        instance = super().save(commit=False)
        instance.estado = 'pagado'
        if commit:
            instance.save()
        return instance



