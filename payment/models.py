from datetime import timezone

from django.db import models, transaction
from django.urls import reverse
from model_utils.models import TimeStampedModel

from academic.models import Department, AcademicSession
from myschool import settings


# Create your models here.
class Invoice(models.Model):
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE, verbose_name="Étudiant")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, verbose_name="Année académique")
    balance_from_previous_session = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Clôturer")],
        default="active",
    )

    @property
    def statut(self):
        if self.status == 'active':
            return "Actif"
        else:
            return "Clôturer"

    class Meta:
        ordering = ["student", "session"]

    def __str__(self):
        return f"{self.student}"

    def total_amount_payable(self):
        return self.balance_from_previous_session + self.amount_payable()

    def balance(self):
        payable = self.total_amount_payable()
        paid = self.total_amount_paid()
        return payable - paid

    def amount_payable(self):
        items = InvoiceItem.objects.filter(invoice=self)
        total = 0
        for item in items:
            total += item.amount
        return total

    def total_amount_paid(self):
        receipts = Receipt.objects.filter(invoice=self)
        amount = 0
        for receipt in receipts:
            amount += receipt.amount_paid
        return amount

    def get_absolute_url(self):
        return reverse("payment:invoice_detail", kwargs={"pk": self.pk})


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.IntegerField(verbose_name="Montant")
    term1 = models.IntegerField(verbose_name="Première tranche")
    term2 = models.IntegerField(verbose_name="Deuxième tranche")
    term3 = models.IntegerField(verbose_name="Troisième tranche")
    term4 = models.IntegerField(verbose_name="Quatrième tranche")


class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.IntegerField(verbose_name="somme versée")
    date_paid = models.DateField(auto_now_add=True, verbose_name="Date de paiement")
    comment = models.CharField(max_length=200, blank=True, verbose_name="Commentaire")

    def __str__(self):
        return f"Receipt on {self.date_paid}"
