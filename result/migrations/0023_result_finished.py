# Generated by Django 4.1.1 on 2022-11-26 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0022_remove_result_created_at_remove_result_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='finished',
            field=models.BooleanField(blank=True, default=False, verbose_name='Terminé'),
        ),
    ]