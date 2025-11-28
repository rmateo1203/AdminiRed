def sidebar_config(request):
    """Context processor para pasar la configuración del sidebar a todas las plantillas."""
    sidebar_position = request.session.get('sidebar_position', 'left')  # 'left' o 'top'
    return {
        'sidebar_position': sidebar_position,
    }

