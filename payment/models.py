from django.db import models
from model_utils.models import TimeStampedModel

from student.models import Student


# Create your models here.
class Payment(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, verbose_name="Etudiant")
    payment_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    payement_date = models.DateTimeField(verbose_name="Date de paiement", auto_now=True)
