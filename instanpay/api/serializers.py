from rest_framework import serializers
from django.contrib.auth.models import User

from instanpay.models import (
    Transaction, Product, Group, Operator
)

# Operator Serializer
class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = [
            'id',
            'operator_name'
        ]


# Group Serializer
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'group_name'
        ]


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    operator = OperatorSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'product_name', 'code',
            'group', 'operator',
            'price', 'commision',
        ]


# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'trx_code', 'customer',
            'product',
            'price', 'commision', 'status'
        ]


# Basic TopUp Serializer
class TopUpSerializer(serializers.Serializer):
    customer = serializers.CharField()
    code = serializers.CharField(write_only=True)

    def validate(self, data):
        code = data.get('code')
        product_exists = Product.objects.filter(
            is_active=True, code=code, subtype='I'
        ).exists()

        if not product_exists:
            raise serializers.ValidationError({
                'code': 'Product code not found or inactive product.'
            })

        return data


# TopUp Serializer
class TopUpRequestSerializer(TopUpSerializer, serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'trx_code', 'customer', 'code',
            'product',
            'price', 'commision', 'status'
        ]
        read_only_fields = [
            'id', 'trx_code',
            'product',
            'price', 'commision', 'status'
        ]

    def create(self, validated_data):
        code = validated_data.get('code')
        customer = validated_data.get('customer')
        user = self.context.get('user')
        leader = user.profile.leader

        product_obj = Product.objects.get(code=code)

        transaction_obj = Transaction.objects.create(
            product = product_obj,
            customer = customer,
            user = user
        )

        return transaction_obj

    def validate(self, data):
        super().validate(data)
        user_obj = self.context.get('user')
        product_obj = Product.objects.get(code=data.get('code'))

        # Saldo Validation
        if user_obj.wallet.saldo < product_obj.price:
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