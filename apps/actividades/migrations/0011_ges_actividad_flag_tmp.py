# Generated by Django 2.2.7 on 2021-01-11 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0010_auto_20200923_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_actividad',
            name='flag_tmp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
