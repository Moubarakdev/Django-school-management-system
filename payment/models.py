from django.db import models
from model_utils.models import TimeStampedModel

from academic.models import Department, Semester, AcademicSession, Batch
from myschool import settings


# Create your models here.
class SchoolFees(TimeStampedModel):
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    ac_session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE,
        blank=True, null=True, verbose_name="Session académique"
    )
    semesters = models.ManyToManyField(Semester, blank=True, verbose_name="Semestres")
    fees_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Montant des frais")
    description = models.CharField(verbose_name="Description", max_length=50, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    def __str__(self):
        return self.description


class StudentFeesInfo(TimeStampedModel):
    student = models.OneToOneField('student.Student', on_delete=models.CASCADE,
                                   related_name='student_fee', verbose_name="Étudiant")
    fees = models.ForeignKey(SchoolFees, on_delete=models.DO_NOTHING, verbose_name="Montant de base")
    fee_to_pay = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Montant à payer", blank=True)
    paid_fee = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Montant payé", null=True, blank=True)
    owed_fee = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Montant restant", null=True,
                                   blank=True)

    def __str__(self):
        return f'{self.student__temporary_id} {self.student.admission_student__last_name}'


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
