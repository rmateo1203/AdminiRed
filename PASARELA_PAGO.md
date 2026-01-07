# Integración de Pasarela de Pago - Stripe

## Descripción

Se ha implementado una integración completa con **Stripe** como pasarela de pago para permitir que los clientes paguen sus facturas en línea de forma segura.

## Características Implementadas

### 1. Modelo de Transacciones
- **TransaccionPago**: Almacena todas las transacciones realizadas a través de la pasarela
- Registra estado, monto, IDs de transacción, y datos completos de respuesta
- Soporta múltiples pasarelas (actualmente Stripe, extensible a otras)

### 2. Servicio de Pasarela
- **PaymentGateway**: Clase que encapsula la lógica de integración
- Crea sesiones de checkout de Stripe
- Verifica el estado de los pagos
- Procesa webhooks para confirmación automática

### 3. Vistas Implementadas
- `/pagos/<id>/pagar-online/`: Inicia el proceso de pago
- `/pagos/<id>/pago-exitoso/`: Página de confirmación después del pago
- `/pagos/<id>/pago-cancelado/`: Página cuando se cancela el pago
- `/pagos/webhook/stripe/`: Endpoint para recibir webhooks de Stripe

### 4. Templates
- Botón "Pagar en Línea" en el detalle del pago (si está configurada la pasarela)
- Página de confirmación de pago exitoso
- Historial de transacciones en el detalle del pago

## Configuración

### 1. Instalar Dependencias

```bash
pip install stripe
```

Ya está agregado en `requirements.txt`.

### 2. Configurar Variables de Entorno

Agrega las siguientes variables a tu archivo `.env`:

```env
# Stripe - Claves de API
STRIPE_SECRET_KEY=sk_test_...  # Clave secreta de Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...  # Clave pública (para frontend si se necesita)
STRIPE_WEBHOOK_SECRET=whsec_...  # Secreto del webhook

# URL del sitio (para webhooks y redirects)
SITE_URL=http://localhost:8000  # En producción: https://tu-dominio.com
```

### 3. Obtener Claves de Stripe

1. Crea una cuenta en [Stripe](https://stripe.com)
2. Ve al Dashboard → Developers → API keys
3. Copia las claves de prueba (Test mode) o producción (Live mode)
4. Para webhooks:
   - Ve a Developers → Webhooks
   - Agrega endpoint: `https://tu-dominio.com/pagos/webhook/stripe/`
   - Copia el "Signing secret"

### 4. Aplicar Migraciones

```bash
python manage.py migrate pagos
```

## Uso

### Para Clientes

1. El cliente accede al detalle de un pago pendiente
2. Ve el botón "Pagar en Línea" (si la pasarela está configurada)
3. Al hacer clic, es redirigido a Stripe Checkout
4. Completa el pago con tarjeta
5. Es redirigido de vuelta con confirmación

### Para Administradores

- Ver historial de transacciones en el detalle del pago
- Monitorear transacciones en el admin de Django
- Los pagos se marcan automáticamente como "pagado" cuando se completa la transacción

## Seguridad

- ✅ Validación de webhooks con firma
- ✅ No se almacenan datos de tarjetas (Stripe maneja todo)
- ✅ Transacciones registradas con IDs únicos
- ✅ Estados de transacción rastreables

## Extensibilidad

El sistema está diseñado para soportar múltiples pasarelas:

- **Stripe** (implementado)
- **Mercado Pago** (futuro)
- **PayPal** (futuro)
- **Conekta** (futuro)

Para agregar una nueva pasarela, extiende la clase `PaymentGateway` y agrega los métodos correspondientes.

## Notas Importantes

1. **Modo de Prueba**: Usa claves de prueba (`sk_test_...`) para desarrollo
2. **Webhooks**: Configura los webhooks en Stripe para confirmación automática
3. **HTTPS**: En producción, asegúrate de usar HTTPS para los webhooks
4. **Moneda**: Actualmente configurado para MXN (pesos mexicanos)

## Troubleshooting

### El botón "Pagar en Línea" no aparece
- Verifica que `STRIPE_SECRET_KEY` esté configurada en `.env`
- Recarga la página después de configurar

### Los pagos no se confirman automáticamente
- Verifica que el webhook esté configurado en Stripe
- Verifica que `STRIPE_WEBHOOK_SECRET` esté correcto
- Revisa los logs del servidor para errores

### Error al crear sesión de pago
- Verifica que las claves de Stripe sean válidas
- Verifica que el monto sea mayor a 0
- Revisa los logs para más detalles

