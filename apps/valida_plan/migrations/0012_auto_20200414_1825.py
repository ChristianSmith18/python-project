# Generated by Django 2.2.7 on 2020-04-14 22:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('valida_plan', '0011_auto_20200414_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ges_observaciones',
            name='fecha_registro',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
