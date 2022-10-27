from datetime import timezone

from django.db import models, transaction
from django.urls import reverse
from model_utils.models import TimeStampedModel

from academic.models import Department, AcademicSession, AcademicTerm
from myschool import settings


# Create your models here.
class Invoice(models.Model):
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE, verbose_name="Étudiant")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, verbose_name="Année académique")
    balance_from_previous_session = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Closed")],
        default="active",
    )

    class Meta:
        ordering = ["student", "session"]
        unique_together = ['student', 'session']

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

    def save(self, *args, **kwargs):
        self.term1 = (self.amount * 30) / 100
        self.term2 = (self.amount * 30) / 100
        self.term3 = (self.amount * 20) / 100
        self.term4 = (self.amount * 20) / 100

        super().save(*args, **kwargs)


class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.IntegerField(verbose_name="somme versée")
    date_paid = models.DateField(auto_now_add=True, verbose_name="Date de paiement")
    comment = models.CharField(max_length=200, blank=True, verbose_name="Commentaire")

    def __str__(self):
        return f"Receipt on {self.date_paid}"

    def save(self, *args, **kwargs):
        # TODO: update terms after a payment
        item = InvoiceItem.objects.get(invoice=self.invoice)
        #  Algo de gestion des tranches
        if item.term1 >= self.amount_paid:
            item.term1 -= self.amount_paid
        elif item.term1 < self.amount_paid:
            rest = self.amount_paid - item.term1
            item.term1 = 0
            if rest <= item.term2:
                item.term2 -= rest
            elif rest > item.term2:
                rest2 = rest - item.term2
                item.term2 = 0
                if rest2 <= item.term3:
                    item.term3 -= rest2
                elif rest2 > item.term3:
                    rest3 = rest2 - item.term3
                    item.term3 = 0
                    if rest3 <= item.term4:
                        item.term4 -= rest3
                    else:
                        item.term4 = 0
        item.save()
        return super().save(*args, **kwargs)
