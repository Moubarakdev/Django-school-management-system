# Generated by Django 4.1.1 on 2022-09-15 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_remove_teacher_designation_delete_designation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={},
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='name',
        ),
    ]
