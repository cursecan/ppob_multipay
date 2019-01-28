from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView,
    CreateAPIView,
)

from .serializers import *
from ppob.models import (
    Transaction, InqueryResponse, PaymentResponse
)

# Transaction API List
class TransactionAPIView(ListAPIView):
    queryset = Transaction.objects.filter(subtype='PAY')
    serializer_class = TransactionSerializer



class PpobTopupAPIView(CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TopupPpobRequestSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super(PpobTopupAPIView, self).get_serializer_context(*args, **kwargs)
        context['user'] = self.request.user
        return context


