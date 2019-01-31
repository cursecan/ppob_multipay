from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView, GenericAPIView
)
from rest_framework.mixins import (
    CreateModelMixin, RetrieveModelMixin
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

from userprofile.models import (
    Profile, Wallet
)
from payment.api.serializers import KliringPaymentSerializer

class ProfileAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class GetMeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializers = ProfileSerializer(request.user.profile)
        return Response(serializers.data)


class UpdateLimitAPIView(UpdateAPIView):
    serializer_class = UpdateLimitSerializer
    lookup_url_kwarg = 'guid'
    lookup_field = 'guid'

    def get_queryset(self):
        return Profile.objects.filter(leader__user=self.request.user)
    

class ProfileKliringAPIView(CreateModelMixin, RetrieveAPIView):
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'guid'
    lookup_field = 'guid'

    def get_queryset(self):
        return Profile.objects.filter(leader__user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['sender'] = self.get_object().user.id
        data['receiver'] = request.user.id
        
        serializer = KliringPaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

