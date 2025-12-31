"""
Servicios para el módulo de pagos.
"""
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from decouple import config
from datetime import timedelta
from notificaciones.models import Notificacion, ConfiguracionNotificacion
import logging

logger = logging.getLogger(__name__)


class RecordatorioPagoService:
    """Servicio para crear y gestionar recordatorios de pagos."""
    
    @staticmethod
    def crear_recordatorio_antes_vencimiento(pago, dias_antes, tipo_notificacion, configuracion=None):
        """
        Crea un recordatorio para un pago que está por vencer.
        
        Args:
            pago: Instancia de Pago
            dias_antes: Días antes del vencimiento
            tipo_notificacion: TipoNotificacion para el recordatorio
            configuracion: ConfiguracionNotificacion (opcional)
        
        Returns:
            dict: {'success': bool, 'notificacion': Notificacion o None, 'error': str o None}
        """
        try:
            # Verificar que el cliente tenga email
            if not pago.cliente or not pago.cliente.email:
                return {
                    'success': False,
                    'error': 'El cliente no tiene correo electrónico configurado'
                }
            
            # Verificar que el pago no esté pagado
            if pago.estado == 'pagado':
                return {
                    'success': False,
                    'error': 'El pago ya está pagado'
                }
            
            # Determinar canal
            canal = 'email'
            if configuracion:
                canal = configuracion.canal_preferido
            
            # Generar asunto y mensaje
            asunto = f"Recordatorio: Pago próximo a vencer - {pago.concepto}"
            mensaje = RecordatorioPagoService._generar_mensaje_antes_vencimiento(pago, dias_antes)
            
            # Crear notificación
            notificacion = Notificacion.objects.create(
                cliente=pago.cliente,
                pago=pago,
                tipo=tipo_notificacion,
                asunto=asunto,
                mensaje=mensaje,
                canal=canal,
                estado='pendiente',
                fecha_programada=timezone.now()  # Enviar inmediatamente
            )
            
            return {
                'success': True,
                'notificacion': notificacion,
                'message': f'Recordatorio creado para {pago.cliente.nombre_completo}'
            }
            
        except Exception as e:
            logger.error(f'Error al crear recordatorio antes de vencimiento: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def crear_recordatorio_vencido(pago, dias_despues, tipo_notificacion, configuracion=None):
        """
        Crea un recordatorio para un pago vencido.
        
        Args:
            pago: Instancia de Pago
            dias_despues: Días después del vencimiento
            tipo_notificacion: TipoNotificacion para el recordatorio
            configuracion: ConfiguracionNotificacion (opcional)
        
        Returns:
            dict: {'success': bool, 'notificacion': Notificacion o None, 'error': str o None}
        """
        try:
            # Verificar que el cliente tenga email
            if not pago.cliente or not pago.cliente.email:
                return {
                    'success': False,
                    'error': 'El cliente no tiene correo electrónico configurado'
                }
            
            # Verificar que el pago no esté pagado
            if pago.estado == 'pagado':
                return {
                    'success': False,
                    'error': 'El pago ya está pagado'
                }
            
            # Determinar canal
            canal = 'email'
            if configuracion:
                canal = configuracion.canal_preferido
            
            # Calcular días vencido
            dias_vencido = (timezone.now().date() - pago.fecha_vencimiento).days
            
            # Generar asunto y mensaje
            asunto = f"⚠️ Pago Vencido - {pago.concepto}"
            mensaje = RecordatorioPagoService._generar_mensaje_vencido(pago, dias_vencido)
            
            # Crear notificación
            notificacion = Notificacion.objects.create(
                cliente=pago.cliente,
                pago=pago,
                tipo=tipo_notificacion,
                asunto=asunto,
                mensaje=mensaje,
                canal=canal,
                estado='pendiente',
                fecha_programada=timezone.now()  # Enviar inmediatamente
            )
            
            return {
                'success': True,
                'notificacion': notificacion,
                'message': f'Recordatorio creado para {pago.cliente.nombre_completo}'
            }
            
        except Exception as e:
            logger.error(f'Error al crear recordatorio vencido: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def _generar_mensaje_antes_vencimiento(pago, dias_antes):
        """Genera el mensaje de recordatorio antes de vencimiento."""
        cliente = pago.cliente
        fecha_vencimiento = pago.fecha_vencimiento.strftime('%d de %B de %Y')
        
        # Mensaje en texto plano
        mensaje_texto = f"""Estimado/a {cliente.nombre_completo},

Le recordamos que tiene un pago próximo a vencer:

DETALLES DEL PAGO:
• Concepto: {pago.concepto}
• Monto: ${pago.monto:,.2f}
• Fecha de vencimiento: {fecha_vencimiento}
• Días restantes: {dias_antes} día(s)

IMPORTANTE:
Por favor, realice el pago antes de la fecha de vencimiento para evitar interrupciones en su servicio.

Si tiene alguna pregunta o necesita asistencia, no dude en contactarnos.

Saludos cordiales,
Equipo AdminiRed
"""
        
        # Intentar generar mensaje HTML
        try:
            mensaje_html = render_to_string('pagos/emails/recordatorio_antes_vencimiento.html', {
                'cliente': cliente,
                'pago': pago,
                'fecha_vencimiento': fecha_vencimiento,
                'dias_antes': dias_antes,
            })
            return mensaje_html
        except Exception as e:
            logger.warning(f'No se pudo cargar plantilla HTML, usando texto plano: {str(e)}')
            return mensaje_texto
    
    @staticmethod
    def _generar_mensaje_vencido(pago, dias_vencido):
        """Genera el mensaje de recordatorio para pago vencido."""
        cliente = pago.cliente
        fecha_vencimiento = pago.fecha_vencimiento.strftime('%d de %B de %Y')
        
        # Mensaje en texto plano
        mensaje_texto = f"""Estimado/a {cliente.nombre_completo},

ATENCIÓN: Su pago está vencido

DETALLES DEL PAGO:
• Concepto: {pago.concepto}
• Monto: ${pago.monto:,.2f}
• Fecha de vencimiento: {fecha_vencimiento}
• Días vencido: {dias_vencido} día(s)

URGENTE:
Su pago está vencido. Por favor, realice el pago lo antes posible para evitar interrupciones en su servicio o recargos por mora.

Si tiene alguna pregunta o necesita asistencia, no dude en contactarnos.

Saludos cordiales,
Equipo AdminiRed
"""
        
        # Intentar generar mensaje HTML
        try:
            mensaje_html = render_to_string('pagos/emails/recordatorio_vencido.html', {
                'cliente': cliente,
                'pago': pago,
                'fecha_vencimiento': fecha_vencimiento,
                'dias_vencido': dias_vencido,
            })
            return mensaje_html
        except Exception as e:
            logger.warning(f'No se pudo cargar plantilla HTML, usando texto plano: {str(e)}')
            return mensaje_texto

