from django.contrib import admin

from .models import (
    Billing, Kliring, Profit
)

# Billing View
@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'debit', 'credit', 'balance',
        'timestamp',
        'prev_bill', 'seq'
    ]

# Kliring View
@admin.register(Kliring)
class KliringAdmin(admin.ModelAdmin):
    list_display = [
        'buyer', 'leader',
        'loan', 'payment'
    ]


# Profit View
@admin.register(Profit)
class ProfitAdmin(admin.ModelAdmin):
    list_display = [
        'buyer', 'leader',
        'profit', 'commision', 'witdraw',
        'return_back',
    ]