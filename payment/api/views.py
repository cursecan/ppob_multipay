from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateAPIView
)

from userprofile.models import Profile
from payment.models import Payment
from .serializers import (
    SaldoTransferSerializer, KliringPaymentSerializer
)


class TransferSaldoApiView(CreateAPIView):
    model = Payment
    serializer_class = SaldoTransferSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['sender'] = self.request.user
        return context