# Generated by Django 2.2.7 on 2020-05-25 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estado_seguimiento', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='glo_estadoseguimiento',
            name='estado',
        ),
    ]