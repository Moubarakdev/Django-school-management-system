from django.forms import ModelForm

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
