# Generated by Django 4.1.1 on 2022-11-14 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0033_alter_academicsession_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='hourly_volume',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Volume horaire'),
        ),
    ]