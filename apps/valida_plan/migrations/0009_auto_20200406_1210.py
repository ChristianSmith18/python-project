# Generated by Django 2.2.7 on 2020-04-06 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('valida_plan', '0008_auto_20200406_1147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ges_observaciones',
            old_name='id_user',
            new_name='user_observa',
        ),
    ]
