from rest_framework import serializers
from django.contrib.auth.models import User

from userprofile.models import (
    Profile, Wallet
)

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    saldo = serializers.SerializerMethodField(read_only=True)
    limit = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'guid',
            'email', 'saldo', 'limit', 
        ]

    def get_email(self, obj):
        return obj.get_username()

    def get_saldo(self, obj):
        return obj.get_saldo()

    def get_limit(self, obj):
        return obj.get_limit()


class UpdateLimitSerializer(ProfileSerializer, serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0, write_only=True)

    def update(self, instance, validated_data):
        Wallet.objects.filter(profile=instance).update(
            limit=validated_data.get('amount')
        )
        return super().update(instance, validated_data)


