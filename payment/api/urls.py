from django.urls import path

from . import views

app_name = 'api_payment'
urlpatterns = [
    path('transfer/', views.TransferSaldoApiView.as_view(), name='transfer'),
]