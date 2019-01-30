from django.urls import path

from . import views

app_name = 'api_bill'
urlpatterns = [
    path('', views.BillingListApiView.as_view(), name='list_billing')
]