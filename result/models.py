from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from django.urls import reverse

from student.models import Student
from academic.models import Subject, Department

'''class Exam(TimeStampedModel):
    EXAM_CHOICES = (
        ('d', 'Devoir'),
        ('e', 'Examen'),
        ('r', 'Rattrapage'),
    )
    exam_name = models.CharField(
        max_length=1,
        choices=EXAM_CHOICES, verbose_name='titre de l\'examen'
    )
    exam_date = models.DateTimeField(verbose_name="Date examen")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifier le")

    def __str__(self):
        return f'{self.get_exam_name_display()} - \
            {self.exam_date.year}'

'''


class Result(TimeStampedModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='results'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )
    class_marks = models.FloatField(
        blank=True, default=0,
        null=True, verbose_name="Note de classe"
    )
    exam_marks = models.FloatField(
        blank=True, default=0,
        null=True, verbose_name="Note d'examen"
    )
    extra_marks = models.FloatField(
        blank=True, default=0,
        null=True, verbose_name='note de rattrapage'
    )
    total_marks = models.FloatField(
        blank=True, default=0,
        null=True, verbose_name="Total"
    )
    average = models.FloatField(
        blank=True, default=0,
        null=True, verbose_name='moyenne'
    )
    validated = models.BooleanField(
        blank=True,
        default="False",
        verbose_name="Validé ?"
    )
    finished = models.BooleanField(
        blank=True,
        default=False,
        verbose_name="Terminé"
    )

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f'{self.student} | {self.subject} | {self.total_marks}'

    @property
    def validated_or_not(self):
        return "validé" if self.validated else "non validé"

    def save(self, *args, **kwargs):
        if self.class_marks and self.exam_marks:
            self.total_marks = self.class_marks + self.exam_marks
        elif self.class_marks and not self.exam_marks:
            self.total_marks = self.class_marks
        else:
            self.total_marks = self.exam_marks
        self.average = self.total_marks / 2
        if self.extra_marks:
            if self.average < self.extra_marks:
                self.average = self.extra_marks

        if self.average >= 10:
            self.validated = True
        else:
            self.validated = False
        super().save(*args, **kwargs)


def create_resource():
    return reverse('result:create_subject_group')


class SubjectGroup(TimeStampedModel):
    """ Keep track of group of subjects that belongs to a
    department
    """
    department = models.ForeignKey(
        Department,
        related_name='subjects',
        on_delete=models.DO_NOTHING, verbose_name='filière'
    )
    subjects = models.ManyToManyField(Subject, blank=True, verbose_name='matières')

    def __str__(self):
        return f'{self.department}'

    def get_subjects(self):
        return " | ".join([str(sg) for sg in self.subjects.all()])
