from django.urls import path

from . import views

app_name = 'userprofile'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='list_profile'),
    path('user-control/', views.ProfileControl.as_view(), name='user_control'),
    path('user-control/<slug:guid>/', views.ProfileDetailControlView.as_view(), name='detail_user_control'),
    # Partial data req
    path('limit/<slug:guid>/', views.limitView, name='limit'),
]