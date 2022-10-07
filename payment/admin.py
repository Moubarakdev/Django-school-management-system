from django.contrib import admin

from payment.models import StudentFeesInfo


# Register your models here.
class StudentFeesInfoAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'fees',
    )


admin.site.register(StudentFeesInfo, StudentFeesInfoAdmin)
