"""
Servicios para enviar notificaciones por diferentes canales.
"""
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from decouple import config

logger = logging.getLogger(__name__)


class NotificationService:
    """Servicio base para enviar notificaciones."""
    
    @staticmethod
    def send_email(notificacion):
        """Envía una notificación por correo electrónico."""
        try:
            if not notificacion.cliente or not notificacion.cliente.email:
                return {
                    'success': False,
                    'error': 'El cliente no tiene correo electrónico configurado'
                }
            
            from_email = config('DEFAULT_FROM_EMAIL', default='noreply@adminired.com')
            recipient_list = [notificacion.cliente.email]
            
            # Verificar si el mensaje es HTML
            es_html = '<html' in notificacion.mensaje.lower() or '<!DOCTYPE' in notificacion.mensaje.upper()
            
            if es_html:
                # Enviar email HTML
                from django.core.mail import EmailMultiAlternatives
                
                # Extraer texto plano del HTML (simple)
                import re
                texto_plano = re.sub(r'<[^>]+>', '', notificacion.mensaje)
                texto_plano = re.sub(r'\s+', ' ', texto_plano).strip()
                
                msg = EmailMultiAlternatives(
                    subject=notificacion.asunto,
                    body=texto_plano,
                    from_email=from_email,
                    to=recipient_list
                )
                msg.attach_alternative(notificacion.mensaje, "text/html")
                msg.send()
            else:
                # Enviar email de texto plano
                send_mail(
                    subject=notificacion.asunto,
                    message=notificacion.mensaje,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
            
            return {
                'success': True,
                'message': f'Email enviado exitosamente a {notificacion.cliente.email}'
            }
        except Exception as e:
            logger.error(f'Error al enviar email: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def send_sms(notificacion):
        """Envía una notificación por SMS usando Twilio."""
        try:
            if not notificacion.cliente or not notificacion.cliente.telefono:
                return {
                    'success': False,
                    'error': 'El cliente no tiene teléfono configurado'
                }
            
            # Verificar si Twilio está configurado
            twilio_account_sid = config('TWILIO_ACCOUNT_SID', default='')
            twilio_auth_token = config('TWILIO_AUTH_TOKEN', default='')
            twilio_phone_number = config('TWILIO_PHONE_NUMBER', default='')
            
            if not all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
                return {
                    'success': False,
                    'error': 'Twilio no está configurado. Agrega TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN y TWILIO_PHONE_NUMBER en .env'
                }
            
            # Importar Twilio solo si está disponible
            try:
                from twilio.rest import Client
            except ImportError:
                return {
                    'success': False,
                    'error': 'Twilio no está instalado. Ejecuta: pip install twilio'
                }
            
            # Limpiar número de teléfono (remover caracteres especiales)
            telefono = ''.join(filter(str.isdigit, notificacion.cliente.telefono))
            
            # Agregar código de país si no está presente (México: +52)
            if not telefono.startswith('52'):
                telefono = f'52{telefono}'
            if not telefono.startswith('+'):
                telefono = f'+{telefono}'
            
            # Crear cliente de Twilio
            client = Client(twilio_account_sid, twilio_auth_token)
            
            # Enviar SMS
            message = client.messages.create(
                body=notificacion.mensaje,
                from_=twilio_phone_number,
                to=telefono
            )
            
            return {
                'success': True,
                'message': f'SMS enviado exitosamente. SID: {message.sid}',
                'sid': message.sid
            }
        except Exception as e:
            logger.error(f'Error al enviar SMS: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def send_whatsapp(notificacion):
        """Envía una notificación por WhatsApp usando Twilio WhatsApp API."""
        try:
            if not notificacion.cliente or not notificacion.cliente.telefono:
                return {
                    'success': False,
                    'error': 'El cliente no tiene teléfono configurado'
                }
            
            # Verificar si Twilio está configurado
            twilio_account_sid = config('TWILIO_ACCOUNT_SID', default='')
            twilio_auth_token = config('TWILIO_AUTH_TOKEN', default='')
            twilio_whatsapp_from = config('TWILIO_WHATSAPP_FROM', default='whatsapp:+14155238886')
            
            if not all([twilio_account_sid, twilio_auth_token]):
                return {
                    'success': False,
                    'error': 'Twilio no está configurado. Agrega TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN en .env'
                }
            
            # Importar Twilio solo si está disponible
            try:
                from twilio.rest import Client
            except ImportError:
                return {
                    'success': False,
                    'error': 'Twilio no está instalado. Ejecuta: pip install twilio'
                }
            
            # Limpiar número de teléfono (remover caracteres especiales)
            telefono = ''.join(filter(str.isdigit, notificacion.cliente.telefono))
            
            # Agregar código de país si no está presente (México: +52)
            if not telefono.startswith('52'):
                telefono = f'52{telefono}'
            if not telefono.startswith('+'):
                telefono = f'+{telefono}'
            
            # Formatear para WhatsApp
            whatsapp_to = f'whatsapp:{telefono}'
            
            # Crear cliente de Twilio
            client = Client(twilio_account_sid, twilio_auth_token)
            
            # Enviar WhatsApp
            message = client.messages.create(
                body=notificacion.mensaje,
                from_=twilio_whatsapp_from,
                to=whatsapp_to
            )
            
            return {
                'success': True,
                'message': f'WhatsApp enviado exitosamente. SID: {message.sid}',
                'sid': message.sid
            }
        except Exception as e:
            logger.error(f'Error al enviar WhatsApp: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def send_notification(notificacion):
        """Envía una notificación según su canal."""
        if not notificacion.debe_enviarse:
            return {
                'success': False,
                'error': 'La notificación no está lista para enviarse'
            }
        
        resultado = None
        
        try:
            if notificacion.canal == 'email':
                resultado = NotificationService.send_email(notificacion)
            elif notificacion.canal == 'sms':
                resultado = NotificationService.send_sms(notificacion)
            elif notificacion.canal == 'whatsapp':
                resultado = NotificationService.send_whatsapp(notificacion)
            elif notificacion.canal == 'sistema':
                # Para notificaciones del sistema, solo marcamos como enviada
                resultado = {
                    'success': True,
                    'message': 'Notificación del sistema registrada'
                }
            else:
                resultado = {
                    'success': False,
                    'error': f'Canal no soportado: {notificacion.canal}'
                }
            
            # Actualizar estado de la notificación
            if resultado.get('success'):
                mensaje_resultado = resultado.get('message', 'Enviado exitosamente')
                if resultado.get('sid'):
                    mensaje_resultado += f" | SID: {resultado['sid']}"
                notificacion.marcar_como_enviada(resultado=mensaje_resultado)
            else:
                error_msg = resultado.get('error', 'Error desconocido')
                notificacion.marcar_como_fallida(resultado=error_msg)
            
            return resultado
            
        except Exception as e:
            logger.error(f'Error al procesar notificación {notificacion.pk}: {str(e)}')
            notificacion.marcar_como_fallida(resultado=f'Error: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }



