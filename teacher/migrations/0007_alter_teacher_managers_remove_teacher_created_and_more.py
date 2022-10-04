# Generated by Django 4.1.1 on 2022-10-04 11:12

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teacher', '0006_alter_teacher_first_name_alter_teacher_last_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='teacher',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='created',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='email',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='id',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='modified',
        ),
        migrations.AddField(
            model_name='teacher',
            name='user_ptr',
            field=models.OneToOneField(auto_created=True, default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
