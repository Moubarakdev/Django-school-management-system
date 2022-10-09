from django.urls import path

from payment.views import InvoiceListView, \
    InvoiceCreateView, InvoiceDetailView, InvoiceDeleteView, ReceiptCreateView, ReceiptUpdateView, InvoiceUpdateView

app_name = 'payment'

urlpatterns = [
    # fees
    path("list/", InvoiceListView.as_view(), name="read_invoices"),
    path("create/", InvoiceCreateView.as_view(), name="create_invoice"),
    path("<int:pk>/detail/", InvoiceDetailView.as_view(), name="invoice_detail"),
    path("<int:pk>/update/", InvoiceUpdateView.as_view(), name="update_invoice"),
    path("<int:pk>/delete/", InvoiceDeleteView.as_view(), name="delete_invoice"),
    path("receipt/create", ReceiptCreateView.as_view(), name="create_invoice"),
    path(
        "receipt/<int:pk>/update/", ReceiptUpdateView.as_view(), name="update_receipt"
    ),
]
