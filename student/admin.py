from django.contrib import admin
from .models import Student, AdmissionStudent


class AdmissionStudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'created', 'nationality',
        'choosen_department', 'admitted',
        'assigned_as_student'
    )
    list_editable = ('admitted', 'assigned_as_student')
    list_filter = (
        'paid', 'rejected', 'choosen_department',
        'admitted', 'nationality',
    )


class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_student',
                    'ac_session',
                    'temp_serial',
                    'temporary_id')


admin.site.register(Student, StudentAdmin)
admin.site.register(AdmissionStudent, AdmissionStudentAdmin)
