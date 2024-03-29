# Generated by Django 4.1.1 on 2022-09-26 22:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonuserprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Créer le'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commonuserprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modifier le'),
        ),
        migrations.AddField(
            model_name='sociallink',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Créer le'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sociallink',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modifier le'),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Créer le'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modifier le'),
        ),
    ]
