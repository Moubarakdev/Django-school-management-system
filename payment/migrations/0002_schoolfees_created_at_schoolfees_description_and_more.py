# Generated by Django 4.1.1 on 2022-10-05 10:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolfees',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Créer le'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolfees',
            name='description',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='schoolfees',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modifier le'),
        ),
    ]