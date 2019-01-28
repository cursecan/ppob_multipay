from django import forms

from .models import (
    Group, Operator, Product, ExtraServer
)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'group_name'
        ]

    def clean_group_name(self):
        return self.cleaned_data.get('group_name').upper()


class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = [
            'operator_name'
        ]

    def clean_operator_name(self):
        return self.cleaned_data.get('operator_name').upper()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    
    def clean_code(self):
        return self.cleaned_data.get('code').upper()


class ProductViewForm(ProductForm):
    class Meta(ProductForm.Meta):
        fields = [
            'code', 'product_name',
            'subtype', 'group', 'operator',
            'nominal', 'price', 'commision',
            'is_active'
        ]