# Generated by Django 4.1.1 on 2022-09-28 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_user_approval_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='employee_or_student_id',
            field=models.CharField(blank=True, help_text='seulement si vous êtes déjà Étudiant', max_length=10, null=True, verbose_name='Matricule'),
        ),
    ]
