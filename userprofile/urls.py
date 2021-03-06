from django.urls import path

from . import views

app_name = 'userprofile'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='list_profile'),
    path('user-control/', views.ProfileControl.as_view(), name='user_control'),
    # Partial data req
    path('limit/<slug:guid>/', views.limitView, name='limit'),
]