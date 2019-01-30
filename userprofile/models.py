from django.db import models
from django.contrib.auth.models import User

import uuid

class Profile(models.Model):
    AGEN = 1
    CUSTOMER = 2
    PROFILETYPE_LIST = (
        (AGEN, 'Agen'),
        (CUSTOMER, 'Customer')
    )
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    leader = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    profile_type = models.PositiveSmallIntegerField(choices=PROFILETYPE_LIST, default=CUSTOMER)

    class Meta:
        ordering = [
            'user__username'
        ]

    # def save(self, *args, **kwargs):
    #     if self.leader is None :
    #         super(Profile, self).save(*args, **kwargs)
    #         self.leader = self
    #     super(Profile, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.user.username

    def get_saldo(self):
        return self.wallet.saldo

    def get_limit(self):
        return self.wallet.limit

    def get_username(self):
        return self.user.username

    def get_fullname(self):
        return '%s %s' %(self.user.first_name, self.user.last_name)
        

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    loan = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-id']
