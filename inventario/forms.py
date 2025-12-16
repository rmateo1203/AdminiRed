from django import forms
from .models import Material, MovimientoInventario, CategoriaMaterial


class CategoriaMaterialForm(forms.ModelForm):
    """Formulario para crear y editar categorías de materiales."""
    
    class Meta:
        model = CategoriaMaterial
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la categoría (opcional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].required = False


class MaterialForm(forms.ModelForm):
    """Formulario para crear y editar materiales."""
    
    class Meta:
        model = Material
        fields = [
            'nombre',
            'codigo',
            'categoria',
            'descripcion',
            'stock_actual',
            'stock_minimo',
            'unidad_medida',
            'precio_compra',
            'precio_venta',
            'ubicacion',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del material'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único del material'
            }),
            'categoria': forms.HiddenInput(),  # Campo oculto, se maneja con el buscador
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del material'
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': '0'
            }),
            'unidad_medida': forms.HiddenInput(),  # Campo oculto, se maneja con el buscador
            'precio_compra': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'placeholder': '0.00'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'placeholder': '0.00'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ubicación en almacén'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = CategoriaMaterial.objects.all().order_by('nombre')
        self.fields['categoria'].required = False
        self.fields['descripcion'].required = False
        self.fields['precio_compra'].required = False
        self.fields['precio_venta'].required = False
        self.fields['ubicacion'].required = False


class MovimientoInventarioForm(forms.ModelForm):
    """Formulario para crear movimientos de inventario."""
    
    class Meta:
        model = MovimientoInventario
        fields = [
            'material',
            'tipo',
            'cantidad',
            'motivo',
            'notas',
        ]
        widgets = {
            'material': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '1'
            }),
            'motivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Motivo del movimiento'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.all().order_by('nombre')
        self.fields['notas'].required = False
    
    def save(self, commit=True):
        movimiento = super().save(commit=False)
        if commit:
            # Actualizar stock según el tipo de movimiento
            material = movimiento.material
            if movimiento.tipo == 'entrada':
                material.aumentar_stock(movimiento.cantidad)
            elif movimiento.tipo == 'salida':
                if material.stock_actual >= movimiento.cantidad:
                    material.reducir_stock(movimiento.cantidad)
                else:
                    raise forms.ValidationError(f'Stock insuficiente. Stock actual: {material.stock_actual}')
            elif movimiento.tipo == 'ajuste':
                # Para ajustes, se puede aumentar o disminuir según la cantidad
                if movimiento.cantidad > 0:
                    material.aumentar_stock(movimiento.cantidad)
                else:
                    material.reducir_stock(abs(movimiento.cantidad))
            
            movimiento.save()
        return movimiento



