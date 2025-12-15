"""
Comando de gestión para enviar notificaciones pendientes.
Uso: python manage.py send_notifications
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from notificaciones.models import Notificacion
from notificaciones.services import NotificationService
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Envía todas las notificaciones pendientes que están listas para enviarse'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Número máximo de notificaciones a procesar (default: 50)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula el envío sin enviar realmente',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        dry_run = options['dry_run']
        
        # Obtener notificaciones pendientes que deben enviarse
        notificaciones = Notificacion.objects.filter(
            estado='pendiente'
        ).select_related('cliente', 'tipo')[:limit]
        
        total = notificaciones.count()
        
        if total == 0:
            self.stdout.write(
                self.style.SUCCESS('No hay notificaciones pendientes para enviar.')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'Procesando {total} notificación(es)...')
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('MODO DRY-RUN: No se enviarán realmente las notificaciones')
            )
        
        enviadas = 0
        fallidas = 0
        
        for notificacion in notificaciones:
            if not notificacion.debe_enviarse:
                continue
            
            self.stdout.write(
                f'Procesando: {notificacion.asunto} ({notificacion.get_canal_display()})...'
            )
            
            if dry_run:
                self.stdout.write(
                    self.style.SUCCESS(f'  [DRY-RUN] Se enviaría a: {notificacion.cliente.nombre_completo if notificacion.cliente else "General"}')
                )
                enviadas += 1
            else:
                resultado = NotificationService.send_notification(notificacion)
                
                if resultado.get('success'):
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Enviada: {resultado.get("message", "Exitoso")}')
                    )
                    enviadas += 1
                else:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Fallida: {resultado.get("error", "Error desconocido")}')
                    )
                    fallidas += 1
        
        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(
                f'Resumen: {enviadas} enviadas, {fallidas} fallidas de {total} totales'
            )
        )



