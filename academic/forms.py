from django.forms import ModelForm

from .models import Department, Semester, AcademicSession, Subject


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        exclude = ['created_by', ]


class SemesterForm(ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'
        exclude = ['created_by', ]


class AcademicSessionForm(ModelForm):
    class Meta:
        model = AcademicSession
        fields = '__all__'
        exclude = ['created_by', ]


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['created_by', ]
