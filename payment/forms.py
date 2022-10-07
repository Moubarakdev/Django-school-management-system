from django.forms import ModelForm

from payment.models import SchoolFees


class SchoolFeesForm(ModelForm):
    class Meta:
        model = SchoolFees
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at']

