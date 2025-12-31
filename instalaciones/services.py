"""
Servicios para el módulo de instalaciones.
"""
from django.core.cache import cache
from django.utils import timezone
from datetime import datetime
from .models import ConfiguracionNumeroContrato, Instalacion
import re


class NumeroContratoService:
    """Servicio para generar números de contrato dinámicamente."""
    
    @staticmethod
    def generar_numero_contrato():
        """
        Genera un número de contrato único basado en la configuración activa.
        
        Returns:
            str: Número de contrato generado
        """
        config = ConfiguracionNumeroContrato.get_activa()
        
        # Obtener fecha actual
        ahora = timezone.now()
        fecha = ahora.date()
        
        # Reemplazar variables de fecha
        formato = config.formato
        formato = formato.replace('{YYYY}', str(ahora.year))
        formato = formato.replace('{YY}', str(ahora.year)[-2:])
        formato = formato.replace('{MM}', f"{ahora.month:02d}")
        formato = formato.replace('{DD}', f"{ahora.day:02d}")
        formato = formato.replace('{PREFIJO}', config.prefijo or 'INST')
        
        # Generar número secuencial
        if config.reiniciar_diario:
            # Buscar el último número del día
            # Crear patrón base sin el número secuencial
            patron_base = formato.replace('{####}', '')
            # Reemplazar variables de fecha en el patrón base
            patron_base = patron_base.replace('{YYYY}', str(ahora.year))
            patron_base = patron_base.replace('{YY}', str(ahora.year)[-2:])
            patron_base = patron_base.replace('{MM}', f"{ahora.month:02d}")
            patron_base = patron_base.replace('{DD}', f"{ahora.day:02d}")
            patron_base = patron_base.replace('{PREFIJO}', config.prefijo or 'INST')
            
            # Buscar instalaciones que empiecen con el patrón base del día
            instalaciones_del_dia = Instalacion.objects.filter(
                numero_contrato__startswith=patron_base
            )
            
            # Extraer números secuenciales (últimos N dígitos según config.digitos_secuencia)
            numeros_usados = []
            for inst in instalaciones_del_dia:
                # Extraer los últimos N dígitos (donde N = digitos_secuencia)
                match = re.search(r'(\d{' + str(config.digitos_secuencia) + r'})$', inst.numero_contrato)
                if match:
                    try:
                        numero = int(match.group(1))
                        numeros_usados.append(numero)
                    except ValueError:
                        pass
            
            # Encontrar el siguiente número disponible
            if numeros_usados:
                siguiente_numero = max(numeros_usados) + 1
            else:
                siguiente_numero = config.numero_inicial
        else:
            # Secuencia global (no se reinicia diariamente)
            # Buscar todas las instalaciones que coincidan con el patrón base
            # Crear patrón base sin el número secuencial
            patron_base = formato.replace('{####}', '')
            patron_base = patron_base.replace('{YYYY}', '')
            patron_base = patron_base.replace('{YY}', '')
            patron_base = patron_base.replace('{MM}', '')
            patron_base = patron_base.replace('{DD}', '')
            patron_base = patron_base.replace('{PREFIJO}', config.prefijo or 'INST')
            
            # Obtener todas las instalaciones y filtrar las que coincidan con el patrón
            todas_instalaciones = Instalacion.objects.all()
            instalaciones_coincidentes = []
            
            for inst in todas_instalaciones:
                # Verificar si el número de contrato empieza con el patrón base
                if inst.numero_contrato.startswith(patron_base):
                    instalaciones_coincidentes.append(inst)
            
            # Extraer números secuenciales
            numeros_usados = []
            for inst in instalaciones_coincidentes:
                # Extraer los últimos N dígitos
                match = re.search(r'(\d{' + str(config.digitos_secuencia) + r'})$', inst.numero_contrato)
                if match:
                    try:
                        numero = int(match.group(1))
                        numeros_usados.append(numero)
                    except ValueError:
                        pass
            
            if numeros_usados:
                siguiente_numero = max(numeros_usados) + 1
            else:
                siguiente_numero = config.numero_inicial
        
        # Formatear número con la cantidad de dígitos especificada
        numero_formateado = f"{siguiente_numero:0{config.digitos_secuencia}d}"
        
        # Reemplazar {####} con el número formateado
        numero_contrato = formato.replace('{####}', numero_formateado)
        
        # Verificar unicidad y ajustar si es necesario
        intentos = 0
        while Instalacion.objects.filter(numero_contrato=numero_contrato).exists():
            siguiente_numero += 1
            numero_formateado = f"{siguiente_numero:0{config.digitos_secuencia}d}"
            numero_contrato = formato.replace('{####}', numero_formateado)
            intentos += 1
            if intentos > 1000:  # Prevenir loops infinitos
                raise ValueError('No se pudo generar un número de contrato único después de 1000 intentos')
        
        return numero_contrato
    
    @staticmethod
    def obtener_preview(formato, prefijo='INST', numero_inicial=1, digitos_secuencia=4, reiniciar_diario=True):
        """
        Genera un preview del formato de número de contrato.
        
        Args:
            formato: Formato del número de contrato
            prefijo: Prefijo personalizado
            numero_inicial: Número inicial
            digitos_secuencia: Dígitos de secuencia
            reiniciar_diario: Si reinicia diariamente
        
        Returns:
            str: Preview del número de contrato
        """
        ahora = timezone.now()
        
        # Reemplazar variables
        preview = formato
        preview = preview.replace('{YYYY}', str(ahora.year))
        preview = preview.replace('{YY}', str(ahora.year)[-2:])
        preview = preview.replace('{MM}', f"{ahora.month:02d}")
        preview = preview.replace('{DD}', f"{ahora.day:02d}")
        preview = preview.replace('{PREFIJO}', prefijo or 'INST')
        
        # Reemplazar número secuencial
        numero_formateado = f"{numero_inicial:0{digitos_secuencia}d}"
        preview = preview.replace('{####}', numero_formateado)
        
        return preview

