from django.db import models
from django.contrib.auth.models import User

from core.models import CommonBase


class Payment(CommonBase):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='receiver')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(max_length=500, blank=True)
    kliring_payment = models.OneToOneField('KlirPayment', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        ordering = [
            '-id'
        ]

    def __str__(self):
        return '%s, %d' %(self.sender.email, self.amount)


class KlirPayment(CommonBase):
    pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    extra_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='c_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='c_receiver')

    class Meta:
        ordering = ['-id']

    