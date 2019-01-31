from django.contrib import admin

from .models import (
    Payment, KlirPayment
)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'sender', 'receiver',
        'amount'
    ]


@admin.register(KlirPayment)
class KlirPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'sender', 'receiver',
        'pay', 'extra_pay',
        'timestamp'
    ]