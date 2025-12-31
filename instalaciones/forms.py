from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
import re
from .models import Instalacion, TipoInstalacion, PlanInternet, ConfiguracionNumeroContrato
from clientes.models import Cliente


class InstalacionForm(forms.ModelForm):
    """Formulario para crear y editar instalaciones."""
    
    class Meta:
        model = Instalacion
        fields = [
            'cliente',
            'tipo_instalacion',
            'direccion_instalacion',
            'coordenadas',
            'plan',
            'plan_nombre',
            'velocidad_descarga',
            'velocidad_subida',
            'precio_mensual',
            'estado',
            'fecha_programada',
            'fecha_instalacion',
            'fecha_activacion',
            'ip_asignada',
            'mac_equipo',
            'numero_contrato',
            'notas_instalacion',
            'notas_tecnicas',
        ]
        widgets = {
            'cliente': forms.HiddenInput(),  # Campo oculto, se maneja con el buscador
            'tipo_instalacion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'direccion_instalacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa de instalación'
            }),
            'coordenadas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'latitud,longitud (ej: 19.4326,-99.1332)'
            }),
            'plan': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_plan'
            }),
            'plan_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_plan_nombre',
                'placeholder': 'Nombre del plan (ej: Plan Básico 50 Mbps)'
            }),
            'velocidad_descarga': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mbps',
                'min': 1
            }),
            'velocidad_subida': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mbps (opcional)',
                'min': 1
            }),
            'precio_mensual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': 0
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_programada': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_instalacion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_activacion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'ip_asignada': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '192.168.1.1'
            }),
            'mac_equipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00:1B:44:11:3A:B7'
            }),
            'numero_contrato': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número único de contrato'
            }),
            'notas_instalacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notas sobre la instalación'
            }),
            'notas_tecnicas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notas técnicas de la instalación'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos opcionales visualmente
        self.fields['tipo_instalacion'].required = False
        self.fields['coordenadas'].required = False
        self.fields['velocidad_subida'].required = False
        self.fields['fecha_programada'].required = False
        self.fields['fecha_instalacion'].required = False
        self.fields['fecha_activacion'].required = False
        self.fields['ip_asignada'].required = False
        self.fields['mac_equipo'].required = False
        self.fields['notas_instalacion'].required = False
        self.fields['notas_tecnicas'].required = False
        
        # Ordenar clientes por nombre completo
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre', 'apellido1')
        
        # Configurar campo plan (opcional)
        self.fields['plan'].required = False
        self.fields['plan'].queryset = PlanInternet.objects.filter(activo=True).order_by('precio_mensual', 'velocidad_descarga')
        self.fields['plan'].empty_label = '-- Seleccionar del catálogo (opcional) --'
        
        # Hacer número de contrato opcional (se genera automáticamente si no se proporciona)
        self.fields['numero_contrato'].required = False
        if not self.instance or not self.instance.pk:
            # En creación, el número de contrato es opcional (se genera automáticamente)
            self.fields['numero_contrato'].widget.attrs['placeholder'] = 'Se generará automáticamente si se deja vacío'
    
    def clean_cliente(self):
        """Valida que el cliente exista y esté activo."""
        cliente = self.cleaned_data.get('cliente')
        if not cliente:
            raise ValidationError('Debe seleccionar un cliente.')
        return cliente
    
    def clean_plan(self):
        """Valida que el plan esté activo si se selecciona."""
        plan = self.cleaned_data.get('plan')
        if plan and not plan.activo:
            raise ValidationError('El plan seleccionado no está activo.')
        return plan
    
    def clean_velocidad_descarga(self):
        """Valida la velocidad de descarga."""
        velocidad = self.cleaned_data.get('velocidad_descarga')
        if velocidad is not None and velocidad <= 0:
            raise ValidationError('La velocidad de descarga debe ser mayor a 0.')
        if velocidad is not None and velocidad > 10000:
            raise ValidationError('La velocidad de descarga no puede ser mayor a 10,000 Mbps.')
        return velocidad
    
    def clean_velocidad_subida(self):
        """Valida la velocidad de subida."""
        velocidad = self.cleaned_data.get('velocidad_subida')
        if velocidad is not None and velocidad <= 0:
            raise ValidationError('La velocidad de subida debe ser mayor a 0.')
        if velocidad is not None and velocidad > 10000:
            raise ValidationError('La velocidad de subida no puede ser mayor a 10,000 Mbps.')
        return velocidad
    
    def clean_precio_mensual(self):
        """Valida el precio mensual."""
        precio = self.cleaned_data.get('precio_mensual')
        if precio is not None and precio < 0:
            raise ValidationError('El precio mensual no puede ser negativo.')
        if precio is not None and precio > 1000000:
            raise ValidationError('El precio mensual no puede ser mayor a $1,000,000.')
        return precio
    
    def clean_mac_equipo(self):
        """Valida el formato de MAC address."""
        mac = self.cleaned_data.get('mac_equipo')
        if mac:
            # Formato MAC: XX:XX:XX:XX:XX:XX o XX-XX-XX-XX-XX-XX
            mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
            if not re.match(mac_pattern, mac):
                raise ValidationError(
                    'El formato de MAC address es inválido. Use el formato: XX:XX:XX:XX:XX:XX o XX-XX-XX-XX-XX-XX'
                )
        return mac
    
    def clean_coordenadas(self):
        """Valida el formato de coordenadas."""
        coordenadas = self.cleaned_data.get('coordenadas')
        if coordenadas:
            # Formato: lat,lon o lat, lon
            try:
                coords = coordenadas.replace(' ', '').split(',')
                if len(coords) != 2:
                    raise ValueError()
                lat = float(coords[0])
                lon = float(coords[1])
                if not (-90 <= lat <= 90):
                    raise ValidationError('La latitud debe estar entre -90 y 90.')
                if not (-180 <= lon <= 180):
                    raise ValidationError('La longitud debe estar entre -180 y 180.')
            except (ValueError, IndexError):
                raise ValidationError(
                    'El formato de coordenadas es inválido. Use el formato: latitud,longitud (ej: 19.4326,-99.1332)'
                )
        return coordenadas
    
    def clean_numero_contrato(self):
        """Valida que el número de contrato sea único."""
        numero_contrato = self.cleaned_data.get('numero_contrato')
        if numero_contrato:
            # Verificar unicidad excluyendo la instancia actual
            qs = Instalacion.objects.filter(numero_contrato=numero_contrato)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('Este número de contrato ya está en uso.')
        return numero_contrato
    
    def clean(self):
        """Validaciones cruzadas."""
        cleaned_data = super().clean()
        
        # Validar que si se selecciona un plan, se llenen los campos automáticamente
        plan = cleaned_data.get('plan')
        plan_nombre = cleaned_data.get('plan_nombre')
        velocidad_descarga = cleaned_data.get('velocidad_descarga')
        velocidad_subida = cleaned_data.get('velocidad_subida')
        precio_mensual = cleaned_data.get('precio_mensual')
        
        if plan:
            # Si se selecciona un plan, usar sus valores si los campos están vacíos
            if not plan_nombre:
                cleaned_data['plan_nombre'] = plan.nombre
            if not velocidad_descarga:
                cleaned_data['velocidad_descarga'] = plan.velocidad_descarga
            if velocidad_subida is None and plan.velocidad_subida:
                cleaned_data['velocidad_subida'] = plan.velocidad_subida
            if not precio_mensual:
                cleaned_data['precio_mensual'] = plan.precio_mensual
        
        # Validar que plan_nombre esté presente si no hay plan
        if not plan and not plan_nombre:
            raise ValidationError({
                'plan_nombre': 'Debe especificar un nombre de plan o seleccionar uno del catálogo.'
            })
        
        # Validar que velocidad_descarga esté presente
        if not velocidad_descarga:
            raise ValidationError({
                'velocidad_descarga': 'La velocidad de descarga es requerida.'
            })
        
        # Validar que precio_mensual esté presente
        if not precio_mensual:
            raise ValidationError({
                'precio_mensual': 'El precio mensual es requerido.'
            })
        
        # Validar fechas en orden lógico
        fecha_programada = cleaned_data.get('fecha_programada')
        fecha_instalacion = cleaned_data.get('fecha_instalacion')
        fecha_activacion = cleaned_data.get('fecha_activacion')
        estado = cleaned_data.get('estado')
        
        if fecha_instalacion and fecha_programada:
            if fecha_instalacion < fecha_programada:
                raise ValidationError({
                    'fecha_instalacion': 'La fecha de instalación no puede ser anterior a la fecha programada.'
                })
        
        if fecha_activacion and fecha_instalacion:
            if fecha_activacion < fecha_instalacion:
                raise ValidationError({
                    'fecha_activacion': 'La fecha de activación no puede ser anterior a la fecha de instalación.'
                })
        
        if fecha_activacion and fecha_programada:
            if fecha_activacion < fecha_programada:
                raise ValidationError({
                    'fecha_activacion': 'La fecha de activación no puede ser anterior a la fecha programada.'
                })
        
        # Validar estado según fechas
        if estado == 'activa' and not fecha_activacion:
            # Si el estado es activa pero no hay fecha de activación, sugerirla
            if fecha_instalacion:
                cleaned_data['fecha_activacion'] = fecha_instalacion
            elif fecha_programada:
                cleaned_data['fecha_activacion'] = fecha_programada
            else:
                cleaned_data['fecha_activacion'] = timezone.now()
        
        if estado == 'programada' and not fecha_programada:
            raise ValidationError({
                'fecha_programada': 'La fecha programada es requerida cuando el estado es "Programada".'
            })
        
        if estado in ['en_proceso', 'activa'] and not fecha_instalacion:
            raise ValidationError({
                'fecha_instalacion': f'La fecha de instalación es requerida cuando el estado es "{estado}".'
            })
        
        return cleaned_data


class ConfiguracionNumeroContratoForm(forms.ModelForm):
    """Formulario para configurar la generación de números de contrato."""
    
    class Meta:
        model = ConfiguracionNumeroContrato
        fields = [
            'activa',
            'formato',
            'prefijo',
            'numero_inicial',
            'digitos_secuencia',
            'reiniciar_diario',
        ]
        widgets = {
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'formato': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: INST-{YYYY}{MM}{DD}-{####}',
                'id': 'id_formato'
            }),
            'prefijo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'INST',
                'maxlength': 20
            }),
            'numero_inicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'step': 1
            }),
            'digitos_secuencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'step': 1
            }),
            'reiniciar_diario': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_formato(self):
        """Valida que el formato contenga {####}."""
        formato = self.cleaned_data.get('formato')
        if '{####}' not in formato:
            raise ValidationError(
                'El formato debe contener {####} para el número secuencial.'
            )
        return formato
    
    def clean_digitos_secuencia(self):
        """Valida los dígitos de secuencia."""
        digitos = self.cleaned_data.get('digitos_secuencia')
        if digitos < 1 or digitos > 10:
            raise ValidationError('Los dígitos de secuencia deben estar entre 1 y 10.')
        return digitos

