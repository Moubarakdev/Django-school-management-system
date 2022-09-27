from django.forms import ModelForm

from result.models import SubjectGroup


class SubjectGroupForm(ModelForm):
    class Meta:
        model = SubjectGroup
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']
