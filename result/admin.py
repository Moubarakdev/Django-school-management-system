from django.contrib import admin

from result.models import Result, Exam, SubjectGroup


# Register your models here.
class ResutlAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'semester', 'exam',
        'subject', 'class_marks',
        'exam_marks', 'total_marks', 'extra_marks'
    )
    list_editable = ('total_marks', 'exam')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'exam_date')


class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('department', 'semester', 'get_subjects')


admin.site.register(Result, ResutlAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(SubjectGroup, SubjectGroupAdmin)
