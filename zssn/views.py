from zssn.models import Survivor, Inventory, Location, Flag
from zssn.serializers import SurvivorSerializer, InventorySerializer, LocationSerializer, FlagSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from zssn.permissions import SurvivorInfectedReadOnly
from rest_framework.decorators import api_view
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from zssn.reports import Report


class SurvivorViewSet(viewsets.ModelViewSet):
    
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    permission_classes = [SurvivorInfectedReadOnly]

class InventoryViewSet(viewsets.ModelViewSet):
   
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class LocationViewSet(viewsets.ModelViewSet):
    
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class FlagViewSet(viewsets.ModelViewSet):
    
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer

class ReportViewSet(viewsets.ViewSet):
	def list(self, request):
        reports = []
        reports.append(Report.infected())
        reports.append(Report.non_infected())
        reports.append(Report.resource())
        reports.append(Report.lost_points())
        
        return Response(reports)