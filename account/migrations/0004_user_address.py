# Generated by Django 4.1.1 on 2022-09-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_commonuserprofile_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Adresse'),
        ),
    ]