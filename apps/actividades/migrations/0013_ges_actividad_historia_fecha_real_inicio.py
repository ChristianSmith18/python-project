# Generated by Django 2.2.7 on 2021-01-15 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0012_ges_actividad_fecha_real_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_actividad_historia',
            name='fecha_real_inicio',
            field=models.DateField(blank=True, null=True),
        ),
    ]
