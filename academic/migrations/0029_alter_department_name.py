# Generated by Django 4.1.1 on 2022-10-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0028_alter_department_options_alter_department_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nom de la filière'),
        ),
    ]