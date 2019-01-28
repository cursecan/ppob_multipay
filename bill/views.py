from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, DeleteView, CreateView
)
from django.views import View
from django.db.models import Q, F, Case, When, DateTimeField, CharField
from django.db.models.functions import TruncSecond, Cast
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import (
    Billing, Kliring
)
from core.decorators import superuser_required
from userprofile.models import Profile

import csv

# All sale list view
@method_decorator(login_required, name='dispatch')
@method_decorator(superuser_required, name='dispatch')
class SaleView(ListView):
    queryset = Billing.objects.filter(
        Q(instanpay_trx__isnull=False) | Q(ppob_trx__isnull=False)
    ).filter(seq = 1)
    
    template_name = 'billing/pg-sale.html'
    context_object_name = 'sale_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.queryset
        search = self.request.GET.get('search', None)
        sdate = self.request.GET.get('sdate', None)
        edate = self.request.GET.get('edate', None)

        # Filtering start date & end date
        if sdate:
            queryset = queryset.filter(timestamp__date__gte=sdate)
        if edate:
            queryset = queryset.filter(timestamp__date__lte=edate)

        # Filtering trx code
        if search:
            queryset = queryset.filter(
                Q(instanpay_trx__trx_code__contains = search) | Q(ppob_trx__trx_code__contains = search)
            )
        return queryset


# All kliring list view
@method_decorator(login_required, name='dispatch')
class KliringView(ListView):
    template_name = 'billing/pg-kliring.html'
    context_object_name = 'kliring_list'

    def get_queryset(self):
        # Filter only seq = 1
        queryset = Kliring.objects.filter(seq=1)
        return queryset


# Function View
# =============


# Export Sale Obj in CSV
@login_required
@superuser_required
def export_transaction_csv(request):
    queryset = Billing.objects.filter(
        Q(instanpay_trx__isnull=False) | Q(ppob_trx__isnull=False)
    ).filter(seq = 1)

    search = request.GET.get('search', None)
    sdate = request.GET.get('sdate', None)
    edate = request.GET.get('edate', None)

    if sdate:
        queryset = queryset.filter(timestamp__date__gte=sdate)
    if edate:
        queryset = queryset.filter(timestamp__date__lte=edate)

    if search:
        queryset = queryset.filter(
            instanpay_trx__trx_code__contains = search
        )

    queryset = queryset.annotate(
        get_trx=Case(
            When(instanpay_trx__isnull=False, then=F('instanpay_trx__trx_code')),
            When(ppob_trx__isnull=False, then=F('ppob_trx__trx_code'))
        ),
        get_product=Case(
            When(instanpay_trx__isnull=False, then=F('instanpay_trx__product__product_name')),
            When(ppob_trx__isnull=False, then=F('ppob_trx__product__product_name'))
        ),
        get_profit=Case(
            When(instanpay_trx__isnull=False, then=F('instanpay_trx__profit__profit')),
            When(ppob_trx__isnull=False, then=F('ppob_trx__profit__profit'))
        ),
        get_time=Cast(
            TruncSecond('timestamp', DateTimeField()), CharField()
        ),
        get_status=Case(
            When(instanpay_trx__isnull=False, then=F('instanpay_trx__status')),
            When(ppob_trx__isnull=False, then=F('ppob_trx__status'))
        )
    ).values_list('user__username', 'get_trx', 'get_product', 'credit', 'get_profit', 'get_time', 'get_status')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sale.csv"'

    writer = csv.writer(response)
    writer.writerow(['User', 'Transaction', 'Product', 'Price', 'Profit', 'Timestamp', 'Status'])
    

    for i in queryset:
        writer.writerow(i)

    return response

    

