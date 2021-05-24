# Generated by Django 2.2.7 on 2020-05-07 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('controlador', '0006_auto_20200501_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_controlador',
            name='analista_asignado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]