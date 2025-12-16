from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class CategoriaMaterial(models.Model):
    """Categorías de materiales (Cables, Equipos, Accesorios, etc.)"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre de categoría')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    
    class Meta:
        verbose_name = 'Categoría de Material'
        verbose_name_plural = 'Categorías de Materiales'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Material(models.Model):
    """Modelo para gestionar materiales del inventario."""
    
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('bajo_stock', 'Bajo Stock'),
        ('agotado', 'Agotado'),
        ('descontinuado', 'Descontinuado'),
    ]
    
    UNIDAD_MEDIDA_CHOICES = [
        ('pza', 'Pieza (Pza)'),
        ('caja', 'Caja'),
        ('paquete', 'Paquete'),
        ('rollo', 'Rollo'),
        ('metro', 'Metro (m)'),
        ('kg', 'Kilogramo (Kg)'),
        ('litro', 'Litro (L)'),
        ('par', 'Par'),
        ('juego', 'Juego'),
        ('bolsa', 'Bolsa'),
        ('bobina', 'Bobina'),
        ('carrete', 'Carrete'),
        ('unidad', 'Unidad'),
        ('docena', 'Docena'),
        ('millar', 'Millar'),
        ('otro', 'Otro'),
    ]
    
    # Información básica
    nombre = models.CharField(max_length=200, verbose_name='Nombre del material')
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código del material')
    categoria = models.ForeignKey(
        CategoriaMaterial,
        on_delete=models.SET_NULL,
        null=True,
        related_name='materiales',
        verbose_name='Categoría'
    )
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    
    # Stock
    stock_actual = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock actual'
    )
    stock_minimo = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock mínimo',
        help_text='Cantidad mínima antes de alertar'
    )
    unidad_medida = models.CharField(
        max_length=20,
        choices=UNIDAD_MEDIDA_CHOICES,
        default='pza',
        verbose_name='Unidad de medida'
    )
    
    # Precios
    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio de compra',
        blank=True,
        null=True
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio de venta',
        blank=True,
        null=True
    )
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='disponible',
        verbose_name='Estado'
    )
    
    # Ubicación
    ubicacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ubicación en almacén'
    )
    
    # Fechas
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['categoria', 'estado']),
            models.Index(fields=['stock_actual']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    
    @property
    def necesita_reposicion(self):
        """Verifica si el material necesita reposición."""
        return self.stock_actual <= self.stock_minimo
    
    @property
    def esta_agotado(self):
        """Verifica si el material está agotado."""
        return self.stock_actual == 0
    
    def reducir_stock(self, cantidad):
        """Reduce el stock del material."""
        if self.stock_actual >= cantidad:
            self.stock_actual -= cantidad
            self.actualizar_estado()
            self.save()
            return True
        return False
    
    def aumentar_stock(self, cantidad):
        """Aumenta el stock del material."""
        self.stock_actual += cantidad
        self.actualizar_estado()
        self.save()
    
    def actualizar_estado(self):
        """Actualiza el estado según el stock."""
        if self.stock_actual == 0:
            self.estado = 'agotado'
        elif self.stock_actual <= self.stock_minimo:
            self.estado = 'bajo_stock'
        else:
            self.estado = 'disponible'


class MovimientoInventario(models.Model):
    """Modelo para registrar movimientos de inventario."""
    
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
        ('devolucion', 'Devolución'),
    ]
    
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='movimientos',
        verbose_name='Material'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de movimiento'
    )
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad'
    )
    motivo = models.CharField(max_length=200, verbose_name='Motivo')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    notas = models.TextField(blank=True, null=True, verbose_name='Notas')
    
    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['material', 'fecha']),
            models.Index(fields=['tipo']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.material.nombre} - {self.cantidad}"
