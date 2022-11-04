from crispy_forms.helper import FormHelper

from django import forms as djform
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import CommonUserProfile

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = ('requested_role',)


class UserCreateFormDashboard(forms.UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2',
            'requested_role', 'approval_status', 'is_staff')


class UserChangeFormDashboard(forms.UserChangeForm):
    password = None

    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'requested_role', 'approval_status',
            'is_staff',
        )


class UserRegistrationForm(forms.UserCreationForm):
    REQUESTED_CHOICES = (
        ('student', 'Etudiant'),
        ('teacher', 'Professeur'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.template_pack = 'bootstrap4'

    error_message = forms.UserCreationForm.error_messages.update(
        {
            "duplicate_username": _(
                "Ce nom d'utilisateur existe déjà."
            )
        }
    )

    last_name = djform.CharField(
        widget=djform.TextInput(
            attrs={
                "placeholder": "Nom",
                "class": "form-control"
            }
        ))
    first_name = djform.CharField(
        widget=djform.TextInput(
            attrs={
                "placeholder": "Prénom",
                "class": "form-control"
            }
        ))
    username = djform.CharField(
        widget=djform.TextInput(
            attrs={
                "placeholder": "Nom d'utilisateur",
                "class": "form-control"
            }
        ))
    email = djform.EmailField(
        widget=djform.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = djform.CharField(
        widget=djform.PasswordInput(
            attrs={
                "placeholder": "Mot de passe",
                "class": "form-control"
            }
        ))
    password2 = djform.CharField(
        widget=djform.PasswordInput(
            attrs={
                "placeholder": "Confirmer mot de passe",
                "class": "form-control"
            }
        ))
    requested = djform.ChoiceField(choices=REQUESTED_CHOICES)

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email', 'password1', 'password2', 'requested')

    '''
    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(
            self.error_messages["duplicate_username"]
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password didn\'t match!')
        return cd['password2']
'''


class ProfileCompleteForm(djform.ModelForm):
    class Meta:
        model = User
        fields = [
            'employee_or_student_id',
            'requested_role',
            'email',
            'approval_extra_note']


class ApprovalProfileUpdateForm(djform.ModelForm):
    class Meta:
        model = User
        fields = ['requested_role']


class CommonUserProfileForm(djform.ModelForm):
    class Meta:
        model = CommonUserProfile
        fields = [
            'country',
            'address',
            'summary',
        ]

    widgets = {
        'address': djform.Textarea(attrs={"rows": 2}),
    }


class LoginForm(djform.Form):
    username = djform.CharField(
        widget=djform.TextInput(
            attrs={
                "placeholder": "Nom d'utilisateur ou Email",
                "class": "form-control"
            }
        ))
    password = djform.CharField(
        widget=djform.PasswordInput(
            attrs={
                "placeholder": "Mot de passe",
                "class": "form-control"
            }
        ))


class UpdateUserForm(djform.ModelForm):
    username = djform.CharField(max_length=100,
                                required=True,
                                widget=djform.TextInput(attrs={'class': 'form-control'}))
    email = djform.EmailField(required=True, disabled=True,
                              widget=djform.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name', ]
