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



class CoverForm(ModelForm):
    class Meta:
        model = Creo
        fields = ['cover']

class CreoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Creo.objects.all()
    serializer_class = CreoSerializer    

    @action()
    def uploadCover(self, request, pk=None, format=None):
        creo = self.get_object()
        form = CoverForm(request.POST, request.FILES, instance=creo)
        if not form.is_valid():
            return Response({'status': 'invalid'})
        form.save()
        creo = Creo.objects.get(pk=pk)
        return Response(CreoSerializer(creo).data)


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        qs = Location.objects.all()
        params = self.request.QUERY_PARAMS
        address = params.get('address', None)
        neighborhood = params.get('neighborhood', None)
        zipcode = params.get('zipcode', None)
        latitude = params.get('latitude', None)
        longitude = params.get('longitude', None)
        if latitude is not None and longitude is not None:
            qs = qs.filter(Q(latitude=latitude) & Q(longitude=longitude))
        elif address is not None:
            qs = qs.filter(address__iexact=address)
        elif neighborhood is not None:
            qs = qs.filter(neighborhood__iexact=neighborhood)
        elif zipcode is not None:
            qs = qs.filter(zipcode=zipcode)
        return qs




#  ___             _        _    _    _   _              
# | __|_ _____ _ _| |_ ___ | |  (_)__| |_(_)_ _  __ _ ___
# | _|\ V / -_) ' \  _(_-< | |__| (_-<  _| | ' \/ _` (_-<
# |___|\_/\___|_||_\__/__/ |____|_/__/\__|_|_||_\__, /__/
#                                               |___/    

class EventListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreoSerializer

class FeaturedEventsList(EventListView):
    queryset = Creo.events.all()
    #TODO: probably can't get away with not returning a queryset
    #      to feature objects instead of event objects

class EventsNearYouList(EventListView):
    queryset = Creo.events.all()
    #TODO: geoDistance in python
    
class EventsForYouList(EventListView):
    def get_queryset(self):
        return getUzer(self.request).autovocatedEvents()

class EventsHappeningNowList(EventListView):
    def get_queryset(self):
        hasntEnded = Q( end__gt=localNow() )
        startsByTomorrow = Q( start__lt=endOfTomorrow() )
        return Creo.events.filter(
            hasntEnded & startsByTomorrow
        ).order_by('end')
