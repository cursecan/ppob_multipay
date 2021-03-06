from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from .models import (
    Payment, KlirPayment
)

from bill.models import (
    Billing, Kliring
)
from userprofile.models import Wallet


@receiver(post_save, sender=Payment)
def record_payment(sender, instance, created, **kwargs):
    if created:
        Billing.objects.create(
            user = instance.receiver, 
            debit = instance.amount, 
            payment = instance
        )
        Billing.objects.create(
            user = instance.sender,
            credit = instance.amount,
            payment = instance
        )


@receiver(post_save, sender=KlirPayment)
def extra_kliring_payment(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.filter(user=instance.sender).update(
            loan = F('loan') - instance.pay
        )

        Kliring.unclean_objects.filter(
            buyer = instance.sender,
            leader = instance.receiver
        ).update(
            payment = F('loan'),
            flag = instance
        )

        if instance.extra_pay > 0:
            Payment.objects.create(
                amount = instance.extra_pay,
                sender = instance.receiver,
                receiver = instance.sender,
                kliring_payment = instance,
                description = "Payment cause from extra kliring payment."
            )