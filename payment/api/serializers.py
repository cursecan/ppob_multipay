from rest_framework import serializers
from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce

from payment.models import (
    Payment, KlirPayment
)
from userprofile.models import Profile
from bill.models import Kliring

class SaldoTransferSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    nominal = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=1, write_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'sender', 'receiver',
            'amount',
            'email', 'nominal'
        ]
        read_only_fields = [
            'id',
            'sender', 'receiver',
            'amount'
        ]

    def validate(self, data):
        email = data.get('email')
        nominal = data.get('nominal')
        sender = self.context.get('sender')

        profile_objs = Profile.objects.filter(user__username=email)
        if not profile_objs.exists():
            raise serializers.ValidationError({
                'error': 'User does not exists.'
            })
        if sender.wallet.saldo < nominal:
            raise serializers.ValidationError({
                'error': 'Saldo sender not enough.'
            })

        return data
    
    def create(self, validated_data):
        nominal = validated_data.get('nominal')
        email = validated_data.get('email')
        sender = self.context.get('sender')

        profile_obj = Profile.objects.get(user__username=email)
        payment_obj = Payment.objects.create(
            receiver = profile_obj.user,
            sender = sender,
            amount = nominal,
        )
        return payment_obj


class KliringPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlirPayment
        fields = [
            'id',
            'sender', 'receiver',
            'pay', 'extra_pay',
            'timestamp'
        ]

    def validate(self, data):
        sender = data.get('sender')
        receiver = data.get('receiver')
        pay = data.get('pay')

        kliring_obj = Kliring.unclean_objects.filter(leader=receiver, buyer=sender)
        total = kliring_obj.aggregate(t_loan = Coalesce(Sum('loan'), V(0)))
        if total['t_loan'] == 0:
            raise serializers.ValidationError({
                'error': 'User does not has loan.'
            })
        if pay != total['t_loan']:
            raise serializers.ValidationError({
                'error': 'Pay value does not match with loan record value.'
            })
        return data
