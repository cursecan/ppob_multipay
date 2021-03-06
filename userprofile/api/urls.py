from django.urls import path

from . import views

app_name = 'api_profile'
urlpatterns = [
    path('user/', views.ProfileAPIView.as_view(), name='user'),
    path('my-profile/', views.GetMeAPIView.as_view(), name='get_me'),
    path('limit-update/<slug:guid>/', views.UpdateLimitAPIView.as_view(), name='limit_update'),
    path('kliring-pay/<slug:guid>/', views.ProfileKliringAPIView.as_view(), name='kliring_pay'),
]