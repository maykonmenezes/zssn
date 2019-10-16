from zssn.models import Survivor, Inventory, LastLocation, Flag
from zssn.serializers import SurvivorSerializer, InventorySerializer, LastLocationSerializer, FlagSerializer
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
    """
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    

class InventoryViewSet(viewsets.ModelViewSet):
    """
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class LastLocationViewSet(viewsets.ModelViewSet):
    """
    Additionally we also provide an extra `highlight` action.
    """
    queryset = LastLocation.objects.all()
    serializer_class = LastLocationSerializer

class FlagViewSet(viewsets.ModelViewSet):
    """
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer