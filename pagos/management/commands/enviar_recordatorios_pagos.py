"""
Comando de gestión para enviar recordatorios automáticos de pagos.

Uso:
    python manage.py enviar_recordatorios_pagos
    python manage.py enviar_recordatorios_pagos --dias-antes 3
    python manage.py enviar_recordatorios_pagos --solo-vencidos
    python manage.py enviar_recordatorios_pagos --dry-run
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from pagos.models import Pago
from notificaciones.models import TipoNotificacion, Notificacion, ConfiguracionNotificacion
from pagos.services import RecordatorioPagoService
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Envía recordatorios automáticos de pagos pendientes y vencidos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias-antes',
            type=int,
            default=3,
            help='Días antes del vencimiento para enviar recordatorio (default: 3)',
        )
        parser.add_argument(
            '--dias-despues',
            type=int,
            default=1,
            help='Días después del vencimiento para enviar recordatorio (default: 1)',
        )
        parser.add_argument(
            '--solo-vencidos',
            action='store_true',
            help='Enviar solo recordatorios de pagos vencidos',
        )
        parser.add_argument(
            '--solo-pendientes',
            action='store_true',
            help='Enviar solo recordatorios de pagos pendientes (antes de vencer)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula el envío sin crear notificaciones realmente',
        )
        parser.add_argument(
            '--forzar',
            action='store_true',
            help='Forzar envío incluso si ya se envió un recordatorio recientemente',
        )

    def handle(self, *args, **options):
        dias_antes = options['dias_antes']
        dias_despues = options['dias_despues']
        solo_vencidos = options['solo_vencidos']
        solo_pendientes = options['solo_pendientes']
        dry_run = options['dry_run']
        forzar = options['forzar']
        
        hoy = timezone.now().date()
        
        # Obtener o crear tipos de notificación
        tipo_recordatorio_antes, _ = TipoNotificacion.objects.get_or_create(
            codigo='recordatorio_pago_antes',
            defaults={
                'nombre': 'Recordatorio de Pago (Antes de Vencimiento)',
                'descripcion': 'Recordatorio enviado antes de la fecha de vencimiento',
            }
        )
        
        tipo_recordatorio_vencido, _ = TipoNotificacion.objects.get_or_create(
            codigo='recordatorio_pago_vencido',
            defaults={
                'nombre': 'Recordatorio de Pago Vencido',
                'descripcion': 'Recordatorio enviado después de la fecha de vencimiento',
            }
        )
        
        # Obtener configuración o usar valores por defecto
        config_antes = ConfiguracionNotificacion.objects.filter(
            tipo_notificacion=tipo_recordatorio_antes,
            activa=True
        ).first()
        
        config_vencido = ConfiguracionNotificacion.objects.filter(
            tipo_notificacion=tipo_recordatorio_vencido,
            activa=True
        ).first()
        
        # Usar configuración si existe, sino usar valores del comando
        if config_antes:
            dias_antes = config_antes.dias_antes_vencimiento
        if config_vencido:
            dias_despues = config_vencido.dias_despues_vencimiento
        
        self.stdout.write(
            self.style.SUCCESS('='*60)
        )
        self.stdout.write(
            self.style.SUCCESS('📧 SISTEMA DE RECORDATORIOS AUTOMÁTICOS DE PAGOS')
        )
        self.stdout.write(
            self.style.SUCCESS('='*60)
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('\n⚠️  MODO DRY-RUN: No se crearán notificaciones realmente\n')
            )
        
        # Recordatorios de pagos pendientes (antes de vencer)
        recordatorios_antes = 0
        if not solo_vencidos:
            fecha_limite_antes = hoy + timedelta(days=dias_antes)
            
            pagos_pendientes = Pago.objects.filter(
                estado='pendiente',
                fecha_vencimiento=fecha_limite_antes,
                cliente__email__isnull=False
            ).exclude(cliente__email='').select_related('cliente', 'instalacion')
            
            # Excluir pagos que ya tienen recordatorio reciente (a menos que se fuerce)
            if not forzar:
                # Obtener IDs de pagos con recordatorios enviados en los últimos 2 días
                pagos_con_recordatorio = Notificacion.objects.filter(
                    pago__in=pagos_pendientes,
                    tipo=tipo_recordatorio_antes,
                    estado='enviada',
                    fecha_envio__gte=timezone.now() - timedelta(days=2)
                ).values_list('pago_id', flat=True)
                
                pagos_pendientes = pagos_pendientes.exclude(id__in=pagos_con_recordatorio)
            
            total_pendientes = pagos_pendientes.count()
            
            if total_pendientes > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f'\n📅 Recordatorios ANTES de vencimiento ({dias_antes} días antes):'
                    )
                )
                self.stdout.write(
                    f'   Encontrados {total_pendientes} pago(s) pendiente(s) que vencen el {fecha_limite_antes.strftime("%d/%m/%Y")}'
                )
                
                for pago in pagos_pendientes:
                    if dry_run:
                        self.stdout.write(
                            f'   [DRY-RUN] Se crearía recordatorio para: {pago.cliente.nombre_completo} - ${pago.monto}'
                        )
                        recordatorios_antes += 1
                    else:
                        resultado = RecordatorioPagoService.crear_recordatorio_antes_vencimiento(
                            pago, dias_antes, tipo_recordatorio_antes, config_antes
                        )
                        if resultado['success']:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'   ✓ Recordatorio creado: {pago.cliente.nombre_completo} - ${pago.monto}'
                                )
                            )
                            recordatorios_antes += 1
                        else:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'   ✗ Error: {pago.cliente.nombre_completo} - {resultado.get("error", "Error desconocido")}'
                                )
                            )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ No hay pagos pendientes que requieran recordatorio ({dias_antes} días antes)'
                    )
                )
        
        # Recordatorios de pagos vencidos
        recordatorios_vencidos = 0
        if not solo_pendientes:
            fecha_limite_vencido = hoy - timedelta(days=dias_despues)
            
            pagos_vencidos = Pago.objects.filter(
                estado__in=['vencido', 'pendiente'],
                fecha_vencimiento__lte=fecha_limite_vencido,
                cliente__email__isnull=False
            ).exclude(cliente__email='').exclude(estado='pagado').select_related('cliente', 'instalacion')
            
            # Excluir pagos que ya tienen recordatorio reciente (a menos que se fuerce)
            if not forzar:
                # Obtener IDs de pagos con recordatorios enviados en los últimos 7 días
                pagos_con_recordatorio = Notificacion.objects.filter(
                    pago__in=pagos_vencidos,
                    tipo=tipo_recordatorio_vencido,
                    estado='enviada',
                    fecha_envio__gte=timezone.now() - timedelta(days=7)
                ).values_list('pago_id', flat=True)
                
                pagos_vencidos = pagos_vencidos.exclude(id__in=pagos_con_recordatorio)
            
            total_vencidos = pagos_vencidos.count()
            
            if total_vencidos > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f'\n⚠️  Recordatorios de pagos VENCIDOS ({dias_despues} días después):'
                    )
                )
                self.stdout.write(
                    f'   Encontrados {total_vencidos} pago(s) vencido(s) o pendiente(s) desde el {fecha_limite_vencido.strftime("%d/%m/%Y")}'
                )
                
                for pago in pagos_vencidos:
                    if dry_run:
                        dias = (hoy - pago.fecha_vencimiento).days
                        self.stdout.write(
                            f'   [DRY-RUN] Se crearía recordatorio para: {pago.cliente.nombre_completo} - ${pago.monto} (Vencido hace {dias} días)'
                        )
                        recordatorios_vencidos += 1
                    else:
                        resultado = RecordatorioPagoService.crear_recordatorio_vencido(
                            pago, dias_despues, tipo_recordatorio_vencido, config_vencido
                        )
                        if resultado['success']:
                            dias = (hoy - pago.fecha_vencimiento).days
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'   ✓ Recordatorio creado: {pago.cliente.nombre_completo} - ${pago.monto} (Vencido hace {dias} días)'
                                )
                            )
                            recordatorios_vencidos += 1
                        else:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'   ✗ Error: {pago.cliente.nombre_completo} - {resultado.get("error", "Error desconocido")}'
                                )
                            )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ No hay pagos vencidos que requieran recordatorio ({dias_despues} días después)'
                    )
                )
        
        # Resumen
        total_recordatorios = recordatorios_antes + recordatorios_vencidos
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(
                f'📊 RESUMEN:\n'
                f'   • Recordatorios antes de vencimiento: {recordatorios_antes}\n'
                f'   • Recordatorios de pagos vencidos: {recordatorios_vencidos}\n'
                f'   • Total de recordatorios: {total_recordatorios}'
            )
        )
        
        if not dry_run and total_recordatorios > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    '\n💡 Tip: Ejecuta "python manage.py send_notifications" para enviar las notificaciones creadas.'
                )
            )
        
        self.stdout.write('='*60 + '\n')

