# Generated by Django 4.0 on 2022-11-24 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0005_alter_contrato_initdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='type',
            field=models.CharField(choices=[('COMERCIANTE LOCAL', 'comerciante local'), ('COMERCIANTE EXTRANJERO', 'comerciante extranjero'), ('CONSULTOR', 'consultor'), ('PRODUCTOR', 'productor')], default='COMERCIANTE LOCAL', max_length=30),
        ),
    ]
