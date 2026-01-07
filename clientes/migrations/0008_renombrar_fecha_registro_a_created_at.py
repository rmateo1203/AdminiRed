# Generated manually
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0007_agregar_campo_usuario_portal'),
    ]

    operations = [
        # Renombrar campos en el modelo Cliente
        migrations.RenameField(
            model_name='cliente',
            old_name='fecha_registro',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='fecha_actualizacion',
            new_name='updated_at',
        ),
        # Renombrar campos en el modelo HistoricalCliente (django-simple-history)
        migrations.RenameField(
            model_name='historicalcliente',
            old_name='fecha_registro',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='historicalcliente',
            old_name='fecha_actualizacion',
            new_name='updated_at',
        ),
    ]

