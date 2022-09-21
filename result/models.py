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
    practical_marks = models.SmallIntegerField(
        blank=True,
        null=True, verbose_name='note pratique'
    )
    theory_marks = models.SmallIntegerField(
        blank=True,
        null=True, verbose_name='note théorique'
    )
    total_marks = models.SmallIntegerField(
        blank=True,
        null=True, verbose_name='total notes'
    )

    class Meta:
        unique_together = ('student', 'semester', 'subject')

    def __str__(self):
        return f'{self.student} | {self.subject} | {self.total_marks}'

    def save(self, *args, **kwargs):
        if self.theory_marks and self.practical_marks:
            self.total_marks = self.practical_marks + self.theory_marks
        elif self.practical_marks and not self.theory_marks:
            self.total_marks = self.practical_marks
        else:
            self.total_marks = self.theory_marks
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
