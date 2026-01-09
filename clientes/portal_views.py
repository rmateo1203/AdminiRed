"""
Vistas para el portal de clientes.
Los clientes pueden acceder solo a sus propios pagos y servicios activos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
from .models import Cliente
from pagos.models import Pago, TransaccionPago
from instalaciones.models import Instalacion
# from .forms import ClienteForm  # No necesario para el portal
from django.contrib.auth import get_user_model

User = get_user_model()


def es_cliente(user):
    """Verifica si el usuario es un cliente (tiene perfil de cliente)."""
    if not user.is_authenticated:
        return False
    return hasattr(user, 'cliente_perfil') and user.cliente_perfil is not None


def obtener_cliente_desde_usuario(user):
    """Obtiene el cliente asociado a un usuario."""
    if not user.is_authenticated:
        return None
    try:
        return user.cliente_perfil
    except:
        return None


from functools import wraps

def cliente_required(view_func):
    """Decorador para verificar que el usuario es un cliente."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('clientes:portal_login')
        
        cliente = obtener_cliente_desde_usuario(request.user)
        if not cliente:
            messages.error(request, 'No tienes acceso al portal de clientes.')
            return redirect('clientes:portal_login')
        
        if cliente.is_deleted or cliente.estado_cliente != 'activo':
            messages.error(request, 'Tu cuenta de cliente no está activa.')
            return redirect('clientes:portal_login')
        
        # Verificar si debe cambiar la contraseña
        # Permitir acceso solo a la página de cambiar contraseña si debe_cambiar_password es True
        if cliente.debe_cambiar_password:
            # Si ya está en la página de cambiar contraseña, permitir acceso
            if request.resolver_match.url_name != 'portal_cambiar_password':
                messages.warning(request, 'Por seguridad, debes cambiar tu contraseña antes de continuar.')
                return redirect('clientes:portal_cambiar_password')
        
        # Agregar cliente al contexto
        kwargs['cliente'] = cliente
        return view_func(request, *args, **kwargs)
    
    return wrapper


