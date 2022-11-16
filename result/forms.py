from django.forms import ModelForm, modelformset_factory
from django import forms

from academic.models import Subject
from result.models import SubjectGroup, Result


class SubjectGroupForm(ModelForm):
    class Meta:
        model = SubjectGroup
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']


class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at', 'total_marks', 'average', 'validated', ]


class CreateResults(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )


EditResults = modelformset_factory(
    Result, fields=("class_marks", "exam_marks"), extra=0, can_delete=True
)
