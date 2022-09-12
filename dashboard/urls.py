from django.urls import path, include

from account.views import UserRequestsListView
from dashboard.views import index

app_name = "dashboard"

urlpatterns = [
    path('', index, name="index"),
    path('academic/', include('academic.urls')),
    path('requests/', UserRequestsListView.as_view(), name="read_requests")
]
