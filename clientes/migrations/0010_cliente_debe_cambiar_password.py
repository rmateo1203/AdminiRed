# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0009_alter_cliente_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='debe_cambiar_password',
            field=models.BooleanField(
                default=True,
                help_text='Indica si el cliente debe cambiar su contraseña en el próximo inicio de sesión',
                verbose_name='Debe cambiar contraseña'
            ),
        ),
    ]

