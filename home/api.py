#           _____ _____ 
#     /\   |  __ \_   _|
#    /  \  | |__) || |  
#   / /\ \ |  ___/ | |  
#  / ____ \| |    _| |_ 
# /_/    \_\_|   |_____|

from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.forms import ModelForm

from rest_framework import viewsets, authentication, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

import django_filters

from permissions import *
from serializers import *
from models import *
from utilities import *




class UserExistsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username, format=None):
        exists = User.objects.filter(username=username).exists()
        return Response(exists)


class SetPasswordView(APIView):
    permission_classes = (JustMe,)

#    def post(self, request, format=None):


class IsEmailVerifiedView(APIView):
    permission_classes = (JustMe,)

    def post(self, request, format=None):
        try:
            isVerified = getUzer(request).isEmailVerified
        except Uzer.DoesNotExist:
            isVerified = False
        return Response(isVerified)



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CreoFilter(django_filters.FilterSet):
    latitudeMin = django_filters.NumberFilter(name='location__latitude', lookup_type='gte')
    latitudeMax = django_filters.NumberFilter(name='location__latitude', lookup_type='lte')
    longitudeMin = django_filters.NumberFilter(name='location__longitude', lookup_type='gte')
    longitudeMax = django_filters.NumberFilter(name='location__longitude', lookup_type='lte')

    class Meta:
        model = Creo
        fields = ('creotype',
                  'latitudeMin','latitudeMax',
                  'longitudeMin','longitudeMax',)


class CreoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Creo.objects.all()
    serializer_class = CreoSerializer
    filter_class = CreoFilter

    @action()
    def uploadCover(self, request, pk=None, format=None):
        class CoverForm(ModelForm):
            class Meta:
                model = Creo
                fields = ['cover']
        creo = self.get_object()
        form = CoverForm(request.POST, request.FILES, instance=creo)
        if not form.is_valid():
            return Response({'status': 'invalid'})
        form.save()
        creo = Creo.objects.get(pk=pk)
        return Response(CreoSerializer(creo).data)


class LocationFilter(django_filters.FilterSet):
    neighborhood = django_filters.CharFilter(lookup_type='iexact')
    latitudeMin = django_filters.NumberFilter(name='latitude', lookup_type='gte')
    latitudeMax = django_filters.NumberFilter(name='latitude', lookup_type='lte')
    longitudeMin = django_filters.NumberFilter(name='longitude', lookup_type='gte')
    longitudeMax = django_filters.NumberFilter(name='longitude', lookup_type='lte')

    class Meta:
        model = Location
        fields = ('neighborhood','zipcode','address',
                  'latitude','longitude',
                  'latitudeMin','latitudeMax',
                  'longitudeMin','longitudeMax',)


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_class = LocationFilter



#TODO: turn this into a @link() ?
# class EventsForYouList(EventListView):
#     def get_queryset(self):
#         return getUzer(self.request).autovocatedEvents()
