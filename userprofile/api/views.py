from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *


from userprofile.models import (
    Profile, Wallet
)

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
    
    
    
        