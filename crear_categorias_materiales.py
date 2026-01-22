#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para crear categorías de materiales para instalación de internet.

Uso:
    python crear_categorias_materiales.py
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from inventario.models import CategoriaMaterial


def crear_categorias():
    """Crea las categorías de materiales para instalación de internet."""
    
    print('🚀 Creando categorías de materiales para instalación de internet...\n')
    
    # Definir categorías con sus descripciones
    categorias = [
        {
            'nombre': 'Cables y Conectores',
            'descripcion': 'Cables de red (UTP, STP), cables de fibra óptica, conectores RJ45, conectores de fibra, cables coaxiales, etc.'
        },
        {
            'nombre': 'Equipos de Red',
            'descripcion': 'Routers, switches, puntos de acceso WiFi, módems, ONT (Optical Network Terminal), gateways, etc.'
        },
        {
            'nombre': 'Antenas y Accesorios',
            'descripcion': 'Antenas direccionales, omnidireccionales, sectoriales, soportes para antenas, cables de antena, etc.'
        },
        {
            'nombre': 'Herramientas de Instalación',
            'descripcion': 'Ponchadoras, crimpeadoras, pelacables, medidores de señal, OTDR, fusionadoras de fibra, etc.'
        },
        {
            'nombre': 'Materiales de Fijación',
            'descripcion': 'Abrazaderas, grapas, tornillos, tarugos, soportes para cable, canaletas, tubos corrugados, etc.'
        },
        {
            'nombre': 'Equipos de Medición',
            'descripcion': 'Medidores de velocidad, analizadores de red, medidores de señal WiFi, probadores de cable, etc.'
        },
        {
            'nombre': 'Accesorios de Fibra Óptica',
            'descripcion': 'Empalmes de fibra, conectores SC/LC/FC, adaptadores, protectores, cajas de empalme, etc.'
        },
        {
            'nombre': 'Accesorios de Cobre',
            'descripcion': 'Conectores RJ45, paneles de parcheo, rosetas, bases de datos, protectores de sobretensión, etc.'
        },
        {
            'nombre': 'Protecciones y Reguladores',
            'descripcion': 'Reguladores de voltaje, UPS, protectores de sobretensión, supresores de picos, etc.'
        },
        {
            'nombre': 'Materiales de Seguridad',
            'descripcion': 'Cascos, guantes, arneses, señalamientos, cintas de seguridad, etc.'
        },
        {
            'nombre': 'Equipos Pasivos',
            'descripcion': 'Divisores, acopladores, atenuadores, filtros, amplificadores pasivos, etc.'
        },
        {
            'nombre': 'Equipos Activos',
            'descripcion': 'Amplificadores de señal, repetidores, extensores de rango, boosters, etc.'
        },
        {
            'nombre': 'Sistemas de Energía',
            'descripcion': 'Baterías, paneles solares, inversores, sistemas de respaldo, etc.'
        },
        {
            'nombre': 'Materiales de Construcción',
            'descripcion': 'Postes, torres, estructuras metálicas, bases de concreto, etc.'
        },
        {
            'nombre': 'Consumibles',
            'descripcion': 'Alcohol isopropílico, toallitas de limpieza, gel de fibra, etiquetas, marcadores, etc.'
        },
        {
            'nombre': 'Cajas y Gabinetes',
            'descripcion': 'Cajas de distribución, gabinetes de red, racks, paneles de pared, etc.'
        },
        {
            'nombre': 'Sistemas de Cableado Estructurado',
            'descripcion': 'Paneles de parcheo, organizadores de cable, sistemas de gestión de cables, etc.'
        },
        {
            'nombre': 'Equipos de Cliente',
            'descripcion': 'Routers para cliente, adaptadores WiFi, módems USB, etc.'
        },
    ]
    
    creadas = 0
    existentes = 0
    errores = 0
    
    for categoria_data in categorias:
        nombre = categoria_data['nombre']
        descripcion = categoria_data['descripcion']
        
        try:
            categoria, created = CategoriaMaterial.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion}
            )
            
            if created:
                print('  ✅ Creada: {}'.format(nombre))
                creadas += 1
            else:
                # Actualizar descripción si ya existe
                if categoria.descripcion != descripcion:
                    categoria.descripcion = descripcion
                    categoria.save()
                    print('  🔄 Actualizada: {}'.format(nombre))
                    creadas += 1
                else:
                    print('  ⏭️  Ya existe: {}'.format(nombre))
                    existentes += 1
                    
        except Exception as e:
            print('  ❌ Error al crear {}: {}'.format(nombre, str(e)))
            errores += 1
    
    # Resumen
    print('\n' + '='*60)
    print('\n✅ Categorías creadas/actualizadas: {}'.format(creadas))
    if existentes > 0:
        print('⏭️  Categorías existentes: {}'.format(existentes))
    if errores > 0:
        print('❌ Errores: {}'.format(errores))
    print('='*60)
    print('\n✨ Proceso completado!\n')


if __name__ == '__main__':
    crear_categorias()

