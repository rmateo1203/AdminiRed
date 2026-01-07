def sidebar_config(request):
    """Context processor para pasar la configuración del sidebar a todas las plantillas."""
    sidebar_position = request.session.get('sidebar_position', 'left')  # 'left' o 'top'
    
    # Verificar si el usuario es un cliente
    es_cliente = False
    if request.user.is_authenticated:
        try:
            cliente = request.user.cliente_perfil
            if cliente and not cliente.is_deleted and cliente.estado_cliente == 'activo':
                es_cliente = True
        except:
            pass
    
    return {
        'sidebar_position': sidebar_position,
        'es_cliente': es_cliente,
    }


def sistema_config(request):
    """Context processor para pasar la configuración del sistema a todas las plantillas."""
    from .models import ConfiguracionSistema
    return {
        'sistema_config': ConfiguracionSistema.get_activa(),
    }

