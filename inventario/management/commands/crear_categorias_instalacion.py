# -*- coding: utf-8 -*-
"""
Comando de gestión para crear categorías de materiales para instalación de internet.

Uso:
    python manage.py crear_categorias_instalacion
"""

from django.core.management.base import BaseCommand
from inventario.models import CategoriaMaterial


class Command(BaseCommand):
    help = 'Crea las categorías de materiales para un negocio de instalación de internet'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar la creación incluso si las categorías ya existen',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Creando categorías de materiales para instalación de internet...\n'))
        
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
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✅ Creada: {nombre}')
                    )
                    creadas += 1
                else:
                    if options['force']:
                        categoria.descripcion = descripcion
                        categoria.save()
                        self.stdout.write(
                            self.style.WARNING(f'  🔄 Actualizada: {nombre}')
                        )
                        creadas += 1
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'  ⏭️  Ya existe: {nombre}')
                        )
                        existentes += 1
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Error al crear {nombre}: {str(e)}')
                )
                errores += 1
        
        # Resumen
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n✅ Categorías creadas: {creadas}'))
        if existentes > 0:
            self.stdout.write(self.style.WARNING(f'⏭️  Categorías existentes: {existentes}'))
        if errores > 0:
            self.stdout.write(self.style.ERROR(f'❌ Errores: {errores}'))
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('\n✨ Proceso completado!\n'))

