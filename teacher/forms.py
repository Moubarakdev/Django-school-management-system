from django import forms

from teacher.models import Teacher, TeacherSubjectGroup


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['last_name', 'first_name', 'photo', 'date_of_birth', 'expertise',
                  'mobile_number', 'email']
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }


class TeacherSubjectsForm(forms.ModelForm):
    class Meta:
        model = TeacherSubjectGroup
        fields = '__all__'
        exclude = ['created_by', 'created', 'updated']
