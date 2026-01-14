"""
Comando de gestión para crear roles y permisos iniciales del sistema.

Uso:
    python manage.py crear_roles_permisos_iniciales
"""
from django.core.management.base import BaseCommand
from core.models import Rol, Permiso, PermisoRol


class Command(BaseCommand):
    help = 'Crea roles y permisos iniciales del sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando roles y permisos iniciales...'))
        
        # =====================================================================
        # CREAR ROLES
        # =====================================================================
        
        roles_data = [
            {
                'codigo': 'administrador',
                'nombre': 'Administrador',
                'descripcion': 'Acceso completo al sistema. Puede gestionar todos los módulos y configuraciones.',
                'es_sistema': True,
            },
            {
                'codigo': 'supervisor',
                'nombre': 'Supervisor',
                'descripcion': 'Puede supervisar y gestionar la mayoría de operaciones, excepto configuraciones críticas del sistema.',
                'es_sistema': True,
            },
            {
                'codigo': 'instalador',
                'nombre': 'Instalador',
                'descripcion': 'Puede gestionar instalaciones y realizar trabajos técnicos.',
                'es_sistema': True,
            },
            {
                'codigo': 'tecnico',
                'nombre': 'Técnico',
                'descripcion': 'Puede realizar trabajos técnicos y ver información relevante.',
                'es_sistema': True,
            },
            {
                'codigo': 'cliente',
                'nombre': 'Cliente',
                'descripcion': 'Usuario cliente con acceso al portal. Solo puede ver sus propios datos (pagos, servicios).',
                'es_sistema': True,
            },
        ]
        
        roles_creados = {}
        for rol_data in roles_data:
            rol, created = Rol.objects.get_or_create(
                codigo=rol_data['codigo'],
                defaults=rol_data
            )
            roles_creados[rol_data['codigo']] = rol
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Rol creado: {rol.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Rol ya existe: {rol.nombre}'))
        
        # =====================================================================
        # CREAR PERMISOS
        # =====================================================================
        
        permisos_data = [
            # Permisos de Clientes
            {'codigo': 'ver_clientes', 'nombre': 'Ver Clientes', 'categoria': 'clientes',
             'descripcion': 'Permite ver la lista y detalles de clientes'},
            {'codigo': 'crear_clientes', 'nombre': 'Crear Clientes', 'categoria': 'clientes',
             'descripcion': 'Permite crear nuevos clientes'},
            {'codigo': 'editar_clientes', 'nombre': 'Editar Clientes', 'categoria': 'clientes',
             'descripcion': 'Permite editar información de clientes'},
            {'codigo': 'eliminar_clientes', 'nombre': 'Eliminar Clientes', 'categoria': 'clientes',
             'descripcion': 'Permite eliminar clientes'},
            {'codigo': 'gestionar_portal_clientes', 'nombre': 'Gestionar Portal de Clientes', 'categoria': 'clientes',
             'descripcion': 'Permite gestionar acceso y credenciales del portal de clientes'},
            
            # Permisos de Instalaciones
            {'codigo': 'ver_instalaciones', 'nombre': 'Ver Instalaciones', 'categoria': 'instalaciones',
             'descripcion': 'Permite ver la lista y detalles de instalaciones'},
            {'codigo': 'crear_instalaciones', 'nombre': 'Crear Instalaciones', 'categoria': 'instalaciones',
             'descripcion': 'Permite crear nuevas instalaciones'},
            {'codigo': 'editar_instalaciones', 'nombre': 'Editar Instalaciones', 'categoria': 'instalaciones',
             'descripcion': 'Permite editar información de instalaciones'},
            {'codigo': 'eliminar_instalaciones', 'nombre': 'Eliminar Instalaciones', 'categoria': 'instalaciones',
             'descripcion': 'Permite eliminar instalaciones'},
            {'codigo': 'gestionar_materiales_instalacion', 'nombre': 'Gestionar Materiales de Instalación', 'categoria': 'instalaciones',
             'descripcion': 'Permite gestionar materiales asignados a instalaciones'},
            
            # Permisos de Pagos
            {'codigo': 'ver_pagos', 'nombre': 'Ver Pagos', 'categoria': 'pagos',
             'descripcion': 'Permite ver la lista y detalles de pagos'},
            {'codigo': 'crear_pagos', 'nombre': 'Crear Pagos', 'categoria': 'pagos',
             'descripcion': 'Permite crear nuevos pagos'},
            {'codigo': 'editar_pagos', 'nombre': 'Editar Pagos', 'categoria': 'pagos',
             'descripcion': 'Permite editar información de pagos'},
            {'codigo': 'eliminar_pagos', 'nombre': 'Eliminar Pagos', 'categoria': 'pagos',
             'descripcion': 'Permite eliminar pagos'},
            {'codigo': 'marcar_pagos_pagados', 'nombre': 'Marcar Pagos como Pagados', 'categoria': 'pagos',
             'descripcion': 'Permite marcar pagos como pagados'},
            {'codigo': 'capturar_pagos_manuales', 'nombre': 'Capturar Pagos Manuales', 'categoria': 'pagos',
             'descripcion': 'Permite capturar pagos realizados por transferencia/depósito'},
            {'codigo': 'reembolsar_pagos', 'nombre': 'Reembolsar Pagos', 'categoria': 'pagos',
             'descripcion': 'Permite reembolsar pagos'},
            {'codigo': 'ver_reportes_pagos', 'nombre': 'Ver Reportes de Pagos', 'categoria': 'pagos',
             'descripcion': 'Permite ver reportes y estadísticas de pagos'},
            
            # Permisos de Inventario
            {'codigo': 'ver_inventario', 'nombre': 'Ver Inventario', 'categoria': 'inventario',
             'descripcion': 'Permite ver el inventario de materiales'},
            {'codigo': 'gestionar_inventario', 'nombre': 'Gestionar Inventario', 'categoria': 'inventario',
             'descripcion': 'Permite crear, editar y eliminar materiales del inventario'},
            {'codigo': 'registrar_movimientos_inventario', 'nombre': 'Registrar Movimientos de Inventario', 'categoria': 'inventario',
             'descripcion': 'Permite registrar entradas, salidas y ajustes de inventario'},
            
            # Permisos de Notificaciones
            {'codigo': 'ver_notificaciones', 'nombre': 'Ver Notificaciones', 'categoria': 'notificaciones',
             'descripcion': 'Permite ver notificaciones del sistema'},
            {'codigo': 'gestionar_notificaciones', 'nombre': 'Gestionar Notificaciones', 'categoria': 'notificaciones',
             'descripcion': 'Permite crear y gestionar notificaciones'},
            {'codigo': 'configurar_notificaciones', 'nombre': 'Configurar Notificaciones', 'categoria': 'notificaciones',
             'descripcion': 'Permite configurar notificaciones automáticas'},
            
            # Permisos del Sistema
            {'codigo': 'gestionar_roles_permisos', 'nombre': 'Gestionar Roles y Permisos', 'categoria': 'sistema',
             'descripcion': 'Permite gestionar roles y permisos del sistema'},
            {'codigo': 'gestionar_usuarios', 'nombre': 'Gestionar Usuarios', 'categoria': 'sistema',
             'descripcion': 'Permite gestionar usuarios del sistema'},
            {'codigo': 'configurar_sistema', 'nombre': 'Configurar Sistema', 'categoria': 'sistema',
             'descripcion': 'Permite configurar parámetros del sistema (logo, colores, etc.)'},
            {'codigo': 'ver_reportes_generales', 'nombre': 'Ver Reportes Generales', 'categoria': 'sistema',
             'descripcion': 'Permite ver reportes y estadísticas generales del sistema'},
        ]
        
        permisos_creados = {}
        for permiso_data in permisos_data:
            permiso, created = Permiso.objects.get_or_create(
                codigo=permiso_data['codigo'],
                defaults=permiso_data
            )
            permisos_creados[permiso_data['codigo']] = permiso
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Permiso creado: {permiso.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Permiso ya existe: {permiso.nombre}'))
        
        # =====================================================================
        # ASIGNAR PERMISOS A ROLES
        # =====================================================================
        
        self.stdout.write(self.style.SUCCESS('\nAsignando permisos a roles...'))
        
        # Administrador: Todos los permisos
        rol_admin = roles_creados['administrador']
        for permiso in permisos_creados.values():
            PermisoRol.objects.get_or_create(rol=rol_admin, permiso=permiso)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Permisos asignados a: {rol_admin.nombre}'))
        
        # Supervisor: La mayoría de permisos excepto configuración del sistema
        rol_supervisor = roles_creados['supervisor']
        permisos_supervisor = [
            'ver_clientes', 'crear_clientes', 'editar_clientes', 'gestionar_portal_clientes',
            'ver_instalaciones', 'crear_instalaciones', 'editar_instalaciones', 'gestionar_materiales_instalacion',
            'ver_pagos', 'crear_pagos', 'editar_pagos', 'marcar_pagos_pagados', 'capturar_pagos_manuales', 'ver_reportes_pagos',
            'ver_inventario', 'gestionar_inventario', 'registrar_movimientos_inventario',
            'ver_notificaciones', 'gestionar_notificaciones', 'configurar_notificaciones',
            'ver_reportes_generales',
        ]
        for codigo_permiso in permisos_supervisor:
            if codigo_permiso in permisos_creados:
                PermisoRol.objects.get_or_create(rol=rol_supervisor, permiso=permisos_creados[codigo_permiso])
        self.stdout.write(self.style.SUCCESS(f'  ✓ Permisos asignados a: {rol_supervisor.nombre}'))
        
        # Instalador: Permisos relacionados con instalaciones
        rol_instalador = roles_creados['instalador']
        permisos_instalador = [
            'ver_clientes',  # Para ver datos del cliente
            'ver_instalaciones', 'crear_instalaciones', 'editar_instalaciones', 'gestionar_materiales_instalacion',
            'ver_pagos',  # Para ver información de pagos relacionada
            'ver_inventario', 'registrar_movimientos_inventario',  # Para registrar uso de materiales
            'ver_notificaciones',
        ]
        for codigo_permiso in permisos_instalador:
            if codigo_permiso in permisos_creados:
                PermisoRol.objects.get_or_create(rol=rol_instalador, permiso=permisos_creados[codigo_permiso])
        self.stdout.write(self.style.SUCCESS(f'  ✓ Permisos asignados a: {rol_instalador.nombre}'))
        
        # Técnico: Permisos básicos
        rol_tecnico = roles_creados['tecnico']
        permisos_tecnico = [
            'ver_clientes',
            'ver_instalaciones', 'editar_instalaciones',  # Solo editar, no crear
            'ver_pagos',
            'ver_inventario',
            'ver_notificaciones',
        ]
        for codigo_permiso in permisos_tecnico:
            if codigo_permiso in permisos_creados:
                PermisoRol.objects.get_or_create(rol=rol_tecnico, permiso=permisos_creados[codigo_permiso])
        self.stdout.write(self.style.SUCCESS(f'  ✓ Permisos asignados a: {rol_tecnico.nombre}'))
        
        # =====================================================================
        # RESUMEN
        # =====================================================================
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('RESUMEN'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'Roles creados: {len(roles_creados)}'))
        self.stdout.write(self.style.SUCCESS(f'Permisos creados: {len(permisos_creados)}'))
        self.stdout.write(self.style.SUCCESS('\n✓ Sistema de roles y permisos configurado correctamente!'))
        self.stdout.write(self.style.SUCCESS('\nPuedes gestionar roles y permisos desde: /admin/core/'))

