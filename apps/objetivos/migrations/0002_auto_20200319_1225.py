# Generated by Django 2.2.7 on 2020-03-19 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objetivos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_objetivo_estrategico',
            name='transversal',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='ges_objetivo_operativo',
            name='transversal',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='ges_objetivo_tactico',
            name='transversal',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='ges_objetivo_tacticotn',
            name='transversal',
            field=models.BooleanField(default=False, null=True),
        ),
    ]