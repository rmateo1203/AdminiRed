from django.core.management.base import BaseCommand
from pagos.models import Pago, TransaccionPago
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Verifica y reporta inconsistencias en la base de datos de pagos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--corregir',
            action='store_true',
            help='Corrige automáticamente las inconsistencias encontradas',
        )

    def handle(self, *args, **options):
        corregir = options.get('corregir', False)
        
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("VERIFICACIÓN DE PAGOS EN LA BASE DE DATOS"))
        self.stdout.write("=" * 80)
        self.stdout.write()
        
        # 1. Pagos marcados como pagados sin transacción completada
        self.stdout.write("1. Pagos marcados como 'pagado' sin transacción completada:")
        self.stdout.write("-" * 80)
        pagos_pagados_sin_transaccion = []
        for pago in Pago.objects.filter(estado='pagado'):
            transacciones_completadas = pago.transacciones.filter(estado='completada')
            if not transacciones_completadas.exists():
                pagos_pagados_sin_transaccion.append(pago)
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠️  Pago ID {pago.id}: {pago.cliente.nombre_completo} - ${pago.monto} - {pago.concepto}"
                    )
                )
                self.stdout.write(f"     Estado: {pago.estado}, Fecha pago: {pago.fecha_pago}")
                self.stdout.write(f"     Transacciones: {pago.transacciones.count()} (ninguna completada)")
                self.stdout.write(
                    "     NOTA: Esto puede ser correcto si fue pagado manualmente (efectivo, transferencia, etc.)"
                )
        
        if not pagos_pagados_sin_transaccion:
            self.stdout.write(self.style.SUCCESS(
                "  ✅ Todos los pagos marcados como 'pagado' tienen al menos una transacción completada."
            ))
        self.stdout.write()
        
        # 2. Transacciones completadas sin pago marcado como pagado
        self.stdout.write("2. Transacciones completadas con pago NO marcado como 'pagado':")
        self.stdout.write("-" * 80)
        transacciones_con_inconsistencia = []
        for transaccion in TransaccionPago.objects.filter(estado='completada'):
            if transaccion.pago.estado != 'pagado':
                transacciones_con_inconsistencia.append(transaccion)
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠️  Transacción ID {transaccion.id}: Pasarela: {transaccion.pasarela}"
                    )
                )
                self.stdout.write(
                    f"     Pago ID {transaccion.pago.id}: Estado actual: '{transaccion.pago.estado}' (debería ser 'pagado')"
                )
                self.stdout.write(f"     Cliente: {transaccion.pago.cliente.nombre_completo} - ${transaccion.pago.monto}")
                self.stdout.write(f"     ID Externa: {transaccion.id_transaccion_pasarela}")
                self.stdout.write(f"     Fecha completada: {transaccion.fecha_completada}")
                
                if corregir:
                    try:
                        transaccion.pago.marcar_como_pagado(
                            metodo_pago='tarjeta',
                            referencia=transaccion.id_transaccion_pasarela or f"{transaccion.pasarela.upper()}-{transaccion.id}"
                        )
                        transaccion.pago.refresh_from_db()
                        if transaccion.pago.estado == 'pagado':
                            self.stdout.write(
                                self.style.SUCCESS(f"     ✅ CORREGIDO: Pago actualizado a estado 'pagado'")
                            )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"     ❌ ERROR al corregir: {str(e)}")
                        )
        
        if not transacciones_con_inconsistencia:
            self.stdout.write(self.style.SUCCESS(
                "  ✅ Todas las transacciones completadas tienen su pago marcado como 'pagado'."
            ))
        self.stdout.write()
        
        # 3. Pagos con múltiples transacciones completadas
        self.stdout.write("3. Pagos con múltiples transacciones completadas:")
        self.stdout.write("-" * 80)
        pagos_con_multiples_completadas = []
        for pago in Pago.objects.filter(estado='pagado'):
            transacciones_completadas = pago.transacciones.filter(estado='completada')
            if transacciones_completadas.count() > 1:
                pagos_con_multiples_completadas.append(pago)
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠️  Pago ID {pago.id}: {pago.cliente.nombre_completo} - ${pago.monto}"
                    )
                )
                self.stdout.write(f"     Tiene {transacciones_completadas.count()} transacciones completadas:")
                for trans in transacciones_completadas:
                    self.stdout.write(
                        f"       - Transacción {trans.id}: {trans.pasarela} - ID: {trans.id_transaccion_pasarela} - {trans.fecha_completada}"
                    )
        
        if not pagos_con_multiples_completadas:
            self.stdout.write(self.style.SUCCESS(
                "  ✅ No hay pagos con múltiples transacciones completadas."
            ))
        self.stdout.write()
        
        # 4. Transacciones pendientes (todas)
        self.stdout.write("4. Transacciones pendientes:")
        self.stdout.write("-" * 80)
        transacciones_pendientes = TransaccionPago.objects.filter(estado='pendiente')
        
        if transacciones_pendientes.exists():
            self.stdout.write(f"  Total de transacciones pendientes: {transacciones_pendientes.count()}")
            count = 0
            for trans in transacciones_pendientes.order_by('-fecha_creacion'):
                if count >= 20:  # Mostrar solo las primeras 20
                    self.stdout.write(f"  ... y {transacciones_pendientes.count() - 20} más")
                    break
                horas_pasadas = (timezone.now() - trans.fecha_creacion).total_seconds() / 3600
                self.stdout.write(
                    self.style.WARNING(f"  ⏰ Transacción ID {trans.id}: Pasarela: {trans.pasarela}")
                )
                self.stdout.write(f"     Pago ID {trans.pago.id}: Estado pago: {trans.pago.estado}")
                self.stdout.write(f"     Cliente: {trans.pago.cliente.nombre_completo} - ${trans.pago.monto}")
                self.stdout.write(f"     Creada hace: {horas_pasadas:.1f} horas")
                self.stdout.write(f"     ID Externa: {trans.id_transaccion_pasarela}")
                
                # Si tiene ID externa de Mercado Pago, intentar verificar
                if trans.pasarela == 'mercadopago' and trans.id_transaccion_pasarela and corregir:
                    try:
                        from pagos.payment_gateway import PaymentGateway
                        gateway = PaymentGateway(pasarela='mercadopago')
                        
                        # El id_transaccion_pasarela puede ser un preference_id (con guiones) o un payment_id (numérico)
                        trans_id = trans.id_transaccion_pasarela
                        
                        # Si parece ser un preference_id (contiene guiones), buscar pagos asociados
                        if '-' in str(trans_id):
                            self.stdout.write(f"     NOTA: ID parece ser preference_id. Buscando pagos asociados...")
                            # Buscar en los datos de respuesta si hay un payment_id
                            if trans.datos_respuesta and 'payment_id' in str(trans.datos_respuesta):
                                # Intentar extraer payment_id de los datos
                                import json
                                datos_str = json.dumps(trans.datos_respuesta) if isinstance(trans.datos_respuesta, dict) else str(trans.datos_respuesta)
                                # Buscar en los datos si hay información del pago
                                self.stdout.write(f"     ⚠️  Esta transacción usa preference_id. Verifica manualmente el estado en Mercado Pago.")
                        else:
                            # Es un payment_id numérico, intentar verificar
                            try:
                                payment_response = gateway.mp.payment().get(int(trans_id))
                                if payment_response.get("status") == 200:
                                    payment = payment_response.get("response", {})
                                    payment_status = payment.get("status", "")
                                    self.stdout.write(f"     Estado en Mercado Pago: {payment_status}")
                                    
                                    if payment_status == "approved" and trans.estado != 'completada':
                                        trans.marcar_como_completada()
                                        trans.pago.refresh_from_db()
                                        self.stdout.write(
                                            self.style.SUCCESS(f"     ✅ ACTUALIZADO: Transacción marcada como completada, pago actualizado a 'pagado'")
                                        )
                                    elif payment_status in ["rejected", "cancelled"]:
                                        trans.estado = 'fallida'
                                        trans.mensaje_error = payment.get("status_detail", f"Pago {payment_status}")
                                        trans.save()
                                        self.stdout.write(
                                            self.style.WARNING(f"     ⚠️  Actualizado: Transacción marcada como fallida ({payment_status})")
                                        )
                            except ValueError:
                                self.stdout.write(
                                    self.style.WARNING(f"     ⚠️  ID no es numérico, no se puede verificar automáticamente")
                                )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"     ❌ Error al verificar con Mercado Pago: {str(e)}")
                        )
                
                count += 1
        else:
            self.stdout.write(self.style.SUCCESS(
                "  ✅ No hay transacciones pendientes."
            ))
        self.stdout.write()
        
        # 5. Resumen general
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("RESUMEN GENERAL"))
        self.stdout.write("=" * 80)
        total_pagos = Pago.objects.count()
        pagos_pagados = Pago.objects.filter(estado='pagado').count()
        pagos_pendientes = Pago.objects.filter(estado='pendiente').count()
        pagos_vencidos = Pago.objects.filter(estado='vencido').count()
        pagos_cancelados = Pago.objects.filter(estado='cancelado').count()
        
        total_transacciones = TransaccionPago.objects.count()
        transacciones_completadas = TransaccionPago.objects.filter(estado='completada').count()
        transacciones_pendientes = TransaccionPago.objects.filter(estado='pendiente').count()
        transacciones_fallidas = TransaccionPago.objects.filter(estado='fallida').count()
        
        self.stdout.write(f"Total de Pagos: {total_pagos}")
        self.stdout.write(f"  - Pagados: {pagos_pagados}")
        self.stdout.write(f"  - Pendientes: {pagos_pendientes}")
        self.stdout.write(f"  - Vencidos: {pagos_vencidos}")
        self.stdout.write(f"  - Cancelados: {pagos_cancelados}")
        self.stdout.write()
        self.stdout.write(f"Total de Transacciones: {total_transacciones}")
        self.stdout.write(f"  - Completadas: {transacciones_completadas}")
        self.stdout.write(f"  - Pendientes: {transacciones_pendientes}")
        self.stdout.write(f"  - Fallidas: {transacciones_fallidas}")
        self.stdout.write()
        
        # Inconsistencias encontradas
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("INCONSISTENCIAS ENCONTRADAS"))
        self.stdout.write("=" * 80)
        total_inconsistencias = len(transacciones_con_inconsistencia)
        
        if total_inconsistencias == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "✅ No se encontraron inconsistencias críticas. La base de datos está correcta."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  Se encontraron {total_inconsistencias} inconsistencias críticas:"
                )
            )
            self.stdout.write(
                f"  - Transacciones completadas sin pago marcado como pagado: {len(transacciones_con_inconsistencia)}"
            )
            if not corregir:
                self.stdout.write()
                self.stdout.write(
                    "Para corregir estas inconsistencias automáticamente, ejecuta:"
                )
                self.stdout.write(
                    self.style.SUCCESS("  python manage.py verificar_pagos_bd --corregir")
                )
            else:
                self.stdout.write()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Se intentaron corregir {len(transacciones_con_inconsistencia)} inconsistencias."
                    )
                )

