from zssn.models import Survivor, Inventory, Location, Flag
from zssn.serializers import SurvivorSerializer, InventorySerializer, LocationSerializer, FlagSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from zssn.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action


class SurvivorViewSet(viewsets.ModelViewSet):
    
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    

class InventoryViewSet(viewsets.ModelViewSet):
   
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class LocationViewSet(viewsets.ModelViewSet):
    
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class FlagViewSet(viewsets.ModelViewSet):
    
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer