from django.contrib import admin

from .models import Result, Exam, SubjectGroup


class ResutlAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'exam',
        'subject', 'class_marks',
        'exam_marks', 'extra_marks', 'total_marks', 'average', 'validated',
    )
    list_editable = ('class_marks', 'exam_marks', 'extra_marks', 'exam')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'exam_date')


class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('department', 'get_subjects')


admin.site.register(Result, ResutlAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(SubjectGroup, SubjectGroupAdmin)
