# Generated by Django 2.2.7 on 2020-05-28 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('periodos', '0004_auto_20200528_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glo_seguimiento',
            name='fecha_inicio',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
