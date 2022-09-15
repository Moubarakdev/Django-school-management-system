from django import forms

from teacher.models import Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['last_name', 'first_name', 'photo', 'date_of_birth', 'expertise',
                  'mobile', 'email', ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }
