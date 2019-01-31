from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView
)
from django.views.generic.edit import SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.db.models import Q, F, Sum, Value as V
from django.db.models.functions import Coalesce

from .models import (
    Wallet, Profile
)
from bill.models import (
    Kliring
)
from .forms import LimitForm
from core.decorators import superuser_required
from payment.forms import PublicPayment

# Profile View - Admin
# ===================
# View profile semua pengguna aplikasi
# yang hanya diakses dari Superuser
@method_decorator(login_required, name='dispatch')
@method_decorator(superuser_required, name='dispatch')
class ProfileView(ListView):
    context_object_name = 'profile_list'
    template_name = 'userprofile/pg-profile.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Profile.objects.all()
        search = self.request.GET.get('search', None)
        if search :
            queryset = queryset.filter(user__username__contains=search)
        return queryset



# Profile View - Agen
# ===================
# View profile dan control pengguna 
# dilihat dari sisi Agen
class ProfileControl(ListView):
    template_name = 'userprofile/pg-profile-control.html'
    context_object_name = 'profile_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Profile.objects.filter(
            leader=self.request.user.profile
        )
        return queryset




# Function View
# =============


# Setting Limit and View Limit
@login_required
@superuser_required
def limitView(request, guid):
    data = dict()
    wallet_obj = get_object_or_404(Wallet, profile__guid=guid)
    form = LimitForm(request.POST or None, instance=wallet_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else :
            data['form_is_valid'] = False

    content = {
        'form': form,
    }
    data['html'] = render_to_string(
        'userprofile/includes/partial-limit-form.html',
        content, request=request
    )
    return JsonResponse(data)

