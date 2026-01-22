#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para crear materiales de inventario para instalación de internet.

Uso:
    python crear_materiales_inventario.py
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from inventario.models import Material, CategoriaMaterial
from decimal import Decimal


def crear_materiales():
    """Crea materiales de ejemplo para cada categoría."""
    
    print('🚀 Creando materiales de inventario para instalación de internet...\n')
    
    # Obtener categorías
    categorias = {}
    for cat in CategoriaMaterial.objects.all():
        categorias[cat.nombre] = cat
    
    # Definir materiales por categoría
    materiales_data = [
        # Cables y Conectores
        {
            'nombre': 'Cable UTP Cat 5e',
            'codigo': 'UTP-CAT5E-305M',
            'categoria': 'Cables y Conectores',
            'descripcion': 'Cable UTP categoría 5e, 305 metros, para instalaciones de red',
            'stock_actual': 50,
            'stock_minimo': 10,
            'unidad_medida': 'rollo',
            'precio_compra': Decimal('450.00'),
            'precio_venta': Decimal('650.00'),
            'ubicacion': 'Almacén A - Estante 1'
        },
        {
            'nombre': 'Cable UTP Cat 6',
            'codigo': 'UTP-CAT6-305M',
            'categoria': 'Cables y Conectores',
            'descripcion': 'Cable UTP categoría 6, 305 metros, alta velocidad',
            'stock_actual': 30,
            'stock_minimo': 8,
            'unidad_medida': 'rollo',
            'precio_compra': Decimal('650.00'),
            'precio_venta': Decimal('950.00'),
            'ubicacion': 'Almacén A - Estante 1'
        },
        {
            'nombre': 'Conector RJ45',
            'codigo': 'CON-RJ45-100',
            'categoria': 'Cables y Conectores',
            'descripcion': 'Conector RJ45 estándar, paquete de 100 unidades',
            'stock_actual': 500,
            'stock_minimo': 100,
            'unidad_medida': 'paquete',
            'precio_compra': Decimal('120.00'),
            'precio_venta': Decimal('180.00'),
            'ubicacion': 'Almacén A - Estante 2'
        },
        {
            'nombre': 'Cable de Fibra Óptica Monomodo',
            'codigo': 'FO-MONO-1000M',
            'categoria': 'Cables y Conectores',
            'descripcion': 'Cable de fibra óptica monomodo, 1000 metros',
            'stock_actual': 5,
            'stock_minimo': 2,
            'unidad_medida': 'rollo',
            'precio_compra': Decimal('3500.00'),
            'precio_venta': Decimal('5000.00'),
            'ubicacion': 'Almacén B - Estante 1'
        },
        
        # Equipos de Red
        {
            'nombre': 'Router WiFi TP-Link Archer C6',
            'codigo': 'ROUT-TPL-C6',
            'categoria': 'Equipos de Red',
            'descripcion': 'Router WiFi dual band AC1200, ideal para clientes residenciales',
            'stock_actual': 25,
            'stock_minimo': 5,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('450.00'),
            'precio_venta': Decimal('650.00'),
            'ubicacion': 'Almacén C - Estante 1'
        },
        {
            'nombre': 'Switch 8 Puertos Gigabit',
            'codigo': 'SW-8P-GIG',
            'categoria': 'Equipos de Red',
            'descripcion': 'Switch no administrable de 8 puertos Gigabit',
            'stock_actual': 15,
            'stock_minimo': 3,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('350.00'),
            'precio_venta': Decimal('500.00'),
            'ubicacion': 'Almacén C - Estante 1'
        },
        {
            'nombre': 'Punto de Acceso WiFi Ubiquiti',
            'codigo': 'AP-UBI-AC',
            'categoria': 'Equipos de Red',
            'descripcion': 'Punto de acceso WiFi AC, para exteriores',
            'stock_actual': 10,
            'stock_minimo': 2,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('1200.00'),
            'precio_venta': Decimal('1800.00'),
            'ubicacion': 'Almacén C - Estante 2'
        },
        {
            'nombre': 'ONT GPON',
            'codigo': 'ONT-GPON-1',
            'categoria': 'Equipos de Red',
            'descripcion': 'Terminal de red óptica GPON para fibra',
            'stock_actual': 20,
            'stock_minimo': 5,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('800.00'),
            'precio_venta': Decimal('1200.00'),
            'ubicacion': 'Almacén C - Estante 2'
        },
        
        # Antenas y Accesorios
        {
            'nombre': 'Antena Direccional 2.4 GHz',
            'codigo': 'ANT-DIR-24',
            'categoria': 'Antenas y Accesorios',
            'descripcion': 'Antena direccional de 2.4 GHz, 24 dBi',
            'stock_actual': 12,
            'stock_minimo': 3,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('450.00'),
            'precio_venta': Decimal('650.00'),
            'ubicacion': 'Almacén D - Estante 1'
        },
        {
            'nombre': 'Antena Omnidireccional 5 GHz',
            'codigo': 'ANT-OMNI-5',
            'categoria': 'Antenas y Accesorios',
            'descripcion': 'Antena omnidireccional de 5 GHz, 15 dBi',
            'stock_actual': 8,
            'stock_minimo': 2,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('350.00'),
            'precio_venta': Decimal('500.00'),
            'ubicacion': 'Almacén D - Estante 1'
        },
        {
            'nombre': 'Soporte para Antena',
            'codigo': 'SOP-ANT-1',
            'categoria': 'Antenas y Accesorios',
            'descripcion': 'Soporte metálico para montaje de antena en poste',
            'stock_actual': 30,
            'stock_minimo': 10,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('150.00'),
            'precio_venta': Decimal('220.00'),
            'ubicacion': 'Almacén D - Estante 2'
        },
        
        # Herramientas de Instalación
        {
            'nombre': 'Ponchadora RJ45',
            'codigo': 'PON-RJ45',
            'categoria': 'Herramientas de Instalación',
            'descripcion': 'Ponchadora para conectores RJ45',
            'stock_actual': 5,
            'stock_minimo': 2,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('250.00'),
            'precio_venta': Decimal('380.00'),
            'ubicacion': 'Almacén E - Estante 1'
        },
        {
            'nombre': 'Pelacables',
            'codigo': 'PEL-CAB',
            'categoria': 'Herramientas de Instalación',
            'descripcion': 'Pelacables automático para cables de red',
            'stock_actual': 8,
            'stock_minimo': 2,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('180.00'),
            'precio_venta': Decimal('280.00'),
            'ubicacion': 'Almacén E - Estante 1'
        },
        {
            'nombre': 'Medidor de Señal WiFi',
            'codigo': 'MED-WIFI',
            'categoria': 'Herramientas de Instalación',
            'descripcion': 'Medidor portátil de señal WiFi',
            'stock_actual': 3,
            'stock_minimo': 1,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('1200.00'),
            'precio_venta': Decimal('1800.00'),
            'ubicacion': 'Almacén E - Estante 2'
        },
        
        # Materiales de Fijación
        {
            'nombre': 'Abrazaderas de Nylon',
            'codigo': 'ABR-NYL-100',
            'categoria': 'Materiales de Fijación',
            'descripcion': 'Abrazaderas de nylon, paquete de 100 unidades',
            'stock_actual': 200,
            'stock_minimo': 50,
            'unidad_medida': 'paquete',
            'precio_compra': Decimal('45.00'),
            'precio_venta': Decimal('70.00'),
            'ubicacion': 'Almacén F - Estante 1'
        },
        {
            'nombre': 'Grapas para Cable',
            'codigo': 'GRA-CAB-1000',
            'categoria': 'Materiales de Fijación',
            'descripcion': 'Grapas para fijar cable, caja de 1000 unidades',
            'stock_actual': 50,
            'stock_minimo': 10,
            'unidad_medida': 'caja',
            'precio_compra': Decimal('80.00'),
            'precio_venta': Decimal('120.00'),
            'ubicacion': 'Almacén F - Estante 1'
        },
        {
            'nombre': 'Canaleta PVC 20x10mm',
            'codigo': 'CAN-PVC-20',
            'categoria': 'Materiales de Fijación',
            'descripcion': 'Canaleta de PVC para cableado, 20x10mm, 2 metros',
            'stock_actual': 100,
            'stock_minimo': 20,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('25.00'),
            'precio_venta': Decimal('40.00'),
            'ubicacion': 'Almacén F - Estante 2'
        },
        {
            'nombre': 'Tubo Corrugado 1/2"',
            'codigo': 'TUB-COR-12',
            'categoria': 'Materiales de Fijación',
            'descripcion': 'Tubo corrugado de 1/2 pulgada, 25 metros',
            'stock_actual': 40,
            'stock_minimo': 10,
            'unidad_medida': 'rollo',
            'precio_compra': Decimal('180.00'),
            'precio_venta': Decimal('280.00'),
            'ubicacion': 'Almacén F - Estante 2'
        },
        
        # Accesorios de Fibra Óptica
        {
            'nombre': 'Conector SC Simplex',
            'codigo': 'CON-SC-SIM',
            'categoria': 'Accesorios de Fibra Óptica',
            'descripcion': 'Conector SC simplex para fibra óptica, paquete de 10',
            'stock_actual': 50,
            'stock_minimo': 10,
            'unidad_medida': 'paquete',
            'precio_compra': Decimal('350.00'),
            'precio_venta': Decimal('520.00'),
            'ubicacion': 'Almacén G - Estante 1'
        },
        {
            'nombre': 'Conector LC Duplex',
            'codigo': 'CON-LC-DUP',
            'categoria': 'Accesorios de Fibra Óptica',
            'descripcion': 'Conector LC duplex, paquete de 10',
            'stock_actual': 40,
            'stock_minimo': 10,
            'unidad_medida': 'paquete',
            'precio_compra': Decimal('450.00'),
            'precio_venta': Decimal('680.00'),
            'ubicacion': 'Almacén G - Estante 1'
        },
        {
            'nombre': 'Caja de Empalme Fibra',
            'codigo': 'CAJ-EMP-FO',
            'categoria': 'Accesorios de Fibra Óptica',
            'descripcion': 'Caja de empalme para fibra óptica, 12 empalmes',
            'stock_actual': 15,
            'stock_minimo': 3,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('280.00'),
            'precio_venta': Decimal('420.00'),
            'ubicacion': 'Almacén G - Estante 2'
        },
        
        # Accesorios de Cobre
        {
            'nombre': 'Panel de Parcheo 24 Puertos',
            'codigo': 'PAN-PAR-24',
            'categoria': 'Accesorios de Cobre',
            'descripcion': 'Panel de parcheo 24 puertos Cat 6',
            'stock_actual': 10,
            'stock_minimo': 2,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('450.00'),
            'precio_venta': Decimal('680.00'),
            'ubicacion': 'Almacén H - Estante 1'
        },
        {
            'nombre': 'Roseta de Pared',
            'codigo': 'ROS-PAR',
            'categoria': 'Accesorios de Cobre',
            'descripcion': 'Roseta de pared para cable de red',
            'stock_actual': 100,
            'stock_minimo': 20,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('25.00'),
            'precio_venta': Decimal('40.00'),
            'ubicacion': 'Almacén H - Estante 1'
        },
        
        # Protecciones y Reguladores
        {
            'nombre': 'Regulador de Voltaje 1000W',
            'codigo': 'REG-VOL-1000',
            'categoria': 'Protecciones y Reguladores',
            'descripcion': 'Regulador de voltaje 1000W para equipos',
            'stock_actual': 8,
            'stock_minimo': 2,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('350.00'),
            'precio_venta': Decimal('520.00'),
            'ubicacion': 'Almacén I - Estante 1'
        },
        {
            'nombre': 'UPS 600VA',
            'codigo': 'UPS-600VA',
            'categoria': 'Protecciones y Reguladores',
            'descripcion': 'UPS 600VA para protección de equipos',
            'stock_actual': 5,
            'stock_minimo': 1,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('850.00'),
            'precio_venta': Decimal('1280.00'),
            'ubicacion': 'Almacén I - Estante 1'
        },
        
        # Materiales de Seguridad
        {
            'nombre': 'Casco de Seguridad',
            'codigo': 'CAS-SEG',
            'categoria': 'Materiales de Seguridad',
            'descripcion': 'Casco de seguridad para trabajos en altura',
            'stock_actual': 20,
            'stock_minimo': 5,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('180.00'),
            'precio_venta': Decimal('280.00'),
            'ubicacion': 'Almacén J - Estante 1'
        },
        {
            'nombre': 'Guantes de Trabajo',
            'codigo': 'GUA-TRA',
            'categoria': 'Materiales de Seguridad',
            'descripcion': 'Guantes de trabajo resistentes, par',
            'stock_actual': 50,
            'stock_minimo': 10,
            'unidad_medida': 'par',
            'precio_compra': Decimal('45.00'),
            'precio_venta': Decimal('70.00'),
            'ubicacion': 'Almacén J - Estante 1'
        },
        
        # Equipos Pasivos
        {
            'nombre': 'Divisor de Señal 2 Salidas',
            'codigo': 'DIV-2SAL',
            'categoria': 'Equipos Pasivos',
            'descripcion': 'Divisor pasivo de señal, 2 salidas',
            'stock_actual': 25,
            'stock_minimo': 5,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('120.00'),
            'precio_venta': Decimal('180.00'),
            'ubicacion': 'Almacén K - Estante 1'
        },
        {
            'nombre': 'Atenuador 10 dB',
            'codigo': 'ATE-10DB',
            'categoria': 'Equipos Pasivos',
            'descripcion': 'Atenuador pasivo de 10 dB',
            'stock_actual': 15,
            'stock_minimo': 3,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('80.00'),
            'precio_venta': Decimal('120.00'),
            'ubicacion': 'Almacén K - Estante 1'
        },
        
        # Equipos Activos
        {
            'nombre': 'Amplificador de Señal WiFi',
            'codigo': 'AMP-WIFI',
            'categoria': 'Equipos Activos',
            'descripcion': 'Amplificador de señal WiFi, 2.4/5 GHz',
            'stock_actual': 12,
            'stock_minimo': 3,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('450.00'),
            'precio_venta': Decimal('680.00'),
            'ubicacion': 'Almacén L - Estante 1'
        },
        {
            'nombre': 'Repetidor WiFi',
            'codigo': 'REP-WIFI',
            'categoria': 'Equipos Activos',
            'descripcion': 'Repetidor WiFi para extender cobertura',
            'stock_actual': 18,
            'stock_minimo': 4,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('280.00'),
            'precio_venta': Decimal('420.00'),
            'ubicacion': 'Almacén L - Estante 1'
        },
        
        # Sistemas de Energía
        {
            'nombre': 'Batería 12V 7Ah',
            'codigo': 'BAT-12V-7AH',
            'categoria': 'Sistemas de Energía',
            'descripcion': 'Batería de 12V 7Ah para sistemas de respaldo',
            'stock_actual': 20,
            'stock_minimo': 5,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('350.00'),
            'precio_venta': Decimal('520.00'),
            'ubicacion': 'Almacén M - Estante 1'
        },
        {
            'nombre': 'Panel Solar 100W',
            'codigo': 'PAN-SOL-100W',
            'categoria': 'Sistemas de Energía',
            'descripcion': 'Panel solar de 100W para instalaciones remotas',
            'stock_actual': 5,
            'stock_minimo': 1,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('1800.00'),
            'precio_venta': Decimal('2700.00'),
            'ubicacion': 'Almacén M - Estante 2'
        },
        
        # Consumibles
        {
            'nombre': 'Alcohol Isopropílico',
            'codigo': 'ALC-ISO-500ML',
            'categoria': 'Consumibles',
            'descripcion': 'Alcohol isopropílico para limpieza de fibra, 500ml',
            'stock_actual': 30,
            'stock_minimo': 10,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('45.00'),
            'precio_venta': Decimal('70.00'),
            'ubicacion': 'Almacén N - Estante 1'
        },
        {
            'nombre': 'Toallitas de Limpieza para Fibra',
            'codigo': 'TOA-FIB-100',
            'categoria': 'Consumibles',
            'descripcion': 'Toallitas de limpieza para conectores de fibra, paquete de 100',
            'stock_actual': 25,
            'stock_minimo': 5,
            'unidad_medida': 'paquete',
            'precio_compra': Decimal('120.00'),
            'precio_venta': Decimal('180.00'),
            'ubicacion': 'Almacén N - Estante 1'
        },
        {
            'nombre': 'Etiquetas para Cable',
            'codigo': 'ETI-CAB-500',
            'categoria': 'Consumibles',
            'descripcion': 'Etiquetas autoadhesivas para identificación de cables, 500 unidades',
            'stock_actual': 40,
            'stock_minimo': 10,
            'unidad_medida': 'paquete',
            'precio_compra': Decimal('35.00'),
            'precio_venta': Decimal('55.00'),
            'ubicacion': 'Almacén N - Estante 2'
        },
        
        # Cajas y Gabinetes
        {
            'nombre': 'Caja de Distribución Externa',
            'codigo': 'CAJ-DIS-EXT',
            'categoria': 'Cajas y Gabinetes',
            'descripcion': 'Caja de distribución para exteriores, resistente a intemperie',
            'stock_actual': 15,
            'stock_minimo': 3,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('280.00'),
            'precio_venta': Decimal('420.00'),
            'ubicacion': 'Almacén O - Estante 1'
        },
        {
            'nombre': 'Gabinete de Red 19"',
            'codigo': 'GAB-RED-19',
            'categoria': 'Cajas y Gabinetes',
            'descripcion': 'Gabinete de red estándar 19 pulgadas, 42U',
            'stock_actual': 3,
            'stock_minimo': 1,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('3500.00'),
            'precio_venta': Decimal('5200.00'),
            'ubicacion': 'Almacén O - Estante 2'
        },
        
        # Sistemas de Cableado Estructurado
        {
            'nombre': 'Organizador de Cable',
            'codigo': 'ORG-CAB',
            'categoria': 'Sistemas de Cableado Estructurado',
            'descripcion': 'Organizador de cables para racks, paquete de 10',
            'stock_actual': 30,
            'stock_minimo': 5,
            'unidad_medida': 'paquete',
            'precio_compra': Decimal('120.00'),
            'precio_venta': Decimal('180.00'),
            'ubicacion': 'Almacén P - Estante 1'
        },
        
        # Equipos de Cliente
        {
            'nombre': 'Router WiFi Cliente',
            'codigo': 'ROUT-CLI-WIFI',
            'categoria': 'Equipos de Cliente',
            'descripcion': 'Router WiFi básico para clientes residenciales',
            'stock_actual': 40,
            'stock_minimo': 10,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('280.00'),
            'precio_venta': Decimal('420.00'),
            'ubicacion': 'Almacén Q - Estante 1'
        },
        {
            'nombre': 'Adaptador WiFi USB',
            'codigo': 'ADP-WIFI-USB',
            'categoria': 'Equipos de Cliente',
            'descripcion': 'Adaptador WiFi USB para computadoras',
            'stock_actual': 25,
            'stock_minimo': 5,
            'unidad_medida': 'pza',
            'precio_compra': Decimal('120.00'),
            'precio_venta': Decimal('180.00'),
            'ubicacion': 'Almacén Q - Estante 1'
        },
    ]
    
    creados = 0
    existentes = 0
    errores = 0
    
    for mat_data in materiales_data:
        nombre = mat_data['nombre']
        codigo = mat_data['codigo']
        categoria_nombre = mat_data.pop('categoria')
        
        try:
            # Obtener categoría
            categoria = categorias.get(categoria_nombre)
            if not categoria:
                print('  ⚠️  Categoría no encontrada: {}'.format(categoria_nombre))
                errores += 1
                continue
            
            # Verificar si el material ya existe
            material_existente = Material.objects.filter(codigo=codigo).first()
            if material_existente:
                print('  ⏭️  Ya existe: {} ({})'.format(nombre, codigo))
                existentes += 1
                continue
            
            # Crear material
            mat_data['categoria'] = categoria
            material = Material(**mat_data)
            material.actualizar_estado()  # Actualizar estado según stock
            material.save()
            
            print('  ✅ Creado: {} ({}) - Stock: {} {}'.format(
                nombre, codigo, material.stock_actual, material.get_unidad_medida_display()
            ))
            creados += 1
            
        except Exception as e:
            print('  ❌ Error al crear {}: {}'.format(nombre, str(e)))
            errores += 1
    
    # Resumen
    print('\n' + '='*70)
    print('\n✅ Materiales creados: {}'.format(creados))
    if existentes > 0:
        print('⏭️  Materiales existentes: {}'.format(existentes))
    if errores > 0:
        print('❌ Errores: {}'.format(errores))
    print('='*70)
    
    # Estadísticas finales
    total_materiales = Material.objects.count()
    print('\n📊 Total de materiales en inventario: {}'.format(total_materiales))
    print('✨ Proceso completado!\n')


if __name__ == '__main__':
    crear_materiales()

