from django.core.management.base import BaseCommand
from django.utils import timezone
from pagos.models import Pago


class Command(BaseCommand):
    help = 'Marca automáticamente como vencidos todos los pagos pendientes cuya fecha de vencimiento ya pasó'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra cuántos pagos se marcarían como vencidos sin actualizarlos',
        )

    def handle(self, *args, **options):
        hoy = timezone.now().date()
        
        # Buscar pagos pendientes con fecha de vencimiento pasada
        pagos_vencidos = Pago.objects.filter(
            estado='pendiente',
            fecha_vencimiento__lt=hoy
        )
        
        cantidad = pagos_vencidos.count()
        
        if cantidad == 0:
            self.stdout.write(
                self.style.SUCCESS('✓ No hay pagos pendientes que necesiten ser marcados como vencidos.')
            )
            return
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(
                    f'[DRY RUN] Se marcarían {cantidad} pago(s) como vencido(s):'
                )
            )
            for pago in pagos_vencidos[:10]:  # Mostrar máximo 10
                dias_vencido = (hoy - pago.fecha_vencimiento).days
                self.stdout.write(
                    f'  - {pago.cliente.nombre_completo}: ${pago.monto} '
                    f'(Vencido hace {dias_vencido} día(s))'
                )
            if cantidad > 10:
                self.stdout.write(f'  ... y {cantidad - 10} más')
            return
        
        # Actualizar pagos vencidos
        actualizados = Pago.actualizar_pagos_vencidos()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Se marcaron {actualizados} pago(s) como vencido(s) automáticamente.'
            )
        )

