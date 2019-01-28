from django import forms

from .models import (
    Wallet, Profile
)

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = [
            'user', 'profile',
            'saldo', 'limit'
        ]

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class LimitForm(WalletForm):
    class Meta(WalletForm.Meta):
        fields = [
            'limit'
        ]

    def clean_limit(self):
        limit = self.cleaned_data.get('limit')
        if limit < 0:
            raise forms.ValidationError('Limit can not insert by negative value')
        return limit