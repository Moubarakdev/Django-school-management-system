from django.forms import ModelForm, inlineformset_factory, modelformset_factory

from payment.models import InvoiceItem, Invoice, Receipt

InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=["description", "amount"], extra=1, can_delete=True
)

InvoiceReceiptFormSet = inlineformset_factory(
    Invoice,
    Receipt,
    fields=("amount_paid", "comment"),
    extra=0,
    can_delete=True,
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=4)
