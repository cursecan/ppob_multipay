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
    Kliring, FlagKliring
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


# Detail Profile - Agen
# =====================
class ProfileDetailControlView(SingleObjectMixin, ListView):
    template_name = 'userprofile/pg-profile-detail-control.html'
    slug_url_kwarg = 'guid'
    slug_field = 'guid'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Profile.objects.all())
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset, *args, **kwargs):
        obj = super(ProfileDetailControlView, self).get_object(queryset, *args, **kwargs)
        return obj

    def get_queryset(self):
        queryset_obj = Kliring.unclean_objects.filter(
            seq=1, buyer=self.object.user, leader=self.request.user, flag__isnull=True
        )
        return queryset_obj

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailControlView, self).get_context_data(*args, **kwargs)
        kliring_res_obj = self.get_queryset().aggregate(total=Coalesce(Sum('loan'), V(0)))
        
        context['kliring_list'] = self.get_queryset()
        context['total_loan'] = kliring_res_obj.get('total')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Profile.objects.all())
        klir_objs = self.get_queryset()
        klir_ammount = klir_objs.aggregate(total=Coalesce(Sum('loan'), V(0)))
        if klir_ammount.get('total') > 0:
            flag_obj = FlagKliring.objects.create(
                amount = klir_ammount.get('total'),
                buyer = self.object.user,
                leader = request.user
            )
            klir_objs.update(
                flag = flag_obj
            )
        return redirect('userprofile:user_control')

        



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

