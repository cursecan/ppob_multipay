from django.urls import path

from . import views

app_name = 'billing'
urlpatterns = [
    path('sale/', views.SaleView.as_view(), name='list_sale'),
    path('export-sale/', views.export_transaction_csv, name='export_sale'),
    path('kliring/', views.KliringView.as_view(), name='kliring'),
]