from django.urls import path

from payment.views import FeesListView, FeesCreateView, FeesDeleteView, FeesUpdateView

app_name = 'payment'

urlpatterns = [
    # fees
    path('fees/', FeesListView.as_view(), name="read_fees"),
    path('fees/create/', FeesCreateView.as_view(), name="create_fees"),
    path('fees/delete/<int:pk>', FeesDeleteView.as_view(), name="delete_fees"),
    path('fees/edit/<int:pk>', FeesUpdateView.as_view(), name="update_fees"),
]
