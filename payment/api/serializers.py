from rest_framework import serializers

from payment.models import Payment
from userprofile.models import Profile


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