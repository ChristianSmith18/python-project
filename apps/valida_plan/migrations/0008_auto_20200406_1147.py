# Generated by Django 2.2.7 on 2020-04-06 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('valida_plan', '0007_ges_observaciones_id_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ges_observaciones',
            name='id_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]