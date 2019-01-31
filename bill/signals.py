from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from userprofile.models import Wallet

from .models import (
    Billing, Kliring, Profit
)

# Billing Signaling
@receiver(post_save, sender=Billing)
def update_saldo(sender, instance, created, **kwargs):
    if created:
        # Updating Saldo User
        wallet_obj = Wallet.objects.get(user=instance.user)
        wallet_obj.saldo = instance.balance                
        wallet_obj.save()


# Loan Signaling
@receiver(post_save, sender=Kliring)
def update_loan_base_saldo(sender, instance, created, **kwargs):
    if created:
        # Update wallet loan to user
        Wallet.objects.filter(user=instance.buyer).update(
            loan = F('loan') + instance.loan - instance.payment,
            saldo = F('saldo') + instance.loan - instance.payment
        )

        # Update wallet saldo for leader
        Wallet.objects.filter(user=instance.leader).update(
            saldo = F('saldo') + instance.payment - instance.loan
        )

# Profit Signaling
@receiver(post_save, sender=Profit)
def update_commision(sender, instance, created, update_fields, **kwargs):
    if created:
        if instance.leader:
            # Update wallet commision agen
            Wallet.objects.filter(user=instance.leader).update(
                commision = F('commision') + instance.commision - instance.witdraw
            )

    if update_fields:
        if 'return_back' in update_fields:
            if instance.return_back == True and instance.leader:
                # Commision is return back
                Wallet.objects.filter(user=instance.leader).update(
                    commision = F('commision') - instance.commision
                )