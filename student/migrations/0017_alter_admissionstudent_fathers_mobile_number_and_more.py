# Generated by Django 4.1.1 on 2022-10-11 15:55

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0016_alter_admissionstudent_fathers_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissionstudent',
            name='fathers_mobile_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Numéro de téléphone du père'),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='guardian_mobile_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Numéro Personne à prévenir'),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='mobile_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Numéro de téléphone'),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='mothers_mobile_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Numéro de téléphone de la mère'),
        ),
    ]
