from rest_framework.generics import (
    ListAPIView, RetrieveAPIView
)


from .serializers import BillingSerializer
from bill.models import Billing


# API View List Billing
class BillingListApiView(ListAPIView):
    serializer_class = BillingSerializer

    def get_queryset(self):
        queryset = Billing.objects.filter(seq=1)
        if self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset