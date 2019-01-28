from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import (
    Profile, Wallet,
)


class ProfileInline(admin.TabularInline):
    model = Profile
    max = 1
    min = 1

class WalletInline(admin.TabularInline):
    model = Wallet
    min = 1
    max = 1

class UserAdminCustom(UserAdmin):
    inlines = [
        ProfileInline,
        WalletInline
    ]

admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)