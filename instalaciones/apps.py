from django.apps import AppConfig


class InstalacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instalaciones'
    
    def ready(self):
        """Importa las señales cuando la app está lista."""
        import instalaciones.signals  # noqa