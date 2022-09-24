from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (
    Layout, Field, ButtonHolder, Submit
)
from .models import AdmissionStudent, CounselingComment, Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'last_name',
            'first_name',
            'fathers_last_name',
            'fathers_first_name',
            'fathers_mobile_number',
            'mothers_last_name',
            'mothers_first_name',
            'mothers_mobile_number',
            'date_of_birth',
            'nationality',
            'current_address',
            'permanent_address',
            'mobile_number',
            'guardian_mobile_number',
            'email',
            'department_choice',
            'bac_passing_year',
            'last_exam_name',
            'photo',
            'bac_marksheet',
            'last_exam_marksheet',
            'admission_policy_agreement',
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'choosen_department',
        ]


class StudentRegistrantUpdateForm(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'last_name',
            'first_name',
            'photo',
            'fathers_last_name',
            'fathers_first_name',
            'fathers_mobile_number',
            'mothers_last_name',
            'mothers_first_name',
            'mothers_mobile_number',
            'date_of_birth',
            'nationality',
            'current_address',
            'permanent_address',
            'mobile_number',
            'guardian_mobile_number',
            'email',
            'bac_marksheet',
            'last_exam_marksheet',
            'choosen_department',
            'admitted',
            'paid',
            'rejected',
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }


class CounselingDataForm(forms.ModelForm):
    class Meta:
        model = CounselingComment
        fields = ['comment', ]


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'roll',
            'registration_number',
            'semester',
            'guardian_mobile',
            'is_alumni', 'is_dropped'
        )