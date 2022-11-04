from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from academic.views import SubjectListView, \
    CreateSubjectView, UpdateSubjectView, DeleteSubjectView, CreateDepartmentView, UpdateDepartmentView, \
    DeleteDepartmentView, CreateAcademicSession, AcademicSessionListView, DepartmentListView, DeleteAcademicSession, \
    UpdateAcademicSession, SiteConfigView, \
    CurrentSessionAndTermView
from myschool import settings

app_name = 'academic'

urlpatterns = [
                  # Site
                  path("site-config", SiteConfigView.as_view(), name="configs"),
                  path("current-session/", CurrentSessionAndTermView.as_view(), name="current_session"),

                  # Subject
                  path('subject/', SubjectListView.as_view(), name="read_subjects"),
                  path('subject/create/', CreateSubjectView.as_view(), name="create_subject"),
                  path('subject/delete/<int:pk>', DeleteSubjectView.as_view(), name="delete_subject"),
                  path('subject/edit/<int:pk>', UpdateSubjectView.as_view(), name="update_subject"),

                  # Department
                  path('department/', DepartmentListView.as_view(), name="read_departments"),
                  path('department/create/', CreateDepartmentView.as_view(), name="create_department"),
                  path('department/delete/<int:pk>', DeleteDepartmentView.as_view(), name="delete_department"),
                  path('department/edit/<int:pk>', UpdateDepartmentView.as_view(), name="update_department"),

                  # Academic Session
                  path('academicsession/', AcademicSessionListView.as_view(), name="read_ac_sessions"),
                  path('academicsession/create/', CreateAcademicSession.as_view(), name="create_ac_session"),
                  path('academicsession/delete/<int:pk>', DeleteAcademicSession.as_view(), name="delete_ac_session"),
                  path('academicsession/update/<int:pk>', UpdateAcademicSession.as_view(), name="update_ac_session"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
