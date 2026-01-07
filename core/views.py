from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db.models import Count, Q, F
from django.utils import timezone
from datetime import timedelta
from clientes.models import Cliente
from instalaciones.models import Instalacion
from pagos.models import Pago
from inventario.models import Material
from notificaciones.models import Notificacion


class CustomLoginView(LoginView):
    """Vista personalizada de login que redirige a clientes al portal."""
    
    def form_valid(self, form):
        """Redirige según el tipo de usuario después del login."""
        # Autenticar al usuario
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            
            # Verificar si es un cliente
            try:
                cliente = user.cliente_perfil
                if cliente and not cliente.is_deleted and cliente.estado_cliente == 'activo':
                    # Redirigir al portal de clientes
                    messages.success(self.request, f'¡Bienvenido, {cliente.nombre_completo}!')
                    return redirect('clientes:portal_mis_pagos')
            except:
                pass  # No es un cliente, continuar con redirección normal
        
        # Para usuarios normales (staff), usar la redirección por defecto
        return super().form_valid(form)


def home(request):
    """Vista para la página de inicio con estadísticas del sistema."""
    
    # Si el usuario es un cliente, redirigir al portal de clientes
    if request.user.is_authenticated:
        try:
            cliente = request.user.cliente_perfil
            if cliente and not cliente.is_deleted and cliente.estado_cliente == 'activo':
                return redirect('clientes:portal_mis_pagos')
        except:
            pass  # No es un cliente, continuar normalmente
    
    # Estadísticas de clientes
    total_clientes = Cliente.objects.count()
    clientes_activos = Cliente.objects.filter(estado_cliente='activo').count()
    clientes_nuevos_mes = Cliente.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Estadísticas de instalaciones
    total_instalaciones = Instalacion.objects.count()
    instalaciones_activas = Instalacion.objects.filter(estado='activa').count()
    instalaciones_pendientes = Instalacion.objects.filter(estado='pendiente').count()
    instalaciones_programadas = Instalacion.objects.filter(estado='programada').count()
    
    # Estadísticas de pagos
    total_pagos = Pago.objects.count()
    pagos_pendientes = Pago.objects.filter(estado='pendiente').count()
    pagos_vencidos = Pago.objects.filter(estado='vencido').count()
    
    # Estadísticas de inventario
    total_materiales = Material.objects.count()
    materiales_bajo_stock = Material.objects.filter(
        stock_actual__lte=F('stock_minimo')
    ).count()
    materiales_agotados = Material.objects.filter(estado='agotado').count()
    
    # Estadísticas de notificaciones
    notificaciones_pendientes = Notificacion.objects.filter(estado='pendiente').count()
    notificaciones_hoy = Notificacion.objects.filter(
        fecha_creacion__date=timezone.now().date()
    ).count()
    
    # Próximos pagos a vencer (próximos 7 días)
    fecha_limite = timezone.now().date() + timedelta(days=7)
    proximos_vencimientos = Pago.objects.filter(
        estado__in=['pendiente', 'vencido'],
        fecha_vencimiento__lte=fecha_limite,
        fecha_vencimiento__gte=timezone.now().date()
    ).order_by('fecha_vencimiento')[:5]
    
    # Instalaciones recientes
    instalaciones_recientes = Instalacion.objects.order_by('-fecha_solicitud')[:5]
    
    context = {
        # Clientes
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'clientes_nuevos_mes': clientes_nuevos_mes,
        
        # Instalaciones
        'total_instalaciones': total_instalaciones,
        'instalaciones_activas': instalaciones_activas,
        'instalaciones_pendientes': instalaciones_pendientes,
        'instalaciones_programadas': instalaciones_programadas,
        
        # Pagos
        'total_pagos': total_pagos,
        'pagos_pendientes': pagos_pendientes,
        'pagos_vencidos': pagos_vencidos,
        
        # Inventario
        'total_materiales': total_materiales,
        'materiales_bajo_stock': materiales_bajo_stock,
        'materiales_agotados': materiales_agotados,
        
        # Notificaciones
        'notificaciones_pendientes': notificaciones_pendientes,
        'notificaciones_hoy': notificaciones_hoy,
        
        # Listas
        'proximos_vencimientos': proximos_vencimientos,
        'instalaciones_recientes': instalaciones_recientes,
    }
    
    return render(request, 'core/home.html', context)


@login_required
def logout_view(request):
    """Vista personalizada para cerrar sesión."""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


def toggle_sidebar(request):
    """Cambia la posición del sidebar entre izquierdo y superior."""
    current_position = request.session.get('sidebar_position', 'left')
    new_position = 'top' if current_position == 'left' else 'left'
    request.session['sidebar_position'] = new_position
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def config_sidebar(request):
    """Vista para configurar la posición del sidebar."""
    if request.method == 'POST':
        position = request.POST.get('sidebar_position', 'left')
        if position in ['left', 'top']:
            request.session['sidebar_position'] = position
            messages.success(request, f'Posición del menú cambiada a: {"Izquierdo" if position == "left" else "Superior"}.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    current_position = request.session.get('sidebar_position', 'left')
    context = {
        'current_position': current_position,
    }
    return render(request, 'core/config_sidebar.html', context)


@login_required
def configurar_sistema(request):
    """Vista para configurar el sistema (logo, colores, nombre de empresa)."""
    from .models import ConfiguracionSistema
    from .forms import ConfiguracionSistemaForm
    
    config = ConfiguracionSistema.get_activa()
    
    if request.method == 'POST':
        form = ConfiguracionSistemaForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración del sistema actualizada exitosamente.')
            return redirect('core:configurar_sistema')
    else:
        form = ConfiguracionSistemaForm(instance=config)
    
    context = {
        'form': form,
        'config': config,
    }
    
    return render(request, 'core/configurar_sistema.html', context)
