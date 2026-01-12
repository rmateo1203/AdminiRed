#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar y corregir inconsistencias en la base de datos de pagos.
Ejecutar con: python manage.py shell < verificar_pagos_manage.py
"""
from pagos.models import Pago, TransaccionPago
from django.utils import timezone
from datetime import timedelta

def verificar_pagos():
    """Verifica y reporta inconsistencias en los pagos."""
    print("=" * 80)
    print("VERIFICACIÓN DE PAGOS EN LA BASE DE DATOS")
    print("=" * 80)
    print()
    
    # 1. Pagos marcados como pagados sin transacción completada
    print("1. Pagos marcados como 'pagado' sin transacción completada:")
    print("-" * 80)
    pagos_pagados_sin_transaccion = []
    for pago in Pago.objects.filter(estado='pagado'):
        transacciones_completadas = pago.transacciones.filter(estado='completada')
        if not transacciones_completadas.exists():
            pagos_pagados_sin_transaccion.append(pago)
            print(f"  ❌ Pago ID {pago.id}: {pago.cliente.nombre_completo} - ${pago.monto} - {pago.concepto}")
            print(f"     Estado: {pago.estado}, Fecha pago: {pago.fecha_pago}")
            print(f"     Transacciones: {pago.transacciones.count()} (ninguna completada)")
    
    if not pagos_pagados_sin_transaccion:
        print("  ✅ Todos los pagos marcados como 'pagado' tienen al menos una transacción completada.")
    print()
    
    # 2. Transacciones completadas sin pago marcado como pagado
    print("2. Transacciones completadas con pago NO marcado como 'pagado':")
    print("-" * 80)
    transacciones_con_inconsistencia = []
    for transaccion in TransaccionPago.objects.filter(estado='completada'):
        if transaccion.pago.estado != 'pagado':
            transacciones_con_inconsistencia.append(transaccion)
            print(f"  ⚠️  Transacción ID {transaccion.id}: Pasarela: {transaccion.pasarela}")
            print(f"     Pago ID {transaccion.pago.id}: Estado actual: '{transaccion.pago.estado}' (debería ser 'pagado')")
            print(f"     Cliente: {transaccion.pago.cliente.nombre_completo} - ${transaccion.pago.monto}")
            print(f"     ID Externa: {transaccion.id_transaccion_pasarela}")
            print(f"     Fecha completada: {transaccion.fecha_completada}")
    
    if not transacciones_con_inconsistencia:
        print("  ✅ Todas las transacciones completadas tienen su pago marcado como 'pagado'.")
    print()
    
    # 3. Pagos con múltiples transacciones completadas
    print("3. Pagos con múltiples transacciones completadas:")
    print("-" * 80)
    pagos_con_multiples_completadas = []
    for pago in Pago.objects.filter(estado='pagado'):
        transacciones_completadas = pago.transacciones.filter(estado='completada')
        if transacciones_completadas.count() > 1:
            pagos_con_multiples_completadas.append(pago)
            print(f"  ⚠️  Pago ID {pago.id}: {pago.cliente.nombre_completo} - ${pago.monto}")
            print(f"     Tiene {transacciones_completadas.count()} transacciones completadas:")
            for trans in transacciones_completadas:
                print(f"       - Transacción {trans.id}: {trans.pasarela} - ID: {trans.id_transaccion_pasarela} - {trans.fecha_completada}")
    
    if not pagos_con_multiples_completadas:
        print("  ✅ No hay pagos con múltiples transacciones completadas.")
    print()
    
    # 4. Transacciones pendientes antiguas (más de 24 horas)
    print("4. Transacciones pendientes antiguas (más de 24 horas):")
    print("-" * 80)
    transacciones_antiguas = TransaccionPago.objects.filter(
        estado='pendiente',
        fecha_creacion__lt=timezone.now() - timedelta(hours=24)
    )
    
    if transacciones_antiguas.exists():
        count = 0
        for trans in transacciones_antiguas:
            if count >= 10:  # Mostrar solo las primeras 10
                print(f"  ... y {transacciones_antiguas.count() - 10} más")
                break
            horas_pasadas = (timezone.now() - trans.fecha_creacion).total_seconds() / 3600
            print(f"  ⏰ Transacción ID {trans.id}: Pasarela: {trans.pasarela}")
            print(f"     Pago ID {trans.pago.id}: Estado: {trans.pago.estado}")
            print(f"     Creada hace: {horas_pasadas:.1f} horas")
            print(f"     ID Externa: {trans.id_transaccion_pasarela}")
            count += 1
    else:
        print("  ✅ No hay transacciones pendientes antiguas.")
    print()
    
    # 5. Resumen general
    print("=" * 80)
    print("RESUMEN GENERAL")
    print("=" * 80)
    total_pagos = Pago.objects.count()
    pagos_pagados = Pago.objects.filter(estado='pagado').count()
    pagos_pendientes = Pago.objects.filter(estado='pendiente').count()
    pagos_vencidos = Pago.objects.filter(estado='vencido').count()
    pagos_cancelados = Pago.objects.filter(estado='cancelado').count()
    
    total_transacciones = TransaccionPago.objects.count()
    transacciones_completadas = TransaccionPago.objects.filter(estado='completada').count()
    transacciones_pendientes = TransaccionPago.objects.filter(estado='pendiente').count()
    transacciones_fallidas = TransaccionPago.objects.filter(estado='fallida').count()
    
    print(f"Total de Pagos: {total_pagos}")
    print(f"  - Pagados: {pagos_pagados}")
    print(f"  - Pendientes: {pagos_pendientes}")
    print(f"  - Vencidos: {pagos_vencidos}")
    print(f"  - Cancelados: {pagos_cancelados}")
    print()
    print(f"Total de Transacciones: {total_transacciones}")
    print(f"  - Completadas: {transacciones_completadas}")
    print(f"  - Pendientes: {transacciones_pendientes}")
    print(f"  - Fallidas: {transacciones_fallidas}")
    print()
    
    # Inconsistencias encontradas
    print("=" * 80)
    print("INCONSISTENCIAS ENCONTRADAS")
    print("=" * 80)
    total_inconsistencias = len(pagos_pagados_sin_transaccion) + len(transacciones_con_inconsistencia)
    
    if total_inconsistencias == 0:
        print("✅ No se encontraron inconsistencias. La base de datos está correcta.")
    else:
        print(f"⚠️  Se encontraron {total_inconsistencias} inconsistencias:")
        print(f"  - Pagos pagados sin transacción completada: {len(pagos_pagados_sin_transaccion)}")
        print(f"  - Transacciones completadas sin pago marcado como pagado: {len(transacciones_con_inconsistencia)}")
        print()
        print("Para corregir estas inconsistencias, ejecuta:")
        print("  python manage.py shell < corregir_pagos_manage.py")
    
    return {
        'pagos_pagados_sin_transaccion': pagos_pagados_sin_transaccion,
        'transacciones_con_inconsistencia': transacciones_con_inconsistencia,
        'pagos_con_multiples_completadas': pagos_con_multiples_completadas,
    }

# Ejecutar la verificación
verificar_pagos()


