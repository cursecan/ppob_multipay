from django.shortcuts import render
from django.views.generic import (
    ListView, CreateView, DetailView, DeleteView, UpdateView
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Product
from .forms import ProductViewForm
from core.decorators import superuser_required



# Product List View
@method_decorator(login_required, name='dispatch')
@method_decorator(superuser_required, name='dispatch')
class ProductView(ListView):
    paginate_by = 10
    template_name = 'instanpay/pg-product.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        queryset = Product.objects.all()

        subtype = self.request.GET.get('subtype', None)
        if subtype:
            queryset = queryset.filter(subtype=subtype)

        return queryset


# Product Detail View
@method_decorator(login_required, name='dispatch')
@method_decorator(superuser_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'instanpay/pg-detail-product.html'
    pk_url_kwarg = 'id'
    context_object_name = 'product'


# Product Update View
@method_decorator(login_required, name='dispatch')
@method_decorator(superuser_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'instanpay/pg-update-product.html'
    pk_url_kwarg = 'id'
    form_class = ProductViewForm