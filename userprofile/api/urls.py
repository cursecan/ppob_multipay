from django.urls import path

from . import views

app_name = 'api_profile'
urlpatterns = [
    path('user/', views.ProfileAPIView.as_view(), name='user'),
    path('my-profile/', views.GetMeAPIView.as_view(), name='get_me'),
]