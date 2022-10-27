from django.contrib import admin

from payment.models import Invoice, InvoiceItem, Receipt


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('student',
                    'session',
                    'balance_from_previous_session',
                    'status')


class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice',
                    'amount',
                    'term1',
                    'term2',
                    'term3',
                    'term4',
                    'description')


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('invoice',
                    'amount_paid',
                    'date_paid',
                    'comment')


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
admin.site.register(Receipt, ReceiptAdmin)
