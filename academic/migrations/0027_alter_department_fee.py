# Generated by Django 4.1.1 on 2022-10-13 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0026_department_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='fee',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Frais de scolarité'),
        ),
    ]
