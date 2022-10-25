# Generated by Django 4.1.1 on 2022-10-11 15:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_alter_admissionstudent_religion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissionstudent',
            name='fathers_mobile_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Numéro de téléphone du père'),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='guardian_mobile_number',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Numéro Personne à prévenir'),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='mothers_mobile_number',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Numéro de téléphone de la mère'),
        ),
    ]