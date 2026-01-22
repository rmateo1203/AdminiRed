"""
Comando de gestión para actualizar automáticamente los pagos vencidos.

Este comando marca como 'vencido' todos los pagos que:
- Tienen estado 'pendiente'
- Su fecha_vencimiento ya pasó

Uso:
    python manage.py actualizar_pagos_vencidos
    
Este comando se puede ejecutar periódicamente mediante un cron job o tarea programada.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from pagos.models import Pago


class Command(BaseCommand):
    help = 'Actualiza automáticamente los pagos pendientes a estado vencido si su fecha de vencimiento ya pasó'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular la actualización sin modificar la base de datos',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Actualizando Pagos Vencidos'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('[MODO SIMULACIÓN - No se modificarán datos]'))
        
        # Actualizar pagos vencidos
        if dry_run:
            hoy = timezone.now().date()
            pagos_vencidos = Pago.objects.filter(
                estado='pendiente',
                fecha_vencimiento__lt=hoy
            )
            cantidad = pagos_vencidos.count()
            self.stdout.write(
                self.style.WARNING(
                    f'[SIMULACIÓN] Se marcarían {cantidad} pago(s) como vencido(s)'
                )
            )
            
            if cantidad > 0:
                self.stdout.write('\nPagos que se marcarían como vencidos:')
                for pago in pagos_vencidos[:20]:  # Mostrar máximo 20
                    dias_vencido = (hoy - pago.fecha_vencimiento).days
                    self.stdout.write(
                        f'  • {pago.cliente.nombre_completo} - ${pago.monto} - '
                        f'Vencido hace {dias_vencido} día(s) - {pago.fecha_vencimiento}'
                    )
                if cantidad > 20:
                    self.stdout.write(f'  ... y {cantidad - 20} más')
        else:
            cantidad = Pago.actualizar_pagos_vencidos()
            
            if cantidad > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Se actualizaron {cantidad} pago(s) a estado vencido.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('✅ No hay pagos pendientes que actualizar.')
                )
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
