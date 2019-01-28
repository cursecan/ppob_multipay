from django.urls import path

from . import views

app_name = 'instanpay'
urlpatterns = [
    path('product/', views.ProductView.as_view(), name='product'),
    path('product/<int:id>/', views.ProductDetailView.as_view(), name='detail_product'),
    path('product/update/<int:id>/', views.ProductUpdateView.as_view(), name='update_product'),
]