# Generated by Django 4.1.1 on 2022-09-28 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default='subscriber', max_length=50, verbose_name='Type de compte'),
        ),
        migrations.AlterField(
            model_name='user',
            name='requested_role',
            field=models.CharField(choices=[('subscriber', 'Abonné'), ('student', 'Étudiant'), ('teacher', 'Professeur'), ('editor', 'Editeur'), ('academic_officer', 'Direction Académique'), ('admin', 'Administrateur')], default='subscriber', max_length=50, verbose_name='Type de compte demandé'),
        ),
    ]
