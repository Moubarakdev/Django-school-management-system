import django_filters

from student.models import Student


class AlumniFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = [
            'admission_student__last_name',
            'admission_student__first_name',
            'admission_student__choosen_department',
            'roll',
            'ac_session',
        ]

    def __init__(self, *args, **kwargs):
        super(AlumniFilter, self).__init__(*args, **kwargs)
        self.filters['admission_student__last_name'].label = 'Nom'
        self.filters['admission_student__first_name'].label = 'Prénom'
        self.filters['admission_student__choosen_department'].label = 'Département'
        self.filters['ac_session'].label = 'Session Académique'
