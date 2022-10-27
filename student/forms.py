from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (
    Layout, Field, ButtonHolder, Submit
)
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import AdmissionStudent, CounselingComment, Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'last_name',
            'first_name',
            'date_of_birth',
            'gender',
            'nationality',
            'religion',
            'fathers_last_name',
            'fathers_first_name',
            'fathers_mobile_number',
            'mothers_last_name',
            'mothers_first_name',
            'mothers_mobile_number',
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


class AdmissionForm2(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'choosen_department',
            'last_name',
            'first_name',
            'date_of_birth',
            'gender',
            'nationality',
            'religion',
            'fathers_last_name',
            'fathers_first_name',
            'fathers_mobile_number',
            'mothers_last_name',
            'mothers_first_name',
            'mothers_mobile_number',
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
            'student_account',
            'admitted',
            'paid',
            'rejected',
        ]
        widgets = {
            'guardian_mobile_number': PhoneNumberPrefixWidget(initial='IN'),
            'gender': forms.HiddenInput(),
            'nationality': forms.HiddenInput(),
            'religion': forms.HiddenInput(),
            'fathers_last_name': forms.HiddenInput(),
            'fathers_first_name': forms.HiddenInput(),
            'fathers_mobile_number': PhoneNumberPrefixWidget(initial='IN'),
            'mothers_last_name': forms.HiddenInput(),
            'mothers_first_name': forms.HiddenInput(),
            'mothers_mobile_number': PhoneNumberPrefixWidget(initial='IN'),
            'bac_passing_year': forms.HiddenInput(),
            'last_exam_name': forms.HiddenInput(),
            'email': forms.HiddenInput(),
            'department_choice': forms.HiddenInput(),
            'photo': forms.HiddenInput(),
            'bac_marksheet': forms.HiddenInput(),
            'last_exam_marksheet': forms.HiddenInput(),
            'admission_policy_agreement': forms.HiddenInput(),
            'student_account': forms.HiddenInput(),
            'admitted': forms.HiddenInput(),
            'paid': forms.HiddenInput(),
            'rejected': forms.HiddenInput(),
            'date_of_birth': forms.HiddenInput(),
            'current_address': forms.HiddenInput(),
            'permanent_address': forms.HiddenInput(),
            'mobile_number': PhoneNumberPrefixWidget(initial='IN'),

        }


class StudentRegistrantUpdateForm(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'last_name',
            'first_name',
            'date_of_birth',
            'gender',
            'nationality',
            'religion',
            'fathers_last_name',
            'fathers_first_name',
            'fathers_mobile_number',
            'mothers_last_name',
            'mothers_first_name',
            'mothers_mobile_number',
            'current_address',
            'permanent_address',
            'mobile_number',
            'guardian_mobile_number',
            'email',
            'choosen_department',
            'bac_passing_year',
            'last_exam_name',
            'photo',
            'bac_marksheet',
            'last_exam_marksheet',
            'admitted',
            'paid',
            'rejected',
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
            'mobile_number': PhoneNumberPrefixWidget(initial='IN'),
            'current_address': forms.Textarea(attrs={"rows": 2}),
            'permanent_address': forms.Textarea(attrs={"rows": 2}),
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
            'guardian_mobile',
            'is_alumni', 'is_dropped'
        )


class ApplicationForm1(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'photo',
            'last_name',
            'first_name',
            'date_of_birth',
            'gender',
            'nationality',
            'religion',
            'email',
            'mobile_number',
            'current_address',
            'permanent_address',
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }


class ApplicationForm2(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'fathers_last_name',
            'fathers_first_name',
            'fathers_mobile_number',
            'mothers_last_name',
            'mothers_first_name',
            'mothers_mobile_number',
            'guardian_mobile_number',
        ]


class ApplicationForm3(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'department_choice',
            'bac_passing_year',
            'bac_marksheet',
            'last_exam_name',
            'last_exam_marksheet',
            'admission_policy_agreement',
        ]
