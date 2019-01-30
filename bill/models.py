from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F

from core.models import CommonBase
from payment.models import Payment
from instanpay.models import Transaction
from ppob.models import Transaction as PpobTransaction


# Billing Model
class Billing(CommonBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    seq = models.PositiveSmallIntegerField(default=1)
    prev_bill = models.OneToOneField('self', on_delete=models.CASCADE, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True, related_name='bil_payment')
    kliring = models.OneToOneField('Kliring', on_delete=models.CASCADE, blank=True, null=True)
    instanpay_trx = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, null=True)
    ppob_trx = models.ForeignKey(PpobTransaction, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        # Descending order by id
        ordering = [
            '-id'
        ]

    def __str__(self):
        return self.user.username


    def save(self, *args, **kwargs):
        # Save obj to effect current balance
        # Then update balance for saldo user
        user_wallet = self.user.wallet
        user_wallet.refresh_from_db()
        self.balance = user_wallet.saldo - self.credit + self.debit
        super(Billing, self).save(*args, **kwargs)


    def get_trx(self):
        # Link to transaction objects
        if self.instanpay_trx:
            return self.instanpay_trx
        if self.ppob_trx:
            return self.ppob_trx
        return None


# Kliring Manager with No payment
class UnCleanKliringManager(models.Manager):
    def get_queryset(self):
        return super(UnCleanKliringManager, self).get_queryset().filter(
            Q(ppob_trx__status__in=['OP', 'PR', 'CO']) | Q(instanpay_trx__status__in=['OP', 'PR', 'CO'])
        ).exclude(loan=F('payment'))


# Kliring Model
class Kliring(CommonBase):
    instanpay_trx = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, null=True)
    ppob_trx = models.OneToOneField(PpobTransaction, on_delete=models.CASCADE, blank=True, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader')
    prev_kliring = models.OneToOneField('self', on_delete=models.CASCADE, blank=True, null=True)
    seq = models.PositiveSmallIntegerField(default=1)
    loan = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    flag = models.ForeignKey('FlagKliring', on_delete=models.CASCADE, blank=True, null=True)

    objects = models.Manager()
    unclean_objects = UnCleanKliringManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return '%s, %s, %d, %d' %(self.buyer.email, self.leader.email, self.loan, self.payment)

    def get_trx(self):
        # Link to transaction object
        if self.instanpay_trx:
            return self.instanpay_trx
        elif self.ppob_trx:
            return self.ppob_trx
        return None

    def is_clean(self):
        # Check kliring has paid 
        # or transaction is failed
        return self.loan == self.payment or self.get_trx().status == 'FL' 


# Profit Model
class Profit(CommonBase):
    instanpay_trx = models.OneToOneField(Transaction, on_delete=models.CASCADE, blank=True, null=True)
    ppob_trx = models.OneToOneField(PpobTransaction, on_delete=models.CASCADE, blank=True, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prof_buyer', blank=True, null=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prof_leader', blank=True, null=True)
    profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    witdraw = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    return_back = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']


# Peyment Kliring Record
class FlagKliring(CommonBase):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='f_buyer')
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='f_leader')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-id']