from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Group, Operator, Product, ExtraServer, Prefix,
    GroupServer, Transaction, ServerResponse
)

from .forms import (
    GroupForm, OperatorForm,
    ProductForm
)

from .resources import ProductResource, OperatorResource, GroupResource

class PrefixInline(admin.TabularInline):
    model = Prefix
    extra = 1

@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = [
        'group_name'
    ]
    form = GroupForm
    list_per_page = 20
    list_max_show_all = 100
    resource_class = GroupResource


@admin.register(Operator)
class OperatorAdmin(ImportExportModelAdmin):
    list_display = [
        'operator_name'
    ]
    form = OperatorForm
    inlines = [
        PrefixInline
    ]
    list_per_page = 20
    list_max_show_all = 100
    resource_class = OperatorResource


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    form = ProductForm
    list_display = [
        'code', 'product_name',
        'group', 'operator',
        'price', 'commision',
        'extend_server', 'is_active'
    ]
    list_editable = [
        'price', 'commision'
    ]
    list_filter = [
        'is_active', 
        'group__group_name', 'operator__operator_name'
    ]
    search_fields = [
        'code'
    ]
    list_per_page = 20
    list_max_show_all = 100
    resource_class = ProductResource

@admin.register(ExtraServer)
class ExtraServerAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'product_name',
        'price'
    ]
    list_per_page = 20
    list_max_show_all = 100


@admin.register(GroupServer)
class GroupServerAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'trx_code',
        'customer',
        'product',
        'product_code', 
        'price', 'commision',
        'status', 'user'
    ]

@admin.register(ServerResponse)
class ResponseAdmin(admin.ModelAdmin):
    pass