from django import forms

from instanpay.models import Product
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(
            subtype='Q'
        )
        self.fields['inquery'].queryset = Transaction.objects.filter(subtype='INQ')

    # def clean_customer(self):
    #     subtype = self.cleaned_data['subtype']
    #     inquery = self.cleaned_data['inquery']
    #     customer = self.cleaned_data['customer']

    #     if subtype == 'PAY':
    #         customer = inquery.customer
    #     return customer

    # def clean_product(self):
    #     subtype = self.cleaned_data['subtype']
    #     product = self.cleaned_data['product']
    #     inquery = self.cleaned_data['inquery']

    #     if subtype == 'PAY':
    #         product = inquery.product
    #     return product