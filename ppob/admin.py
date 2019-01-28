from django.contrib import admin

from .models import (
    Transaction,
    InqueryResponse, PaymentResponse
)
from .forms import TransactionForm


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionForm


@admin.register(InqueryResponse)
class InqueryResponseAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentResponse)
class PaymentResponseAdmin(admin.ModelAdmin):
    pass