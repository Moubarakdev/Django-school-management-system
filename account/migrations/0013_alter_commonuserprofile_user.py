# Generated by Django 4.1.1 on 2022-10-23 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_remove_commonuserprofile_headline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonuserprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
        ),
    ]