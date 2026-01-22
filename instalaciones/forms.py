from django import forms
from django.core.exceptions import ValidationError
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
                'placeholder': 'Se genera automáticamente si se deja vacío'
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
    
    def clean_ip_asignada(self):
        """Valida que la IP sea única."""
        ip = self.cleaned_data.get('ip_asignada')
        if ip:
            qs = Instalacion.objects.filter(ip_asignada=ip)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                instalacion_existente = qs.first()
                raise forms.ValidationError(
                    f'Esta IP ya está asignada a la instalación {instalacion_existente.numero_contrato} '
                    f'({instalacion_existente.cliente.nombre_completo}).'
                )
        return ip
    
    def clean_mac_equipo(self):
        """Valida que la MAC sea única y tenga formato correcto."""
        mac = self.cleaned_data.get('mac_equipo')
        if mac:
            # Normalizar MAC
            mac_normalizada = mac.upper().replace(' ', '').replace('-', ':')
            
            # Validar formato
            import re
            if not re.match(r'^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$', mac_normalizada):
                raise forms.ValidationError(
                    'Formato de MAC inválido. Use formato: 00:1B:44:11:3A:B7 o 00-1B-44-11-3A-B7'
                )
            
            # Validar unicidad
            qs = Instalacion.objects.filter(mac_equipo=mac_normalizada)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                instalacion_existente = qs.first()
                raise forms.ValidationError(
                    f'Esta MAC ya está asignada a la instalación {instalacion_existente.numero_contrato} '
                    f'({instalacion_existente.cliente.nombre_completo}).'
                )
            
            return mac_normalizada
        return mac


class ConfiguracionNumeroContratoForm(forms.ModelForm):
    """Formulario para configurar la generación automática de números de contrato."""
    
    class Meta:
        model = ConfiguracionNumeroContrato
        fields = [
            'activa',
            'prefijo',
            'separador',
            'sufijo',
            'incluir_anio',
            'formato_anio',
            'incluir_mes',
            'incluir_secuencia',
            'longitud_secuencia',
            'resetear_secuencia',
        ]
        widgets = {
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'prefijo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CONT, INST, etc.'
            }),
            'separador': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '-',
                'maxlength': 5
            }),
            'sufijo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sufijo opcional'
            }),
            'incluir_anio': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'formato_anio': forms.Select(attrs={
                'class': 'form-control'
            }),
            'incluir_mes': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'incluir_secuencia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'longitud_secuencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'resetear_secuencia': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer algunos campos opcionales
        self.fields['sufijo'].required = False
        self.fields['prefijo'].required = False

