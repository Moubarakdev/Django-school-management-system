# Generated by Django 4.1.1 on 2022-09-23 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0003_remove_result_practical_marks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='extra_marks',
            field=models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='note de rattrapage'),
        ),
    ]
