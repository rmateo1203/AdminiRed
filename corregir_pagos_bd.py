#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para corregir inconsistencias en la base de datos de pagos.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings.local')
django.setup()

from pagos.models import Pago, TransaccionPago
from django.utils import timezone

def corregir_pagos():
    """Corrige inconsistencias en los pagos."""
    print("=" * 80)
    print("CORRECCIÓN DE PAGOS EN LA BASE DE DATOS")
    print("=" * 80)
    print()
    
    correcciones = {
        'pagos_actualizados': 0,
        'transacciones_verificadas': 0,
        'errores': []
    }
    
    # 1. Corregir transacciones completadas sin pago marcado como pagado
    print("1. Corrigiendo transacciones completadas con pago NO marcado como 'pagado':")
    print("-" * 80)
    
    transacciones_inconsistentes = []
    for transaccion in TransaccionPago.objects.filter(estado='completada'):
        if transaccion.pago.estado != 'pagado':
            transacciones_inconsistentes.append(transaccion)
    
    for transaccion in transacciones_inconsistentes:
        try:
            print(f"  Corrigiendo Pago ID {transaccion.pago.id} (Transacción {transaccion.id})...")
            
            # Marcar el pago como pagado
            transaccion.pago.marcar_como_pagado(
                metodo_pago='tarjeta',
                referencia=transaccion.id_transaccion_pasarela or f"{transaccion.pasarela.upper()}-{transaccion.id}"
            )
            transaccion.pago.refresh_from_db()
            
            if transaccion.pago.estado == 'pagado':
                print(f"    ✅ Pago ID {transaccion.pago.id} actualizado a estado 'pagado'")
                correcciones['pagos_actualizados'] += 1
            else:
                print(f"    ❌ Error: No se pudo actualizar el pago ID {transaccion.pago.id}")
                correcciones['errores'].append(f"Pago ID {transaccion.pago.id}: No se pudo actualizar")
        except Exception as e:
            print(f"    ❌ Error al corregir Pago ID {transaccion.pago.id}: {str(e)}")
            correcciones['errores'].append(f"Pago ID {transaccion.pago.id}: {str(e)}")
    
    if not transacciones_inconsistentes:
        print("  ✅ No hay transacciones que corregir.")
    print()
    
    # 2. Verificar pagos pagados sin transacción completada
    print("2. Verificando pagos marcados como 'pagado' sin transacción completada:")
    print("-" * 80)
    
    pagos_sin_transaccion = []
    for pago in Pago.objects.filter(estado='pagado'):
        if not pago.transacciones.filter(estado='completada').exists():
            pagos_sin_transaccion.append(pago)
            print(f"  ⚠️  Pago ID {pago.id}: {pago.cliente.nombre_completo} - ${pago.monto}")
            print(f"     Estado: {pago.estado}, Fecha pago: {pago.fecha_pago}")
            print(f"     Transacciones: {pago.transacciones.count()}")
            print(f"     NOTA: Este pago está marcado como 'pagado' pero no tiene transacciones completadas.")
            print(f"           Esto puede ser correcto si fue pagado manualmente (efectivo, transferencia, etc.)")
    
    if not pagos_sin_transaccion:
        print("  ✅ Todos los pagos marcados como 'pagado' tienen al menos una transacción completada.")
    print()
    
    # 3. Resumen de correcciones
    print("=" * 80)
    print("RESUMEN DE CORRECCIONES")
    print("=" * 80)
    print(f"Pagos actualizados: {correcciones['pagos_actualizados']}")
    print(f"Errores encontrados: {len(correcciones['errores'])}")
    
    if correcciones['errores']:
        print("\nErrores:")
        for error in correcciones['errores']:
            print(f"  - {error}")
    
    if correcciones['pagos_actualizados'] > 0:
        print(f"\n✅ Se corrigieron {correcciones['pagos_actualizados']} pagos exitosamente.")
    else:
        print("\n✅ No se encontraron inconsistencias que corregir.")
    
    return correcciones

if __name__ == '__main__':
    respuesta = input("¿Estás seguro de que quieres corregir las inconsistencias? (s/n): ")
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        corregir_pagos()
    else:
        print("Operación cancelada.")


