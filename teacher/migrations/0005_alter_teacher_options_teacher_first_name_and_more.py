# Generated by Django 4.1.1 on 2022-09-15 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_alter_teacher_options_remove_teacher_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['joining_date', 'first_name']},
        ),
        migrations.AddField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(max_length=150, null=True, verbose_name='nom'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(max_length=150, null=True, verbose_name='prénom'),
        ),
    ]