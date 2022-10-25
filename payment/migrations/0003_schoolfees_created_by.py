# Generated by Django 4.1.1 on 2022-10-05 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0002_schoolfees_created_at_schoolfees_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolfees',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]