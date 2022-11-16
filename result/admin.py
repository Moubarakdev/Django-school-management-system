from django.contrib import admin

from .models import Result, SubjectGroup


class ResutlAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'subject', 'class_marks',
        'exam_marks', 'extra_marks', 'total_marks', 'average', 'validated',
    )
    list_editable = ('class_marks', 'exam_marks', 'extra_marks')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'exam_date')


class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('department', 'get_subjects')


admin.site.register(Result, ResutlAdmin)
admin.site.register(SubjectGroup, SubjectGroupAdmin)
