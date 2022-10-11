# Generated by Django 4.1.1 on 2022-10-11 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0023_alter_academicterm_current_alter_academicterm_name'),
        ('payment', '0017_alter_invoice_semesters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.academicterm', verbose_name='Période'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='amount_paid',
            field=models.IntegerField(verbose_name='somme versée'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='comment',
            field=models.CharField(blank=True, max_length=200, verbose_name='Commentaire'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='date_paid',
            field=models.DateField(auto_now_add=True, verbose_name='Date de paiement'),
        ),
    ]
