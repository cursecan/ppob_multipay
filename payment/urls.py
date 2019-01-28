from django.urls import path

from . import views

app_name = 'payment'
urlpatterns = [
    # Partial data
    path('add-saldo/<slug:guid>/', views.paymentView, name='manual_payment'),
]