# Generated by Django 4.1.1 on 2022-09-28 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_user_role_alter_user_requested_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='approval_status',
            field=models.CharField(choices=[('n', "Aucune demande d'approbation"), ('p', 'Demande d’approbation en attente'), ('d', 'Demande d’approbation refusée'), ('a', 'Vérifié')], default='p', max_length=2),
        ),
    ]