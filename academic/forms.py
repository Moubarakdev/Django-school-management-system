from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import Department, Semester, AcademicSession, Subject, Batch, SiteConfig, AcademicTerm

SiteConfigForm = modelformset_factory(
    SiteConfig,
    fields=(
        "key",
        "value",
    ),
    extra=0,
)


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


class CurrentSessionForm(forms.Form):
    current_session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all(),
        help_text='Click <a href="/session/create/?next=current-session/">here</a> to add new session',
    )
    current_term = forms.ModelChoiceField(
        queryset=AcademicTerm.objects.all(),
        help_text='Click <a href="/term/create/?next=current-session/">here</a> to add new term',
    )


class AcademicTermForm(ModelForm):
    prefix = "Academic Term"

    class Meta:
        model = AcademicTerm
        fields = ["name", "current"]


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