def portal_registro(request):
    """Vista de registro para clientes."""
    if request.user.is_authenticated and es_cliente(request.user):
        return redirect('clientes:portal_mis_pagos')
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre', '').strip()
        apellido1 = request.POST.get('apellido1', '').strip()
        apellido2 = request.POST.get('apellido2', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()
        estado = request.POST.get('estado', '').strip()
        codigo_postal = request.POST.get('codigo_postal', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # Validaciones básicas
        errores = {}
        
        if not nombre:
            errores['nombre'] = 'El nombre es requerido.'
        if not apellido1:
            errores['apellido1'] = 'El primer apellido es requerido.'
        if not email:
            errores['email'] = 'El correo electrónico es requerido.'
        elif Cliente.objects.filter(email=email, is_deleted=False).exists():
            errores['email'] = 'Este correo electrónico ya está registrado.'
        if not telefono:
            errores['telefono'] = 'El teléfono es requerido.'
        elif Cliente.objects.filter(telefono=telefono, is_deleted=False).exists():
            errores['telefono'] = 'Este teléfono ya está registrado.'
        if not password:
            errores['password'] = 'La contraseña es requerida.'
        elif len(password) < 8:
            errores['password'] = 'La contraseña debe tener al menos 8 caracteres.'
        elif password != password_confirm:
            errores['password_confirm'] = 'Las contraseñas no coinciden.'
        if not direccion:
            errores['direccion'] = 'La dirección es requerida.'
        if not ciudad:
            errores['ciudad'] = 'La ciudad es requerida.'
        if not estado:
            errores['estado'] = 'El estado es requerido.'
        
        if errores:
            context = {
                'errores': errores,
                'form_data': request.POST,
            }
            return render(request, 'clientes/portal_registro.html', context)
        
        # Crear cliente
        try:
            cliente = Cliente.objects.create(
                nombre=nombre,
                apellido1=apellido1,
                apellido2=apellido2 if apellido2 else None,
                email=email,
                telefono=telefono,
                direccion=direccion,
                ciudad=ciudad,
                estado=estado,
                codigo_postal=codigo_postal if codigo_postal else None,
                estado_cliente='activo'
            )
            
            # Crear usuario para el portal (no enviar email porque el cliente ya tiene la contraseña)
            usuario = cliente.crear_usuario_portal(password=password, enviar_email=False)
            
            # Iniciar sesión automáticamente
            user = authenticate(request, username=usuario.username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {cliente.nombre_completo}! Tu cuenta ha sido creada exitosamente.')
                return redirect('clientes:portal_mis_pagos')
            else:
                messages.success(request, 'Tu cuenta ha sido creada. Por favor, inicia sesión.')
                return redirect('clientes:portal_login')
                
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
            context = {
                'errores': {'general': 'Error al crear la cuenta. Por favor, intenta nuevamente.'},
                'form_data': request.POST,
            }
            return render(request, 'clientes/portal_registro.html', context)
    
    return render(request, 'clientes/portal_registro.html')


def portal_login(request):
    """Vista de login para clientes."""
    if request.user.is_authenticated and es_cliente(request.user):
        return redirect('clientes:portal_mis_pagos')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Por favor, completa todos los campos.')
            return render(request, 'clientes/portal_login.html')
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar que sea un cliente
            cliente = obtener_cliente_desde_usuario(user)
            if cliente:
                if cliente.is_deleted:
                    messages.error(request, 'Tu cuenta ha sido desactivada.')
                elif cliente.estado_cliente != 'activo':
                    messages.error(request, f'Tu cuenta está {cliente.get_estado_cliente_display().lower()}.')
                else:
                    login(request, user)
                    messages.success(request, f'¡Bienvenido, {cliente.nombre_completo}!')
                    next_url = request.GET.get('next', 'clientes:portal_mis_pagos')
                    return redirect(next_url)
            else:
                messages.error(request, 'No tienes acceso al portal de clientes.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'clientes/portal_login.html')


@login_required
@cliente_required
def portal_dashboard(request, cliente):
    """Dashboard del portal de cliente - Muestra estadísticas y lista de pagos."""
    # Obtener instalaciones del cliente para el sidebar (solo las del cliente autenticado)
    instalaciones = Instalacion.objects.filter(cliente=cliente).select_related('plan', 'tipo_instalacion').order_by('-fecha_activacion')[:10]
    
    # Obtener pagos del cliente (solo los pagos que pertenecen a este cliente)
    # También verificar que si el pago tiene instalación, esa instalación pertenezca al cliente
    pagos = Pago.objects.filter(cliente=cliente).select_related('instalacion').order_by('-fecha_vencimiento')
    
    # Filtrar pagos para asegurar que las instalaciones asociadas pertenezcan al cliente
    pagos = pagos.filter(
        Q(instalacion__isnull=True) | Q(instalacion__cliente=cliente)
    )
    
    # Estadísticas
    total_pagos = pagos.count()
    pagos_pendientes = pagos.filter(estado='pendiente').count()
    pagos_vencidos = pagos.filter(estado='vencido').count()
    pagos_pagados = pagos.filter(estado='pagado').count()
    monto_pendiente = pagos.filter(estado__in=['pendiente', 'vencido']).aggregate(Sum('monto'))['monto__sum'] or 0
    
    # Filtros
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        pagos = pagos.filter(estado=estado_filter)
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        pagos = pagos.filter(
            Q(concepto__icontains=query) |
            Q(referencia_pago__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(pagos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cliente': cliente,
        'instalaciones': instalaciones,  # Para el sidebar
        'page_obj': page_obj,
        'pagos': page_obj,
        'query': query,
        'estado_filter': estado_filter,
        'estados': Pago.ESTADO_CHOICES,
        'total_pagos': total_pagos,
        'pagos_pendientes': pagos_pendientes,
        'pagos_vencidos': pagos_vencidos,
        'pagos_pagados': pagos_pagados,
        'monto_pendiente': monto_pendiente,
    }
    
    return render(request, 'clientes/portal_dashboard.html', context)


@login_required
@cliente_required
def portal_mis_pagos(request, cliente):
    """Lista de pagos del cliente."""
    # Obtener instalaciones del cliente para el sidebar (solo las del cliente autenticado)
    instalaciones = Instalacion.objects.filter(cliente=cliente).select_related('plan', 'tipo_instalacion').order_by('-fecha_activacion')[:10]
    
    # Obtener todos los pagos del cliente (solo los pagos que pertenecen a este cliente)
    # También verificar que si el pago tiene instalación, esa instalación pertenezca al cliente
    todos_los_pagos = Pago.objects.filter(cliente=cliente).select_related('instalacion')
    
    # Filtrar pagos para asegurar que las instalaciones asociadas pertenezcan al cliente
    todos_los_pagos = todos_los_pagos.filter(
        Q(instalacion__isnull=True) | Q(instalacion__cliente=cliente)
    )
    
    # Estadísticas generales (antes de aplicar filtros)
    total_pagos = todos_los_pagos.count()
    pagos_pendientes = todos_los_pagos.filter(estado='pendiente').count()
    pagos_vencidos = todos_los_pagos.filter(estado='vencido').count()
    pagos_pagados = todos_los_pagos.filter(estado='pagado').count()
    monto_pendiente = todos_los_pagos.filter(estado__in=['pendiente', 'vencido']).aggregate(Sum('monto'))['monto__sum'] or 0
    monto_vencido = todos_los_pagos.filter(estado='vencido').aggregate(Sum('monto'))['monto__sum'] or 0
    
    # Próximos vencimientos (próximos 7 días)
    hoy = timezone.now().date()
    proximos_7_dias = hoy + timedelta(days=7)
    proximos_vencimientos = todos_los_pagos.filter(
        estado__in=['pendiente'],
        fecha_vencimiento__gte=hoy,
        fecha_vencimiento__lte=proximos_7_dias
    ).order_by('fecha_vencimiento')[:5]
    
    # Filtros
    estado_filter = request.GET.get('estado', '')
    if estado_filter:
        todos_los_pagos = todos_los_pagos.filter(estado=estado_filter)
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        todos_los_pagos = todos_los_pagos.filter(
            Q(concepto__icontains=query) |
            Q(referencia_pago__icontains=query)
        )
    
    # Ordenar por fecha de vencimiento (más próximos primero)
    pagos = todos_los_pagos.order_by('-fecha_vencimiento')
    
    # Paginación
    paginator = Paginator(pagos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calcular días hasta vencimiento para cada pago
    pagos_con_dias = []
    for pago in page_obj:
        dias_restantes = None
        dias_vencido = None
        
        # Calcular diferencia de días
        delta = hoy - pago.fecha_vencimiento
        dias_transcurridos = delta.days
        
        if pago.estado == 'vencido':
            # Si está vencido, calcular días vencidos
            dias_vencido = dias_transcurridos
        elif pago.estado == 'pendiente':
            # Si está pendiente, verificar si ya venció o cuántos días faltan
            if dias_transcurridos > 0:
                dias_vencido = dias_transcurridos
            else:
                dias_restantes = abs(dias_transcurridos)
        
        pagos_con_dias.append({
            'pago': pago,
            'dias_restantes': dias_restantes,
            'dias_vencido': dias_vencido
        })
    
    context = {
        'cliente': cliente,
        'instalaciones': instalaciones,  # Para el sidebar
        'page_obj': page_obj,
        'pagos': page_obj,
        'pagos_con_dias': pagos_con_dias,  # Pagos con información de días
        'query': query,
        'estado_filter': estado_filter,
        'estados': Pago.ESTADO_CHOICES,
        # Estadísticas
        'total_pagos': total_pagos,
        'pagos_pendientes': pagos_pendientes,
        'pagos_vencidos': pagos_vencidos,
        'pagos_pagados': pagos_pagados,
        'monto_pendiente': monto_pendiente,
        'monto_vencido': monto_vencido,
        'proximos_vencimientos': proximos_vencimientos,
        'hoy': hoy,
    }
    
    return render(request, 'clientes/portal_mis_pagos.html', context)


@login_required
@cliente_required
def portal_detalle_pago(request, cliente, pago_id):
    """Detalle de un pago específico del cliente."""
    # Obtener instalaciones del cliente para el sidebar (solo las del cliente autenticado)
    instalaciones = Instalacion.objects.filter(cliente=cliente).select_related('plan', 'tipo_instalacion').order_by('-fecha_activacion')[:10]
    
    # Obtener el pago y verificar que pertenezca al cliente
    # También verificar que si tiene instalación, esa instalación pertenezca al cliente
    pago = get_object_or_404(
        Pago.objects.filter(
            cliente=cliente
        ).filter(
            Q(instalacion__isnull=True) | Q(instalacion__cliente=cliente)
        ),
        pk=pago_id
    )
    
    # Obtener transacciones relacionadas
    transacciones = pago.transacciones.all().order_by('-fecha_creacion')
    
    # Verificar si hay pasarelas disponibles
    from django.conf import settings
    tiene_pasarela = (
        bool(getattr(settings, 'STRIPE_SECRET_KEY', None)) or
        bool(getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', None)) or
        (bool(getattr(settings, 'PAYPAL_CLIENT_ID', None)) and bool(getattr(settings, 'PAYPAL_SECRET', None)))
    )
    
    context = {
        'cliente': cliente,
        'instalaciones': instalaciones,  # Para el sidebar
        'pago': pago,
        'transacciones': transacciones,
        'tiene_pasarela': tiene_pasarela,
    }
    
    return render(request, 'clientes/portal_detalle_pago.html', context)


@login_required
@cliente_required
def portal_detalle_pago_modal(request, cliente, pago_id):
    """Vista AJAX para obtener el detalle de un pago en formato JSON (para modal)."""
    from django.http import JsonResponse
    
    # Obtener el pago y verificar que pertenezca al cliente
    try:
        pago = Pago.objects.filter(
            cliente=cliente
        ).filter(
            Q(instalacion__isnull=True) | Q(instalacion__cliente=cliente)
        ).get(pk=pago_id)
    except Pago.DoesNotExist:
        return JsonResponse({'error': 'Pago no encontrado'}, status=404)
    
    # Obtener transacciones relacionadas
    transacciones = []
    for trans in pago.transacciones.all().order_by('-fecha_creacion'):
        transacciones.append({
            'fecha_creacion': trans.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
            'pasarela': trans.get_pasarela_display(),
            'estado': trans.estado,
            'estado_display': trans.get_estado_display(),
            'monto': str(trans.monto),
        })
    
    # Verificar si hay pasarelas disponibles
    from django.conf import settings
    tiene_pasarela = (
        bool(getattr(settings, 'STRIPE_SECRET_KEY', None)) or
        bool(getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', None)) or
        (bool(getattr(settings, 'PAYPAL_CLIENT_ID', None)) and bool(getattr(settings, 'PAYPAL_SECRET', None)))
    )
    
    data = {
        'id': pago.id,
        'concepto': pago.concepto,
        'monto': str(pago.monto),
        'estado': pago.estado,
        'estado_display': pago.get_estado_display(),
        'fecha_vencimiento': pago.fecha_vencimiento.strftime('%d/%m/%Y'),
        'fecha_pago': pago.fecha_pago.strftime('%d/%m/%Y %H:%M') if pago.fecha_pago else None,
        'periodo_mes': pago.get_periodo_mes_display(),
        'periodo_anio': pago.periodo_anio,
        'metodo_pago': pago.get_metodo_pago_display() if pago.metodo_pago else None,
        'referencia_pago': pago.referencia_pago,
        'instalacion': pago.instalacion.plan_nombre if pago.instalacion else None,
        'cliente': pago.cliente.nombre_completo,
        'transacciones': transacciones,
        'tiene_pasarela': tiene_pasarela,
        'puede_pagar': (pago.estado == 'pendiente' or pago.estado == 'vencido') and tiene_pasarela and pago.estado != 'pagado',
    }
    
    return JsonResponse(data)


@login_required
@cliente_required
def portal_mis_servicios(request, cliente):
    """Lista de servicios/instalaciones del cliente - Acceso denegado."""
    messages.warning(request, 'No tienes acceso a esta sección. Solo puedes ver tus pagos.')
    return redirect('clientes:portal_mis_pagos')


@login_required
@cliente_required
def portal_perfil(request, cliente):
    """Perfil del cliente - Acceso denegado."""
    messages.warning(request, 'No tienes acceso a esta sección. Solo puedes ver tus pagos.')
    return redirect('clientes:portal_mis_pagos')


@login_required
def portal_cambiar_password(request):
    """Cambiar contraseña del cliente."""
    # Obtener el cliente del usuario autenticado
    cliente = obtener_cliente_desde_usuario(request.user)
    if not cliente:
        messages.error(request, 'No tienes acceso al portal de clientes.')
        return redirect('clientes:portal_login')
    
    if cliente.is_deleted or cliente.estado_cliente != 'activo':
        messages.error(request, 'Tu cuenta de cliente no está activa.')
        return redirect('clientes:portal_login')
    
    es_obligatorio = cliente.debe_cambiar_password
    
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirm = request.POST.get('password_confirm')
        
        # Validar que todos los campos estén presentes
        if not all([password_actual, password_nueva, password_confirm]):
            messages.error(request, 'Todos los campos son requeridos.')
        else:
            # Verificar contraseña actual
            user = request.user
            if not user.check_password(password_actual):
                messages.error(request, 'La contraseña actual es incorrecta.')
            # Verificar que las nuevas contraseñas coincidan
            elif password_nueva != password_confirm:
                messages.error(request, 'Las nuevas contraseñas no coinciden.')
            # Verificar que la nueva contraseña sea diferente a la actual
            elif user.check_password(password_nueva):
                messages.error(request, 'La nueva contraseña debe ser diferente a la contraseña actual.')
            # Validar longitud mínima
            elif len(password_nueva) < 8:
                messages.error(request, 'La nueva contraseña debe tener al menos 8 caracteres.')
            else:
                # Cambiar la contraseña
                user.set_password(password_nueva)
                user.save()
                
                # Actualizar el flag de cambio de contraseña
                cliente.debe_cambiar_password = False
                cliente.save()
                
                # Actualizar la sesión para mantener al usuario autenticado
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)
                
                messages.success(request, '¡Tu contraseña ha sido cambiada exitosamente!')
                if es_obligatorio:
                    return redirect('clientes:portal_mis_pagos')
                else:
                    return redirect('clientes:portal_mis_pagos')
    
    context = {
        'cliente': cliente,
        'es_obligatorio': es_obligatorio,
    }
    return render(request, 'clientes/portal_cambiar_password.html', context)

