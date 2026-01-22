"""
Comando de gestión para generar pagos automáticamente desde PlanPago activos.

Uso:
    python manage.py generar_pagos
    python manage.py generar_pagos --mes 12 --anio 2024
    python manage.py generar_pagos --solo-pendientes
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from calendar import monthrange
from pagos.models import Pago, PlanPago
from instalaciones.models import Instalacion


class Command(BaseCommand):
    help = 'Genera pagos automáticamente desde los PlanPago activos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mes',
            type=int,
            help='Mes para generar pagos (1-12). Por defecto, mes actual.',
        )
        parser.add_argument(
            '--anio',
            type=int,
            help='Año para generar pagos. Por defecto, año actual.',
        )
        parser.add_argument(
            '--solo-pendientes',
            action='store_true',
            help='Solo generar pagos para instalaciones que no tienen pago en el período',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular la generación sin crear pagos reales',
        )

    def handle(self, *args, **options):
        # Obtener mes y año
        hoy = date.today()
        mes = options.get('mes') or hoy.month
        anio = options.get('anio') or hoy.year
        solo_pendientes = options.get('solo_pendientes', False)
        dry_run = options.get('dry_run', False)
        
        # Validar mes y año
        if mes < 1 or mes > 12:
            self.stdout.write(self.style.ERROR(f'Mes inválido: {mes}. Debe ser entre 1 y 12.'))
            return
        
        if anio < 2000 or anio > 2100:
            self.stdout.write(self.style.ERROR(f'Año inválido: {anio}. Debe ser entre 2000 y 2100.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Generando pagos para {mes}/{anio}...'))
        
        # Obtener todos los PlanPago activos
        # IMPORTANTE: Solo generar pagos para instalaciones activas
        planes_pago = PlanPago.objects.filter(
            activo=True,
            instalacion__estado='activa'  # Solo instalaciones activas
        ).select_related('instalacion', 'instalacion__cliente')
        
        if not planes_pago.exists():
            self.stdout.write(self.style.WARNING('No hay PlanPago activos para instalaciones activas.'))
            return
        
        pagos_creados = 0
        pagos_existentes = 0
        errores = 0
        
        for plan_pago in planes_pago:
            instalacion = plan_pago.instalacion
            cliente = instalacion.cliente
            
            # Verificar si ya existe un pago para este período
            if solo_pendientes:
                pago_existente = Pago.objects.filter(
                    cliente=cliente,
                    instalacion=instalacion,
                    periodo_mes=mes,
                    periodo_anio=anio
                ).exists()
                
                if pago_existente:
                    pagos_existentes += 1
                    continue
            
            # Calcular fecha de vencimiento
            # Usar el día de vencimiento del plan, pero ajustar si es mayor que los días del mes
            dias_en_mes = monthrange(anio, mes)[1]
            dia_vencimiento = min(plan_pago.dia_vencimiento, dias_en_mes)
            
            try:
                fecha_vencimiento = date(anio, mes, dia_vencimiento)
            except ValueError:
                # Si el día no es válido para el mes (ej: 31 de febrero), usar el último día del mes
                fecha_vencimiento = date(anio, mes, dias_en_mes)
            
            # Crear concepto
            meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            concepto = f"Pago mensual de servicio - {meses[mes]} {anio}"
            
            if not dry_run:
                # Crear el pago
                pago = Pago.objects.create(
                    cliente=cliente,
                    instalacion=instalacion,
                    monto=plan_pago.monto_mensual,
                    concepto=concepto,
                    periodo_mes=mes,
                    periodo_anio=anio,
                    fecha_vencimiento=fecha_vencimiento,
                    estado='pendiente'
                )
                pagos_creados += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Pago creado: {cliente.nombre_completo} - ${plan_pago.monto_mensual} - {fecha_vencimiento}'
                    )
                )
            else:
                # Simulación
                pagos_creados += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'[SIMULACIÓN] Pago a crear: {cliente.nombre_completo} - ${plan_pago.monto_mensual} - {fecha_vencimiento}'
                    )
                )
        
        # Resumen
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        if dry_run:
            self.stdout.write(self.style.SUCCESS('SIMULACIÓN - No se crearon pagos reales'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Pagos creados: {pagos_creados}'))
        if solo_pendientes:
            self.stdout.write(self.style.WARNING(f'Pagos existentes (omitidos): {pagos_existentes}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))

