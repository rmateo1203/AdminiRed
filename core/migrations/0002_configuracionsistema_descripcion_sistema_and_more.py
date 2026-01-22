# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracionsistema',
            name='descripcion_sistema',
            field=models.CharField(default='Sistema para el control total de instalaciones de internet', help_text='Descripción corta que aparecerá como subtítulo en el home y footer', max_length=200, verbose_name='Descripción del sistema'),
        ),
        migrations.AddField(
            model_name='configuracionsistema',
            name='titulo_sistema',
            field=models.CharField(blank=True, help_text='Título del sistema. Si está vacío, se usará el nombre de la empresa', max_length=100, null=True, verbose_name='Título del sistema (opcional)'),
        ),
    ]







