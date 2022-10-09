from datetime import timezone

from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel

from academic.models import Department, Semester, AcademicSession, Batch, AcademicTerm
from myschool import settings
from student.models import Student


# Create your models here.
class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Étudiant")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, verbose_name="Année académique")
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, verbose_name="Tranche")
    semesters = models.ManyToManyField(Semester, null=True, blank=False, related_name='semesters', verbose_name="Semestres")
    balance_from_previous_term = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Closed")],
        default="active",
    )

    class Meta:
        ordering = ["student", "term"]

    def __str__(self):
        return f"{self.student}"

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

    def total_amount_payable(self):
        return self.balance_from_previous_term + self.amount_payable()

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
    amount = models.IntegerField()


class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.IntegerField(verbose_name="somme versée")
    date_paid = models.DateField(auto_now_add=True, verbose_name="Date de paiement")
    comment = models.CharField(max_length=200, blank=True, verbose_name="Commentaire")

    def __str__(self):
        return f"Receipt on {self.date_paid}"


'''  
def save(self, *args, **kwargs):
      self.fee_to_pay = self.fees.fees_amount
      super().save(*args, **kwargs)
'''

'''class Payment(TimeStampedModel):
    student = models.ForeignKey(StudentFeesInfo, on_delete=models.DO_NOTHING, verbose_name="Etudiant")
    payment_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    payement_date = models.DateTimeField(verbose_name="Date de paiement", auto_now_add=True)'''
