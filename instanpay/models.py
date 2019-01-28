from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from core.models import CommonBase


class Group(CommonBase):
    slug = models.SlugField(max_length=20, unique=True, editable=False)
    group_name = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.group_name)
        super(Group, self).save(*args, **kwargs)


class Operator(CommonBase):
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    operator_name = models.CharField(max_length=50, unique=True)
    group = models.ManyToManyField(Group, through='Product')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.operator_name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.operator_name)
        super(Operator, self).save(*args, **kwargs)


class Prefix(models.Model):
    prefix = models.CharField(max_length=4, unique=True)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)

    class Meta:
        ordering = ['prefix']

    def __str__(self):
        return self.prefix


class GroupServer(models.Model):
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.group_server


class ExtraServer(models.Model):
    code = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=200)
    group_server = models.ForeignKey(GroupServer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.product_name


class Product(CommonBase):
    INSTAN = 'I'
    INQUERY = 'Q'
    SUBTYPE_LIST = (
        (INSTAN, 'Instan Product'),
        (INQUERY, 'Product Inquery')
    )
    subtype = models.CharField(max_length=1, choices=SUBTYPE_LIST, default=INSTAN)
    code = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    nominal = models.PositiveIntegerField(default=0)
    extend_server = models.OneToOneField(ExtraServer, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = [
            'group', 'operator',
            '-nominal'
        ]

    def __str__(self):
        return self.code


    def get_absolute_url(self):
        return reverse('instanpay:detail_product', kwargs={'id': self.id})

    def get_prodcode(self):
        if self.extend_server:
            return self.extend_server.code
        return self.code

    def get_servergroup(self):
        if self.extend_server:
            return self.extend_server.group_server.code
        return ''


class Transaction(CommonBase):
    OPEN = 'OP'
    PROCESS = 'PR'
    COMPLETE = 'CO'
    FAILED = 'FL'
    STATUS_LIST = (
        (OPEN, 'Open'),
        (PROCESS, 'In Process'),
        (COMPLETE, 'Complete'),
        (FAILED, 'Failed')
    )
    trx_code = models.SlugField(max_length=20, unique=True, editable=False)
    customer = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=20, blank=True)
    server_group = models.CharField(max_length=20, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=2, choices=STATUS_LIST, default=OPEN)

    class Meta:
        ordering = [
            '-id'
        ]

    def __str__(self):
        return self.trx_code

    def save(self, *args, **kwargs):
        if self.trx_code is None or self.trx_code == '':
            self.trx_code = '11' + slugify(int(self.due_date.timestamp()))
            self.price = self.product.price
            self.commision = self.product.commision
            self.product_code = self.product.get_prodcode()
            self.server_group = self.product.get_servergroup()
        super(Transaction, self).save(*args, **kwargs)


    def get_bill(self):
        return self.billing_set.latest('timestamp')

    def get_kliring(self):
        return self.kliring_set.latest('timestamp')




class ServerResponse(CommonBase):
    trx = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    kode_produk = models.CharField(max_length=200, blank=True)
    waktu = models.CharField(max_length=200, blank=True)
    no_hp = models.CharField(max_length=200, blank=True)
    sn = models.CharField(max_length=200, blank=True)
    nominal = models.IntegerField(default=0)
    ref1 = models.CharField(max_length=200, blank=True)
    ref2 = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, blank=True)
    ket = models.CharField(max_length=200, blank=True)
    saldo_terpotong = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sisa_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-id']