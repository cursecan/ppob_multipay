from rest_framework import serializers


from bill.models import Billing


class BillingSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Billing
        fields = [
            'id', 
            'debit', 'credit', 'balance',
            'data',
            'timestamp'
        ]

    def get_data(self, obj):
        data = dict()
        if obj.get_trx():
            data['type'] = 'Transaction'
            data['code'] = obj.get_trx().trx_code
            data['product'] = obj.get_trx().product.product_name
            data['status'] = obj.get_trx().get_status_display()

        else :
            data['type']= 'Topup'
        return data


    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # seq = models.PositiveSmallIntegerField(default=1)
    # prev_bill = models.OneToOneField('self', on_delete=models.CASCADE, blank=True, null=True)
    # payment = models.OneToOneField(Payment, on_delete=models.CASCADE, blank=True, null=True)
    # kliring = models.OneToOneField('Kliring', on_delete=models.CASCADE, blank=True, null=True)
    # instanpay_trx = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, null=True)
    # ppob_trx = models.ForeignKey(PpobTransaction, on_delete=models.CASCADE, blank=True, null=True)