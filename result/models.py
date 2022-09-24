from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from django.urls import reverse

from student.models import Student
from academic.models import Subject, Semester, Department


class Exam(TimeStampedModel):
    EXAM_CHOICES = (
        ('d', 'Devoir'),
        ('e', 'Examen'),
        ('r', 'Rattrapage'),
    )
    exam_name = models.CharField(
        max_length=1,
        choices=EXAM_CHOICES, verbose_name='nom de l\'examen'
    )
    exam_date = models.DateTimeField(verbose_name="Date examen")

    def __str__(self):
        return f'{self.get_exam_name_display()} - \
            {self.exam_date.year}'


class Result(TimeStampedModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='results', verbose_name='étudiant'
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE, verbose_name='semestre'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE, verbose_name='matière'
    )
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE,
        blank=True, null=True, verbose_name='examen'
    )
    class_marks = models.FloatField(
        blank=True,
        null=True, verbose_name='note de devoir'
    )
    exam_marks = models.FloatField(
        blank=True,
        null=True, verbose_name='note d\'examen'
    )
    extra_marks = models.FloatField(
        blank=True, default=0,
        null=True, verbose_name='note de rattrapage'
    )
    total_marks = models.FloatField(
        blank=True,
        null=True, verbose_name='total'
    )
    average = models.FloatField(
        blank=True,
        null=True, verbose_name='moyenne'
    )
    validated = models.BooleanField(
        blank=True,
        default="False",
        verbose_name="Validé ?"
    )

    class Meta:
        unique_together = ('student', 'semester', 'subject')

    def __str__(self):
        return f'{self.student} | {self.subject} | {self.total_marks}'

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
        if self.average > 20:
            self.validated = True
        else:
            self.validated = False
        super().save(*args, **kwargs)


def create_resource():
    return reverse('result:create_subject_group')


class SubjectGroup(TimeStampedModel):
    """ Keep track of group of subjects that belongs to a
    department, semester
    """
    department = models.ForeignKey(
        Department,
        related_name='subjects',
        on_delete=models.DO_NOTHING, verbose_name='département'
    )
    semester = models.ForeignKey(
        Semester,
        related_name='subjects',
        on_delete=models.CASCADE, verbose_name='semestre'
    )
    subjects = models.ManyToManyField(Subject, blank=True, verbose_name='matières')

    def __str__(self):
        return f'{self.department} - {self.semester}'

    def get_subjects(self):
        return " | ".join([str(sg) for sg in self.subjects.all()])