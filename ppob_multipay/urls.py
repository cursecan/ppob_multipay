"""ppob_multipay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView, LogoutView
)

from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)

urlpatterns = [
    path('jwt-api-token-auth/', obtain_jwt_token),
    path('jwt-api-token-refresh/', refresh_jwt_token),
    path('jwt-api-token-verify/', verify_jwt_token),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('manage/', include('userprofile.urls')),
    path('api/manage/', include('userprofile.api.urls')),
    path('payment/', include('payment.urls')),
    path('api/payment/', include('payment.api.urls')),
    path('billing/', include('bill.urls')),
    path('api/billing/', include('bill.api.urls')),
    path('instanpay/', include('instanpay.urls')),
    path('api/instanpay/', include('instanpay.api.urls')),
    path('api/ppob/', include('ppob.api.urls')),

]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
