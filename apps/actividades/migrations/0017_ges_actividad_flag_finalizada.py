# Generated by Django 2.2.7 on 2021-03-29 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0016_remove_ges_actividad_flag_fri'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_actividad',
            name='flag_finalizada',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
