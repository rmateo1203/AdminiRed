"""
Servicio para generar números de contrato automáticamente.
"""
from django.utils import timezone
from datetime import datetime
from .models import Instalacion, ConfiguracionNumeroContrato


class NumeroContratoService:
    """Servicio para generar números de contrato dinámicamente."""
    
    @staticmethod
    def generar_numero_contrato(instalacion):
        """
        Genera un número de contrato automático basado en la configuración activa.
        
        Args:
            instalacion: Instancia de Instalacion (puede no estar guardada aún)
        
        Returns:
            str: Número de contrato generado
        """
        config = ConfiguracionNumeroContrato.get_activa()
        
        if not config or not config.activa:
            # Si no hay configuración, usar formato por defecto
            return NumeroContratoService._generar_formato_default(instalacion)
        
        # Construir el número según el formato configurado
        partes = []
        
        # Prefijo
        if config.prefijo:
            partes.append(config.prefijo)
        
        # Año
        if config.incluir_anio:
            anio = timezone.now().year
            if config.formato_anio == 'completo':
                partes.append(str(anio))
            elif config.formato_anio == 'corto':
                partes.append(str(anio)[-2:])
        
        # Mes
        if config.incluir_mes:
            mes = timezone.now().month
            partes.append(f"{mes:02d}")
        
        # Secuencia
        if config.incluir_secuencia:
            secuencia = NumeroContratoService._obtener_siguiente_secuencia(config)
            partes.append(f"{secuencia:0{config.longitud_secuencia}d}")
        
        # Sufijo
        if config.sufijo:
            partes.append(config.sufijo)
        
        numero_contrato = config.separador.join(partes)
        
        # Verificar unicidad
        if Instalacion.objects.filter(numero_contrato=numero_contrato).exists():
            # Si ya existe, agregar un sufijo único
            contador = 1
            while Instalacion.objects.filter(numero_contrato=f"{numero_contrato}-{contador}").exists():
                contador += 1
            numero_contrato = f"{numero_contrato}-{contador}"
        
        return numero_contrato
    
    @staticmethod
    def _generar_formato_default(instalacion):
        """Genera un número de contrato con formato por defecto."""
        anio = timezone.now().year
        mes = timezone.now().month
        
        # Contar instalaciones del mes actual
        inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        cantidad = Instalacion.objects.filter(fecha_solicitud__gte=inicio_mes).count()
        
        # Formato: CONT-YYYYMM-XXXX
        numero = f"CONT-{anio}{mes:02d}-{cantidad + 1:04d}"
        
        # Verificar unicidad
        if Instalacion.objects.filter(numero_contrato=numero).exists():
            contador = 1
            while Instalacion.objects.filter(numero_contrato=f"{numero}-{contador}").exists():
                contador += 1
            numero = f"{numero}-{contador}"
        
        return numero
    
    @staticmethod
    def _obtener_siguiente_secuencia(config):
        """Obtiene el siguiente número de secuencia según la configuración."""
        if config.resetear_secuencia == 'nunca':
            # Secuencia continua sin reset - contar todas las instalaciones
            cantidad = Instalacion.objects.count()
            return cantidad + 1
        elif config.resetear_secuencia == 'mensual':
            # Reset mensual
            inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            cantidad = Instalacion.objects.filter(fecha_solicitud__gte=inicio_mes).count()
            return cantidad + 1
        elif config.resetear_secuencia == 'anual':
            # Reset anual
            inicio_anio = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            cantidad = Instalacion.objects.filter(fecha_solicitud__gte=inicio_anio).count()
            return cantidad + 1
        else:
            return 1
    
    @staticmethod
    def obtener_preview(config=None):
        """
        Obtiene un preview del número de contrato que se generaría.
        
        Args:
            config: ConfiguracionNumeroContrato (opcional, si no se proporciona usa la activa)
        
        Returns:
            str: Preview del número de contrato
        """
        if config is None:
            config = ConfiguracionNumeroContrato.get_activa()
        
        if not config or not config.activa:
            return NumeroContratoService._generar_formato_default(None)
        
        # Crear una instalación temporal para el preview
        class InstalacionPreview:
            pass
        
        instalacion_preview = InstalacionPreview()
        return NumeroContratoService.generar_numero_contrato(instalacion_preview)
