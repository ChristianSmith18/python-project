# Generated by Django 2.2.7 on 2020-05-25 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Glo_EstadoPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField()),
                ('descripcion_estado', models.CharField(max_length=100)),
            ],
        ),
    ]
