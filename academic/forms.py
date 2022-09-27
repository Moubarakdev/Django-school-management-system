from django.forms import ModelForm

from .models import Department, Semester, AcademicSession, Subject, Batch


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']


class SemesterForm(ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']


class AcademicSessionForm(ModelForm):
    class Meta:
        model = AcademicSession
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']


class BatchForm(ModelForm):
    class Meta:
        model = Batch
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']
