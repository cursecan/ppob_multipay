from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Payment
from .forms import PaymentForm
from userprofile.models import Profile
from core.decorators import superuser_required

# Function View
# ============


@login_required
@superuser_required
def paymentView(request, guid):
    profile_obj = get_object_or_404(Profile, guid=guid)
    data = dict()

    form = PaymentForm(request.POST or None, initial={'sender': profile_obj.user, 'amount': 0})
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.receiver = request.user
            instance.save()
            data['form_is_valid'] = True
        else :
            data['form_is_valid'] = False

    content = {
        'profile': profile_obj,
        'form': form
    }

    data['html'] = render_to_string(
        'payment/includes/partial-payment.html',
        content, request=request
    )
    return JsonResponse(data)