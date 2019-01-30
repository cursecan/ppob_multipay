from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, 
    DestroyAPIView, UpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from instanpay.models import (
    Product, Transaction
)

# Product Instan View
class ProductInstancAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True, subtype='I')

    def get_queryset(self):
        queryset = self.queryset
        group = self.request.GET.get('group', None)
        operator = self.request.GET.get('operator', None)
        subtype = self.request.GET.get('subtype', None)
        if group:
            queryset = queryset.filter(group__slug=group)
        if operator:
            queryset = queryset.filter(operator__slug=operator)
            
        return queryset


# Product Iquery View
class ProductInqueryAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True, subtype='q')

    def get_queryset(self):
        queryset = self.queryset
        group = self.request.GET.get('group', None)
        operator = self.request.GET.get('operator', None)
        subtype = self.request.GET.get('subtype', None)
        if group:
            queryset = queryset.filter(group__slug=group)
        if operator:
            queryset = queryset.filter(operator__slug=operator)
            
        return queryset
    


# Detail Product
class ProductDetailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code', None)
        product_obj = Product.objects.filter(code=code, is_active=True)
        if product_obj.exists():
            serializers = ProductSerializer(product_obj.get())
            return Response(serializers.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
        

# Transaction View
class TransactionAPIView(ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


#TopUp View
class TopUpAPIView(CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TopUpRequestSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context