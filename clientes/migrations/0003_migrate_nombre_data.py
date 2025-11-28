# Generated migration to split nombre field data

from django.db import migrations


def split_nombre_data(apps, schema_editor):
    """Migra los datos del campo nombre completo a nombre, apellido1 y apellido2."""
    Cliente = apps.get_model('clientes', 'Cliente')
    
    for cliente in Cliente.objects.all():
        # Si apellido1 está vacío (valor por defecto), significa que necesitamos migrar
        if not cliente.apellido1:
            nombre_completo = cliente.nombre.strip()
            partes = nombre_completo.split()
            
            if len(partes) == 1:
                # Solo hay un nombre, lo dejamos en nombre
                cliente.nombre = partes[0]
                cliente.apellido1 = ''
            elif len(partes) == 2:
                # Nombre y un apellido
                cliente.nombre = partes[0]
                cliente.apellido1 = partes[1]
            else:
                # Nombre y dos o más apellidos
                cliente.nombre = partes[0]
                cliente.apellido1 = partes[1]
                # Si hay más de 2 partes, unimos las restantes en apellido2
                if len(partes) > 2:
                    cliente.apellido2 = ' '.join(partes[2:])
            
            cliente.save()


def reverse_split_nombre_data(apps, schema_editor):
    """Revierte la migración, uniendo nombre, apellido1 y apellido2 en nombre."""
    Cliente = apps.get_model('clientes', 'Cliente')
    
    for cliente in Cliente.objects.all():
        nombre_completo = cliente.nombre
        if cliente.apellido1:
            nombre_completo += f" {cliente.apellido1}"
        if cliente.apellido2:
            nombre_completo += f" {cliente.apellido2}"
        cliente.nombre = nombre_completo.strip()
        cliente.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_split_nombre_field'),
    ]

    operations = [
        migrations.RunPython(split_nombre_data, reverse_split_nombre_data),
    ]

