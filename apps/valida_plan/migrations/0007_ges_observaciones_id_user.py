# Generated by Django 2.2.7 on 2020-04-06 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('valida_plan', '0006_remove_ges_observaciones_id_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_observaciones',
            name='id_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
