"""
Comando de gestión para generar instalaciones de ejemplo con pagos vencidos.

Este comando crea:
- Clientes de ejemplo
- Instalaciones activas para esos clientes
- PlanPago automático (se crea al activar la instalación)
- Pagos vencidos para períodos anteriores

Uso:
    python manage.py generar_instalaciones_pagos_vencidos
    python manage.py generar_instalaciones_pagos_vencidos --cantidad 5
    python manage.py generar_instalaciones_pagos_vencidos --meses-vencidos 3
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta, datetime
from calendar import monthrange
from clientes.models import Cliente
from instalaciones.models import Instalacion, TipoInstalacion, PlanInternet
from pagos.models import Pago, PlanPago
import random


class Command(BaseCommand):
    help = 'Genera instalaciones de ejemplo con pagos vencidos para pruebas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            type=int,
            default=5,
            help='Cantidad de instalaciones a crear (default: 5)',
        )
        parser.add_argument(
            '--meses-vencidos',
            type=int,
            default=2,
            help='Cantidad de meses vencidos a generar por instalación (default: 2)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular la generación sin crear datos reales',
        )

    def handle(self, *args, **options):
        cantidad = options.get('cantidad', 5)
        meses_vencidos = options.get('meses_vencidos', 2)
        dry_run = options.get('dry_run', False)
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Generando Instalaciones con Pagos Vencidos'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('[MODO SIMULACIÓN - No se crearán datos reales]'))
        
        # Obtener o crear TipoInstalacion
        tipo_instalacion, _ = TipoInstalacion.objects.get_or_create(
            nombre='Fibra Óptica',
            defaults={'nombre': 'Fibra Óptica'}
        )
        
        # Obtener o crear PlanInternet de ejemplo
        plan_internet, _ = PlanInternet.objects.get_or_create(
            nombre='Plan Básico 50 Mbps',
            defaults={
                'nombre': 'Plan Básico 50 Mbps',
                'velocidad_descarga': 50,
                'velocidad_subida': 25,
                'precio_mensual': 500.00,
                'activo': True
            }
        )
        
        nombres = [
            'Juan', 'María', 'Pedro', 'Ana', 'Carlos', 'Laura', 'Miguel', 'Sofía',
            'José', 'Carmen', 'Luis', 'Patricia', 'Roberto', 'Mónica', 'Fernando'
        ]
        apellidos = [
            'García', 'Rodríguez', 'López', 'Martínez', 'González', 'Pérez', 'Sánchez',
            'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez', 'Díaz', 'Hernández', 'Morales'
        ]
        
        clientes_creados = 0
        instalaciones_creadas = 0
        pagos_creados = 0
        
        hoy = date.today()
        
        for i in range(cantidad):
            # Crear cliente
            nombre = random.choice(nombres)
            apellido1 = random.choice(apellidos)
            apellido2 = random.choice(apellidos)
            telefono = f"55{random.randint(10000000, 99999999)}"
            email = f"{nombre.lower()}.{apellido1.lower()}{i}@example.com"
            
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        f'[SIMULACIÓN] Cliente: {nombre} {apellido1} {apellido2} - {telefono}'
                    )
                )
            else:
                cliente, created = Cliente.objects.get_or_create(
                    email=email,
                    defaults={
                        'nombre': nombre,
                        'apellido1': apellido1,
                        'apellido2': apellido2,
                        'telefono': telefono,
                        'email': email,
                        'direccion': f'Calle {random.randint(1, 200)} #123',
                        'ciudad': 'Ciudad de México',
                        'estado': 'CDMX',
                        'codigo_postal': f"{random.randint(10000, 99999)}",
                    }
                )
                
                if created:
                    clientes_creados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Cliente creado: {cliente.nombre_completo}')
                    )
                else:
                    cliente = Cliente.objects.get(email=email)
            
            # Crear instalación
            # Fecha de activación: hace varios meses (para tener pagos vencidos)
            meses_atras = random.randint(3, 6)  # Activada hace 3-6 meses
            
            # Calcular fecha de activación retrocediendo meses correctamente
            anio_activacion = hoy.year
            mes_activacion = hoy.month - meses_atras
            
            # Ajustar si el mes es negativo o cero
            while mes_activacion <= 0:
                mes_activacion += 12
                anio_activacion -= 1
            
            # Usar el día 15 como día de activación (o el día actual si es menor)
            dia_activacion = min(15, hoy.day)
            
            # Asegurar que la fecha sea válida
            dias_en_mes = monthrange(anio_activacion, mes_activacion)[1]
            dia_activacion = min(dia_activacion, dias_en_mes)
            
            try:
                fecha_activacion = date(anio_activacion, mes_activacion, dia_activacion)
            except ValueError:
                # Si el día no es válido para ese mes, usar el último día del mes
                fecha_activacion = date(anio_activacion, mes_activacion, dias_en_mes)
            
            # Asegurar que la fecha esté en el pasado
            if fecha_activacion >= hoy:
                # Si por alguna razón está en el futuro, usar hace 4 meses exactamente
                meses_atras = 4
                anio_activacion = hoy.year
                mes_activacion = hoy.month - meses_atras
                while mes_activacion <= 0:
                    mes_activacion += 12
                    anio_activacion -= 1
                dias_en_mes = monthrange(anio_activacion, mes_activacion)[1]
                fecha_activacion = date(anio_activacion, mes_activacion, min(15, dias_en_mes))
            
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        f'[SIMULACIÓN] Instalación para {nombre} {apellido1} - '
                        f'Activada: {fecha_activacion.strftime("%d/%m/%Y")}'
                    )
                )
            else:
                instalacion = Instalacion.objects.create(
                    cliente=cliente,
                    tipo_instalacion=tipo_instalacion,
                    plan=plan_internet,
                    plan_nombre=plan_internet.nombre,
                    velocidad_descarga=plan_internet.velocidad_descarga,
                    velocidad_subida=plan_internet.velocidad_subida,
                    precio_mensual=plan_internet.precio_mensual,
                    direccion_instalacion=cliente.direccion,
                    estado='activa',
                    fecha_activacion=timezone.make_aware(
                        timezone.datetime.combine(fecha_activacion, timezone.datetime.min.time())
                    ),
                    ip_asignada=None,  # No asignar IP para evitar duplicados en datos de prueba
                    mac_equipo=None,  # No asignar MAC para evitar duplicados en datos de prueba
                )
                instalaciones_creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Instalación creada: {instalacion.numero_contrato} - '
                        f'Cliente: {cliente.nombre_completo}'
                    )
                )
                
                # Esperar a que se cree el PlanPago automáticamente (signal)
                # Refrescar desde BD
                instalacion.refresh_from_db()
                
                if hasattr(instalacion, 'plan_pago') and instalacion.plan_pago:
                    plan_pago = instalacion.plan_pago
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  → PlanPago creado: ${plan_pago.monto_mensual}/mes, '
                            f'día {plan_pago.dia_vencimiento}'
                        )
                    )
                    
                    # Generar pagos vencidos
                    dia_vencimiento = plan_pago.dia_vencimiento
                    
                    # Calcular desde qué mes generar pagos vencidos
                    mes_inicio = fecha_activacion.month
                    anio_inicio = fecha_activacion.year
                    
                    # Generar pagos vencidos para los últimos N meses
                    for mes_offset in range(meses_vencidos):
                        # Calcular mes y año
                        mes = mes_inicio - mes_offset
                        anio = anio_inicio
                        
                        # Ajustar si el mes es negativo
                        while mes <= 0:
                            mes += 12
                            anio -= 1
                        
                        # Calcular fecha de vencimiento
                        dias_en_mes = monthrange(anio, mes)[1]
                        dia_venc = min(dia_vencimiento, dias_en_mes)
                        
                        try:
                            fecha_vencimiento = date(anio, mes, dia_venc)
                        except ValueError:
                            fecha_vencimiento = date(anio, mes, dias_en_mes)
                        
                        # Solo crear si la fecha de vencimiento ya pasó
                        if fecha_vencimiento < hoy:
                            meses_nombres = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                                           'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                            concepto = f"Pago mensual de servicio - {meses_nombres[mes]} {anio}"
                            
                            # Verificar si ya existe
                            pago_existente = Pago.objects.filter(
                                cliente=cliente,
                                instalacion=instalacion,
                                periodo_mes=mes,
                                periodo_anio=anio
                            ).first()
                            
                            if not pago_existente:
                                pago = Pago.objects.create(
                                    cliente=cliente,
                                    instalacion=instalacion,
                                    monto=plan_pago.monto_mensual,
                                    concepto=concepto,
                                    periodo_mes=mes,
                                    periodo_anio=anio,
                                    fecha_vencimiento=fecha_vencimiento,
                                    estado='vencido'  # Directamente como vencido
                                )
                                pagos_creados += 1
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f'  → Pago vencido creado: {concepto} - '
                                        f'${pago.monto} - Vence: {fecha_vencimiento.strftime("%d/%m/%Y")} '
                                        f'({(hoy - fecha_vencimiento).days} días vencido)'
                                    )
                                )
                            else:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'  → Pago ya existe para {concepto}, omitido'
                                    )
                                )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'  ✗ No se pudo crear PlanPago para instalación {instalacion.numero_contrato}'
                        )
                    )
        
        # Resumen
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        if dry_run:
            self.stdout.write(self.style.WARNING('SIMULACIÓN - No se crearon datos reales'))
        else:
            self.stdout.write(self.style.SUCCESS('RESUMEN:'))
            self.stdout.write(self.style.SUCCESS(f'  • Clientes creados: {clientes_creados}'))
            self.stdout.write(self.style.SUCCESS(f'  • Instalaciones creadas: {instalaciones_creadas}'))
            self.stdout.write(self.style.SUCCESS(f'  • Pagos vencidos creados: {pagos_creados}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        if not dry_run:
            # Actualizar pagos vencidos para asegurar consistencia
            cantidad_actualizados = Pago.actualizar_pagos_vencidos()
            if cantidad_actualizados > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Se actualizaron {cantidad_actualizados} pago(s) adicionales a estado vencido.'
                    )
                )

