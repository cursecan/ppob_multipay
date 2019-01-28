from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

from core.models import CommonBase
from instanpay.models import Product


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

    INQUERY = 'INQ'
    PAYMENT = 'PAY'
    LIST_QUERY = (
        (INQUERY, 'Inquery'),
        (PAYMENT, 'Pay')
    )

    trx_code = models.SlugField(max_length=20, unique=True, editable=False)
    customer = models.CharField(max_length=50)
    subtype = models.CharField(max_length=3, choices=LIST_QUERY, default=INQUERY)
    inquery = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inq_product')
    product_code = models.CharField(max_length=20, blank=True)
    server_group = models.CharField(max_length=20, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='inq_user')
    status = models.CharField(max_length=2, choices=STATUS_LIST, default=OPEN)

    class Meta:
        ordering = [
            '-id'
        ]

    def __str__(self):
        if self.subtype == self.INQUERY:
            return 'Inquery %s' %(self.product.product_name)
        return self.trx_code

    def save(self, *args, **kwargs):
        if self.subtype == self.PAYMENT:
            self.customer = self.inquery.customer
            self.product = self.inquery.product
            self.price = self.inquery.trx_inq.get_bayar() - (self.inquery.commision - 500)
            if self.product.price > 0:
                self.price = self.product.price

        if self.trx_code is None or self.trx_code == '':
            self.trx_code = '12' + slugify(int(self.due_date.timestamp()))
            self.commision = self.product.commision
            self.product_code = self.product.get_prodcode()
            self.server_group = self.product.get_servergroup()
        super(Transaction, self).save(*args, **kwargs)


class InqueryResponse(CommonBase):
    trx = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='trx_inq')
    kode_produk = models.CharField(max_length=200, blank=True)
    waktu = models.CharField(max_length=200, blank=True)
    idpel1 = models.CharField(max_length=200, blank=True)
    idpel2 = models.CharField(max_length=200, blank=True)
    idpel3 = models.CharField(max_length=200, blank=True)
    nama_palanggan = models.CharField(max_length=200, blank=True)
    periode = models.CharField(max_length=200, blank=True)
    nominal = models.PositiveIntegerField(default=0)
    admin = models.PositiveIntegerField(default=0)
    ref1 = models.CharField(max_length=200, blank=True)
    ref2 = models.CharField(max_length=200, blank=True)
    ref3 = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, blank=True)
    ket = models.CharField(max_length=200, blank=True)
    saldo_terpotong = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sisa_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    url_struk = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-id']

    def get_bayar(self):
        return self.nominal + self.admin


class PaymentResponse(CommonBase):
    trx = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='trx_pay')
    kode_produk = models.CharField(max_length=200, blank=True)
    waktu = models.CharField(max_length=200, blank=True)
    idpel1 = models.CharField(max_length=200, blank=True)
    idpel2 = models.CharField(max_length=200, blank=True)
    idpel3 = models.CharField(max_length=200, blank=True)
    nama_palanggan = models.CharField(max_length=200, blank=True)
    periode = models.CharField(max_length=200, blank=True)
    nominal = models.PositiveIntegerField(default=0)
    admin = models.PositiveIntegerField(default=0)
    ref1 = models.CharField(max_length=200, blank=True)
    ref2 = models.CharField(max_length=200, blank=True)
    ref3 = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, blank=True)
    ket = models.CharField(max_length=200, blank=True)
    saldo_terpotong = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sisa_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    url_struk = models.CharField(max_length=200, blank=True)
    detail = models.TextField(max_length=3000, blank=True)
    
    class Meta:
        ordering = ['-id']