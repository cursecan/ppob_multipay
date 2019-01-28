from rest_framework import serializers

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
            'email', 'saldo', 'limit'
        ]

    def get_email(self, obj):
        return obj.get_username()

    def get_saldo(self, obj):
        return obj.get_saldo()

    def get_limit(self, obj):
        return obj.get_limit()