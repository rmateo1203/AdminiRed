# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0010_cliente_debe_cambiar_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalcliente',
            name='debe_cambiar_password',
            field=models.BooleanField(
                default=True,
                help_text='Indica si el cliente debe cambiar su contraseña en el próximo inicio de sesión',
                verbose_name='Debe cambiar contraseña'
            ),
        ),
    ]










