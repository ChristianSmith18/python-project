# Generated by Django 2.2.7 on 2020-05-01 23:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_horas', '0004_auto_20200501_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ges_registro_horas',
            name='fecha_insercion',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]