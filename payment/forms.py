from django import forms

from .models import (
    Payment, KlirPayment
)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'sender',
            # 'receiver',
            'amount', 'description',
        ]

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 1000:
            raise forms.ValidationError('Minimal amount 1.000')
        return amount


class PublicPayment(forms.Form):
    amount = forms.DecimalField(max_digits=12, min_value=1)