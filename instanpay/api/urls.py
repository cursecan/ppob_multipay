from django.urls import path

from . import views

app_name = 'api_instanpay'
urlpatterns = [
    path('product/', views.ProductInstancAPIView.as_view(), name='product'),
    path('ppob-product/', views.ProductInqueryAPIView.as_view, name='ppob_product'),
    path('product/detail/', views.ProductDetailAPIView.as_view(), name='detail_product'),
    path('transaction/', views.TransactionAPIView.as_view(), name='transaction'),
    path('topup/', views.TopUpAPIView.as_view(), name='topup'),
]