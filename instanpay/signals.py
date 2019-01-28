from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from django.conf import settings
from django.utils import timezone

from .models import (
    Transaction, ServerResponse
)
from bill.models import (
    Billing, Kliring, Profit
)
from userprofile.models import Wallet
from .tasks import h2h_rbserver


@receiver(post_save, sender=Transaction)
def init_transaction(sender, instance, created, update_fields, **kwargs):
    if created:
        # Create no save billing obj
        billing_obj = Billing()
        billing_obj.user = instance.user
        billing_obj.instanpay_trx = instance
        billing_obj.credit = instance.price

        if instance.price > instance.user.wallet.saldo:
            # Transaction has loan / kliring
            kliring_obj = Kliring.objects.create(
                instanpay_trx = instance,
                buyer = instance.user,
                leader = instance.user.profile.leader.user,
                loan = instance.price - instance.user.wallet.saldo
            )

            # Relate kliring to billing obj
            billing_obj.kliring = kliring_obj

        # Save billing obj
        billing_obj.save()

        # Create Initial Response Server
        server_res_obj = ServerResponse.objects.create(
            trx = instance
        )

        # Create Initial Profit
        profit_obj = Profit()
        profit_obj.instanpay_trx = instance
        profit_obj.buyer = instance.user
        if instance.user.profile.leader.profile_type == 1:
            profit_obj.leader = instance.user.profile.leader.user
            profit_obj.commision = instance.commision
        profit_obj.save()


        # Default H2H
        # ====================================================================
        h2h_rbserver(instance.id, verbose_name='H2H Process', creator=instance)



    if update_fields:
        if 'status' in update_fields and instance.status == 'FL':
            # Billing start refund
            get_bill = instance.get_bill()
            billing_obj = Billing()
            billing_obj.user = instance.user
            billing_obj.instanpay_trx = instance
            billing_obj.debit = instance.price
            billing_obj.prev_bill = get_bill
            billing_obj.seq = get_bill.seq + 1

            if instance.kliring_set.exists():
                # Kliring obj refund
                get_klir = instance.get_kliring()
                kliring_obj = Kliring.objects.create(
                    instanpay_trx = instance,
                    buyer = instance.user,
                    leader = instance.user.profile.leader.user,
                    payment = get_klir.loan,
                    prev_kliring = get_klir,
                    seq = get_klir.seq + 1
                )
                billing_obj.kliring = kliring_obj

            # Billing save
            billing_obj.save()


            # Return Back Profit
            profit_obj = instance.profit
            profit_obj.return_back=True
            profit_obj.save(update_fields=['return_back'])
