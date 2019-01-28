from rest_framework import serializers

from instanpay.api.serializers import ProductSerializer
from ppob.models import (
    Transaction, InqueryResponse, PaymentResponse
)
from instanpay.models import Product

class TransactionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = [
            'id',
            'trx_code', 'customer', 'product',
            'price', 'commision',
            'status',
        ]


class TopupPpobSerializer(serializers.Serializer):
    customer = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)

    def validate(self, data):
        code = data.get('code')

        # Product existing validation
        product_obj = Product.objects.filter(code=code, is_active=True, subtype='Q')
        if not product_obj.exists():
            raise serializers.ValidationError({
                'code': 'Product not found or inactive'
            })

        return data


class TopupPpobRequestSerializer(TopupPpobSerializer, serializers.ModelSerializer):
    inquery_code = serializers.CharField(write_only=True, required=False)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'trx_code', 'customer', 'code', 'subtype', 'inquery_code', 'product',
            'price', 'commision',
            'status',
        ]
        read_only_fields = [
            'id',
            'trx_code', 'product',
            'price', 'commision',
            'status'
        ]

    def create(self, validated_data):
        # Parameter
        code = validated_data.get('code')
        customer = validated_data.get('customer')
        subtype = validated_data.get('subtype', 'INQ')
        inquery_code = validated_data.get('inquery_code')
        user = self.context.get('user')
        leader = user.profile.leader

        product_obj = Product.objects.get(code=code)
        inquery_obj = Transaction.objects.get(trx_code=inquery_code)

        # Initial transaction
        transaction_obj = Transaction()
        transaction_obj.product = product_obj
        transaction_obj.customer = customer
        transaction_obj.user = user
        transaction_obj.subtype = subtype

        if subtype == 'PAY':
            # Required inqueri ID for payment
            transaction_obj.inquery = inquery_obj

        transaction_obj.save()

        return transaction_obj


    def validate(self, data):
        super().validate(data)
        user_obj = self.context.get('user')
        subtype = data.get('subtype')
        inquery_code = data.get('inquery_code')

        product_obj = Product.objects.get(code=data.get('code'))

        # Validation Only for Payment
        if subtype == 'PAY':
            # Inquery data validation
            inquery_obj = Transaction.objects.filter(subtype='INQ', trx_code=inquery_code)
            if not inquery_obj.exists():
                raise serializers.ValidationError({
                    'inquery_code':'Inquery not found.'
                })

            # Saldo Validation
            if user_obj.wallet.saldo < product_obj.price:
                # Inquery payment cannot be loan
                raise serializers.ValidationError({
                    'user': 'Direct error your saldo not enough.'
                })

                unpay = product_obj.price - user_obj.wallet.saldo
                if user_obj.wallet.loan + unpay > user_obj.wallet.limit:
                    raise serializers.ValidationError({
                        'user': 'User wallet on limit.'
                    })
                else:
                    leader = user_obj.profile.leader
                    if leader.wallet.saldo < product_obj.price:
                        raise serializers.ValidationError({
                            'user': 'Leader wallet on limit.'
                        })

            # Duplication Validation
            # pass
        
        return data