# Generated by Django 2.2.7 on 2020-04-09 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_logeventos'),
    ]

    operations = [
        migrations.AddField(
            model_name='logeventos',
            name='metodo',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]