# Generated by Django 2.2.7 on 2020-04-27 18:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('periodos', '0001_initial'),
        ('actividades', '0001_initial'),
        ('controlador', '0003_ges_controlador_jefatura_segundarevision'),
        ('valida_plan2', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ges_Observaciones',
            new_name='Ges_Observaciones_sr',
        ),
    ]