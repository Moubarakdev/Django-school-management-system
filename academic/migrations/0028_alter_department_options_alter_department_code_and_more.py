# Generated by Django 4.1.1 on 2022-10-14 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0027_alter_department_fee'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name_plural': 'Filières'},
        ),
        migrations.AlterField(
            model_name='department',
            name='code',
            field=models.PositiveIntegerField(verbose_name='Code filière '),
        ),
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.TextField(blank=True, help_text='Ecriver une simple description a propos de la filière', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nom de la filière'),
        ),
    ]
