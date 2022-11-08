from django.db.models.signals import post_save
from django.dispatch import receiver

from payment.models import Invoice, Receipt, InvoiceItem


@receiver(post_save, sender=InvoiceItem)
def after_creating_invoice_item(sender, instance, created, **kwargs):
    if created:
        instance.term1 = (instance.amount * 30) / 100
        instance.term2 = (instance.amount * 30) / 100
        instance.term3 = (instance.amount * 20) / 100
        instance.term4 = (instance.amount * 20) / 100
        instance.save()


@receiver(post_save, sender=Invoice)
def after_creating_invoice(sender, instance, created, **kwargs):
    if created:
        previous_inv = (
            Invoice.objects.filter(student=instance.student)
            .exclude(id=instance.id)
            .last()
        )
        if previous_inv:
            if previous_inv.student.admission_student.choosen_department == instance.student.admission_student.choosen_department:
                pass
            else:
                previous_inv.status = "closed"
                previous_inv.save()
                instance.balance_from_previous_session = previous_inv.balance()
                instance.save()


@receiver(post_save, sender=Receipt)
def after_creating_receipt(sender, instance, created, **kwargs):
    if created:
        item = InvoiceItem.objects.get(invoice=instance.invoice)
        #  Algo de gestion des tranches
        if item.term1 >= instance.amount_paid:
            item.term1 -= instance.amount_paid
        elif item.term1 < instance.amount_paid:
            rest = instance.amount_paid - item.term1
            item.term1 = 0
            if rest <= item.term2:
                item.term2 -= rest
            elif rest > item.term2:
                rest2 = rest - item.term2
                item.term2 = 0
                if rest2 <= item.term3:
                    item.term3 -= rest2
                elif rest2 > item.term3:
                    rest3 = rest2 - item.term3
                    item.term3 = 0
                    if rest3 <= item.term4:
                        item.term4 -= rest3
                    else:
                        item.term4 = 0

        item.save()
