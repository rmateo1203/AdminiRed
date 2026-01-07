"""
Módulo para integración con pasarelas de pago.
Soporta múltiples pasarelas: Stripe, Mercado Pago, PayPal, etc.
"""
import logging
import json
import requests
from django.conf import settings
from django.utils import timezone
from .models import TransaccionPago

# Import opcional de Stripe
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None

# Import opcional de Mercado Pago
try:
    import mercadopago
    MERCADOPAGO_AVAILABLE = True
except ImportError:
    MERCADOPAGO_AVAILABLE = False
    mercadopago = None

logger = logging.getLogger(__name__)


class PaymentGateway:
    """Clase base para pasarelas de pago."""
    
    def __init__(self, pasarela='stripe'):
        self.pasarela = pasarela
        self._configure()
    
    def _configure(self):
        """Configura la pasarela de pago."""
        if self.pasarela == 'stripe':
            if not STRIPE_AVAILABLE:
                raise ImportError("stripe no está instalado. Ejecuta: pip install stripe")
            stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
            if not stripe.api_key:
                logger.warning("STRIPE_SECRET_KEY no configurada en settings")
        elif self.pasarela == 'mercadopago':
            if not MERCADOPAGO_AVAILABLE:
                raise ImportError("mercadopago no está instalado. Ejecuta: pip install mercadopago")
            self.mp = mercadopago.SDK(getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', ''))
            if not getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', ''):
                logger.warning("MERCADOPAGO_ACCESS_TOKEN no configurada en settings")
        elif self.pasarela == 'paypal':
            self.paypal_client_id = getattr(settings, 'PAYPAL_CLIENT_ID', '')
            self.paypal_secret = getattr(settings, 'PAYPAL_SECRET', '')
            self.paypal_mode = getattr(settings, 'PAYPAL_MODE', 'sandbox')  # sandbox o live
            if not self.paypal_client_id or not self.paypal_secret:
                logger.warning("PAYPAL_CLIENT_ID o PAYPAL_SECRET no configuradas en settings")
    
    def crear_intento_pago(self, pago, return_url=None, cancel_url=None):
        """
        Crea un intento de pago en la pasarela.
        
        Args:
            pago: Instancia del modelo Pago
            return_url: URL de retorno después del pago exitoso
            cancel_url: URL de cancelación
        
        Returns:
            dict: Información del intento de pago
        """
        if self.pasarela == 'stripe':
            return self._crear_intento_stripe(pago, return_url, cancel_url)
        elif self.pasarela == 'mercadopago':
            return self._crear_intento_mercadopago(pago, return_url, cancel_url)
        elif self.pasarela == 'paypal':
            return self._crear_intento_paypal(pago, return_url, cancel_url)
        else:
            raise ValueError(f"Pasarela {self.pasarela} no soportada")
    
    def _crear_intento_stripe(self, pago, return_url, cancel_url):
        """Crea un intento de pago con Stripe."""
        try:
            # Crear o recuperar cliente en Stripe
            customer_id = self._obtener_o_crear_cliente_stripe(pago.cliente)
            
            # Crear PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(float(pago.monto) * 100),  # Convertir a centavos
                currency='mxn',
                customer=customer_id,
                metadata={
                    'pago_id': str(pago.id),
                    'cliente_id': str(pago.cliente.id),
                    'concepto': pago.concepto,
                },
                description=f"Pago: {pago.concepto}",
            )
            
            # Crear Checkout Session para mejor UX
            success_url = return_url or f"{settings.SITE_URL}/pagos/pago-exitoso/?session_id={{CHECKOUT_SESSION_ID}}"
            cancel_url = cancel_url or f"{settings.SITE_URL}/pagos/pago-cancelado/"
            
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'mxn',
                        'product_data': {
                            'name': pago.concepto,
                            'description': f"Pago para {pago.cliente.nombre_completo}",
                        },
                        'unit_amount': int(float(pago.monto) * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'pago_id': str(pago.id),
                    'cliente_id': str(pago.cliente.id),
                },
            )
            
            # Guardar transacción
            transaccion = TransaccionPago.objects.create(
                pago=pago,
                pasarela='stripe',
                estado='pendiente',
                id_transaccion_pasarela=session.id,
                id_pago_intento=intent.id,
                monto=pago.monto,
                moneda='MXN',
                datos_respuesta={
                    'session_id': session.id,
                    'payment_intent_id': intent.id,
                    'url': session.url,
                }
            )
            
            return {
                'success': True,
                'session_id': session.id,
                'url': session.url,
                'transaccion_id': transaccion.id,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error de Stripe: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def _obtener_o_crear_cliente_stripe(self, cliente):
        """Obtiene o crea un cliente en Stripe."""
        # Buscar si el cliente ya tiene un ID de Stripe guardado
        # Por ahora, creamos uno nuevo cada vez (se puede optimizar guardando el ID)
        try:
            customer = stripe.Customer.create(
                email=cliente.email if hasattr(cliente, 'email') and cliente.email else None,
                name=cliente.nombre_completo,
                metadata={
                    'cliente_id': str(cliente.id),
                }
            )
            return customer.id
        except Exception as e:
            logger.error(f"Error al crear cliente en Stripe: {str(e)}")
            raise
    
    def verificar_pago(self, session_id):
        """
        Verifica el estado de un pago usando el session_id.
        
        Args:
            session_id: ID de la sesión de checkout
        
        Returns:
            dict: Estado del pago
        """
        if self.pasarela == 'stripe':
            return self._verificar_pago_stripe(session_id)
        else:
            raise ValueError(f"Pasarela {self.pasarela} no soportada")
    
    def _verificar_pago_stripe(self, session_id):
        """Verifica el estado de un pago con Stripe."""
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Buscar la transacción
            try:
                transaccion = TransaccionPago.objects.get(id_transaccion_pasarela=session_id)
            except TransaccionPago.DoesNotExist:
                return {
                    'success': False,
                    'error': 'Transacción no encontrada',
                }
            
            # Actualizar estado según la sesión
            if session.payment_status == 'paid':
                transaccion.estado = 'completada'
                transaccion.fecha_completada = timezone.now()
                transaccion.datos_respuesta = {
                    'session': session.to_dict(),
                }
                transaccion.save()
                
                # Marcar el pago como pagado
                transaccion.marcar_como_completada()
                
                return {
                    'success': True,
                    'estado': 'completada',
                    'pago_id': transaccion.pago.id,
                }
            elif session.payment_status == 'unpaid':
                transaccion.estado = 'pendiente'
                transaccion.save()
                return {
                    'success': True,
                    'estado': 'pendiente',
                }
            else:
                return {
                    'success': True,
                    'estado': session.payment_status,
                }
                
        except stripe.error.StripeError as e:
            logger.error(f"Error de Stripe al verificar pago: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
        except Exception as e:
            logger.error(f"Error inesperado al verificar pago: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def procesar_webhook(self, payload, signature):
        """
        Procesa un webhook de la pasarela.
        
        Args:
            payload: Cuerpo del webhook
            signature: Firma del webhook
        
        Returns:
            dict: Resultado del procesamiento
        """
        if self.pasarela == 'stripe':
            return self._procesar_webhook_stripe(payload, signature)
        else:
            raise ValueError(f"Pasarela {self.pasarela} no soportada")
    
    def _procesar_webhook_stripe(self, payload, signature):
        """Procesa un webhook de Stripe."""
        try:
            webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
            if not webhook_secret:
                logger.warning("STRIPE_WEBHOOK_SECRET no configurada")
                return {'success': False, 'error': 'Webhook secret no configurado'}
            
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            # Procesar diferentes tipos de eventos
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                return self._procesar_checkout_completado(session)
            elif event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                return self._procesar_pago_exitoso(payment_intent)
            elif event['type'] == 'payment_intent.payment_failed':
                payment_intent = event['data']['object']
                return self._procesar_pago_fallido(payment_intent)
            else:
                logger.info(f"Evento de Stripe no procesado: {event['type']}")
                return {'success': True, 'message': 'Evento no procesado'}
                
        except ValueError as e:
            logger.error(f"Payload inválido: {str(e)}")
            return {'success': False, 'error': 'Payload inválido'}
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Firma inválida: {str(e)}")
            return {'success': False, 'error': 'Firma inválida'}
        except Exception as e:
            logger.error(f"Error al procesar webhook: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _procesar_checkout_completado(self, session):
        """Procesa un checkout completado."""
        try:
            transaccion = TransaccionPago.objects.get(
                id_transaccion_pasarela=session['id']
            )
            transaccion.marcar_como_completada()
            return {'success': True, 'transaccion_id': transaccion.id}
        except TransaccionPago.DoesNotExist:
            logger.error(f"Transacción no encontrada para session {session['id']}")
            return {'success': False, 'error': 'Transacción no encontrada'}
    
    def _procesar_pago_exitoso(self, payment_intent):
        """Procesa un pago exitoso."""
        try:
            transaccion = TransaccionPago.objects.get(
                id_pago_intento=payment_intent['id']
            )
            transaccion.marcar_como_completada()
            return {'success': True, 'transaccion_id': transaccion.id}
        except TransaccionPago.DoesNotExist:
            logger.error(f"Transacción no encontrada para payment_intent {payment_intent['id']}")
            return {'success': False, 'error': 'Transacción no encontrada'}
    
    def _procesar_pago_fallido(self, payment_intent):
        """Procesa un pago fallido."""
        try:
            transaccion = TransaccionPago.objects.get(
                id_pago_intento=payment_intent['id']
            )
            transaccion.marcar_como_fallida(
                mensaje_error=payment_intent.get('last_payment_error', {}).get('message', 'Pago fallido')
            )
            return {'success': True, 'transaccion_id': transaccion.id}
        except TransaccionPago.DoesNotExist:
            logger.error(f"Transacción no encontrada para payment_intent {payment_intent['id']}")
            return {'success': False, 'error': 'Transacción no encontrada'}
    
    def _crear_intento_mercadopago(self, pago, return_url, cancel_url):
        """Crea un intento de pago con Mercado Pago."""
        try:
            base_url = settings.SITE_URL
            success_url = return_url or f"{base_url}/pagos/{pago.pk}/pago-exitoso/?payment_id={{payment_id}}"
            failure_url = cancel_url or f"{base_url}/pagos/{pago.pk}/pago-cancelado/"
            pending_url = f"{base_url}/pagos/{pago.pk}/pago-exitoso/?payment_id={{payment_id}}"
            
            preference_data = {
                "items": [
                    {
                        "title": pago.concepto,
                        "description": f"Pago para {pago.cliente.nombre_completo}",
                        "quantity": 1,
                        "unit_price": float(pago.monto),
                        "currency_id": "MXN"
                    }
                ],
                "payer": {
                    "name": pago.cliente.nombre_completo,
                    "email": pago.cliente.email if pago.cliente.email else None,
                    "phone": {
                        "number": pago.cliente.telefono
                    }
                },
                "back_urls": {
                    "success": success_url,
                    "failure": failure_url,
                    "pending": pending_url
                },
                "auto_return": "approved",
                "external_reference": str(pago.id),
                "notification_url": f"{base_url}/pagos/webhook/mercadopago/",
                "statement_descriptor": "AdminiRed"
            }
            
            preference_response = self.mp.preference().create(preference_data)
            
            if preference_response["status"] == 201:
                preference = preference_response["response"]
                
                # Guardar transacción
                transaccion = TransaccionPago.objects.create(
                    pago=pago,
                    pasarela='mercadopago',
                    estado='pendiente',
                    id_transaccion_pasarela=preference["id"],
                    monto=pago.monto,
                    moneda='MXN',
                    datos_respuesta=preference
                )
                
                return {
                    'success': True,
                    'preference_id': preference["id"],
                    'url': preference["init_point"],
                    'transaccion_id': transaccion.id,
                }
            else:
                error_msg = preference_response.get("message", "Error desconocido")
                logger.error(f"Error de Mercado Pago: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                }
                
        except Exception as e:
            logger.error(f"Error inesperado en Mercado Pago: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def _crear_intento_paypal(self, pago, return_url, cancel_url):
        """Crea un intento de pago con PayPal."""
        try:
            base_url = settings.SITE_URL
            # PayPal usa 'token' en lugar de 'paymentId' en la URL de retorno
            success_url = return_url or f"{base_url}/pagos/{pago.pk}/pago-exitoso/?token={{token}}&PayerID={{PayerID}}"
            cancel_url = cancel_url or f"{base_url}/pagos/{pago.pk}/pago-cancelado/"
            
            # Obtener access token de PayPal
            access_token = self._obtener_paypal_access_token()
            if not access_token:
                return {
                    'success': False,
                    'error': 'No se pudo obtener el access token de PayPal',
                }
            
            # Crear orden de pago
            api_url = 'https://api-m.sandbox.paypal.com' if self.paypal_mode == 'sandbox' else 'https://api-m.paypal.com'
            
            order_data = {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "reference_id": str(pago.id),
                        "description": pago.concepto,
                        "amount": {
                            "currency_code": "MXN",
                            "value": str(pago.monto)
                        }
                    }
                ],
                "application_context": {
                    "brand_name": "AdminiRed",
                    "landing_page": "BILLING",
                    "user_action": "PAY_NOW",
                    "return_url": success_url,
                    "cancel_url": cancel_url
                }
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            response = requests.post(
                f'{api_url}/v2/checkout/orders',
                json=order_data,
                headers=headers
            )
            
            if response.status_code == 201:
                order = response.json()
                
                # Guardar transacción
                transaccion = TransaccionPago.objects.create(
                    pago=pago,
                    pasarela='paypal',
                    estado='pendiente',
                    id_transaccion_pasarela=order["id"],
                    monto=pago.monto,
                    moneda='MXN',
                    datos_respuesta=order
                )
                
                # Obtener URL de aprobación
                approve_url = None
                for link in order.get("links", []):
                    if link.get("rel") == "approve":
                        approve_url = link.get("href")
                        break
                
                return {
                    'success': True,
                    'order_id': order["id"],
                    'url': approve_url,
                    'transaccion_id': transaccion.id,
                }
            else:
                error_msg = response.json().get("message", "Error desconocido")
                logger.error(f"Error de PayPal: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                }
                
        except Exception as e:
            logger.error(f"Error inesperado en PayPal: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def _obtener_paypal_access_token(self):
        """Obtiene un access token de PayPal."""
        try:
            api_url = 'https://api-m.sandbox.paypal.com' if self.paypal_mode == 'sandbox' else 'https://api-m.paypal.com'
            
            auth = (self.paypal_client_id, self.paypal_secret)
            headers = {
                'Accept': 'application/json',
                'Accept-Language': 'en_US'
            }
            data = {'grant_type': 'client_credentials'}
            
            response = requests.post(
                f'{api_url}/v1/oauth2/token',
                auth=auth,
                headers=headers,
                data=data
            )
            
            if response.status_code == 200:
                return response.json().get('access_token')
            else:
                logger.error(f"Error al obtener access token de PayPal: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error inesperado al obtener access token de PayPal: {str(e)}")
            return None
    
    def procesar_reembolso(self, transaccion, monto_parcial=None, motivo=None):
        """
        Procesa un reembolso de una transacción.
        
        Args:
            transaccion: Instancia de TransaccionPago
            monto_parcial: Monto parcial a reembolsar (None = reembolso total)
            motivo: Motivo del reembolso
        
        Returns:
            dict: Resultado del reembolso
        """
        if transaccion.estado != 'completada':
            return {
                'success': False,
                'error': 'Solo se pueden reembolsar transacciones completadas'
            }
        
        if transaccion.pasarela == 'stripe':
            return self._procesar_reembolso_stripe(transaccion, monto_parcial, motivo)
        elif transaccion.pasarela == 'mercadopago':
            return self._procesar_reembolso_mercadopago(transaccion, monto_parcial, motivo)
        elif transaccion.pasarela == 'paypal':
            return self._procesar_reembolso_paypal(transaccion, monto_parcial, motivo)
        else:
            return {
                'success': False,
                'error': f'Reembolsos no soportados para la pasarela {transaccion.pasarela}'
            }
    
    def _procesar_reembolso_stripe(self, transaccion, monto_parcial, motivo):
        """Procesa un reembolso con Stripe."""
        try:
            # Obtener el payment intent de la transacción
            payment_intent_id = transaccion.id_pago_intento or transaccion.id_transaccion_pasarela
            
            if monto_parcial:
                refund = stripe.Refund.create(
                    payment_intent=payment_intent_id,
                    amount=int(float(monto_parcial) * 100),  # Convertir a centavos
                    reason='requested_by_customer' if motivo else None,
                    metadata={
                        'transaccion_id': str(transaccion.id),
                        'pago_id': str(transaccion.pago.id),
                        'motivo': motivo or 'Reembolso solicitado'
                    }
                )
            else:
                refund = stripe.Refund.create(
                    payment_intent=payment_intent_id,
                    reason='requested_by_customer' if motivo else None,
                    metadata={
                        'transaccion_id': str(transaccion.id),
                        'pago_id': str(transaccion.pago.id),
                        'motivo': motivo or 'Reembolso total solicitado'
                    }
                )
            
            # Actualizar transacción
            transaccion.estado = 'reembolsada'
            transaccion.fecha_completada = timezone.now()
            if not transaccion.datos_respuesta:
                transaccion.datos_respuesta = {}
            transaccion.datos_respuesta['refund'] = refund.to_dict()
            transaccion.save()
            
            # Actualizar el pago
            transaccion.pago.estado = 'cancelado'
            transaccion.pago.save()
            
            return {
                'success': True,
                'refund_id': refund.id,
                'amount': refund.amount / 100,  # Convertir de centavos
                'transaccion_id': transaccion.id,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error de Stripe al procesar reembolso: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
        except Exception as e:
            logger.error(f"Error inesperado al procesar reembolso: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def _procesar_reembolso_mercadopago(self, transaccion, monto_parcial, motivo):
        """Procesa un reembolso con Mercado Pago."""
        try:
            payment_id = transaccion.id_transaccion_pasarela
            
            if monto_parcial:
                refund_data = {
                    "amount": float(monto_parcial)
                }
            else:
                refund_data = {}  # Reembolso total
            
            refund_response = self.mp.payment().refund(payment_id, refund_data)
            
            if refund_response["status"] == 201:
                refund = refund_response["response"]
                
                # Actualizar transacción
                transaccion.estado = 'reembolsada'
                transaccion.fecha_completada = timezone.now()
                if not transaccion.datos_respuesta:
                    transaccion.datos_respuesta = {}
                transaccion.datos_respuesta['refund'] = refund
                transaccion.save()
                
                # Actualizar el pago
                transaccion.pago.estado = 'cancelado'
                transaccion.pago.save()
                
                return {
                    'success': True,
                    'refund_id': refund.get("id"),
                    'amount': refund.get("amount", float(monto_parcial) if monto_parcial else float(transaccion.monto)),
                    'transaccion_id': transaccion.id,
                }
            else:
                error_msg = refund_response.get("message", "Error desconocido")
                logger.error(f"Error de Mercado Pago al procesar reembolso: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                }
                
        except Exception as e:
            logger.error(f"Error inesperado al procesar reembolso en Mercado Pago: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }
    
    def _procesar_reembolso_paypal(self, transaccion, monto_parcial, motivo):
        """Procesa un reembolso con PayPal."""
        try:
            access_token = self._obtener_paypal_access_token()
            if not access_token:
                return {
                    'success': False,
                    'error': 'No se pudo obtener el access token de PayPal',
                }
            
            # Obtener el capture_id de la orden
            order_id = transaccion.id_transaccion_pasarela
            api_url = 'https://api-m.sandbox.paypal.com' if self.paypal_mode == 'sandbox' else 'https://api-m.paypal.com'
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            # Obtener detalles de la orden para encontrar el capture_id
            order_response = requests.get(
                f'{api_url}/v2/checkout/orders/{order_id}',
                headers=headers
            )
            
            if order_response.status_code != 200:
                return {
                    'success': False,
                    'error': 'No se pudo obtener los detalles de la orden',
                }
            
            order = order_response.json()
            capture_id = None
            
            # Buscar el capture_id en las purchase_units
            for purchase_unit in order.get("purchase_units", []):
                for capture in purchase_unit.get("payments", {}).get("captures", []):
                    if capture.get("status") == "COMPLETED":
                        capture_id = capture.get("id")
                        break
                if capture_id:
                    break
            
            if not capture_id:
                return {
                    'success': False,
                    'error': 'No se encontró un pago completado para reembolsar',
                }
            
            # Crear reembolso
            refund_data = {
                "note_to_payer": motivo or "Reembolso solicitado"
            }
            
            if monto_parcial:
                refund_data["amount"] = {
                    "value": str(monto_parcial),
                    "currency_code": "MXN"
                }
            
            refund_response = requests.post(
                f'{api_url}/v2/payments/captures/{capture_id}/refund',
                json=refund_data,
                headers=headers
            )
            
            if refund_response.status_code == 201:
                refund = refund_response.json()
                
                # Actualizar transacción
                transaccion.estado = 'reembolsada'
                transaccion.fecha_completada = timezone.now()
                if not transaccion.datos_respuesta:
                    transaccion.datos_respuesta = {}
                transaccion.datos_respuesta['refund'] = refund
                transaccion.save()
                
                # Actualizar el pago
                transaccion.pago.estado = 'cancelado'
                transaccion.pago.save()
                
                return {
                    'success': True,
                    'refund_id': refund.get("id"),
                    'amount': float(refund.get("amount", {}).get("value", monto_parcial or transaccion.monto)),
                    'transaccion_id': transaccion.id,
                }
            else:
                error_msg = refund_response.json().get("message", "Error desconocido")
                logger.error(f"Error de PayPal al procesar reembolso: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                }
                
        except Exception as e:
            logger.error(f"Error inesperado al procesar reembolso en PayPal: {str(e)}")
            return {
                'success': False,
                'error': str(e),
            }

