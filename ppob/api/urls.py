from django.urls import path

from . import views

app_name = 'api_ppob'
urlpatterns = [
    path('transaction/', views.TransactionAPIView.as_view(), name='transaction'),
    path('topup/', views.PpobTopupAPIView.as_view(), name='topup'),
]