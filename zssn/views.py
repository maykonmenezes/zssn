from zssn.models import Survivor, Inventory, Location, Flag
from zssn.serializers import SurvivorSerializer, InventorySerializer, LastLocationSerializer, FlagSerializer, TradeSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from zssn.permissions import SurvivorReadOnly
from rest_framework.decorators import api_view
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from zssn.reports import Report
from django.shortcuts import get_object_or_404

class SurvivorViewSet(viewsets.ModelViewSet):
    
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    
    def update(self, request):
        return Response({'status':'Survivor changes not allowed!'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['post'], detail=True, serializer_class=LastLocationSerializer)
    def last_location(self, request, pk):
        ls = LastLocationSerializer(data=request.data)
        survivor = get_object_or_404(Survivor, id=pk)
        if ls.is_valid():
            survivor.location.latitude = ls.data['latitude']
            survivor.location.longitude = ls.data['longitude']
            survivor.save()
            return Response({'status':'Survivor last location updated successfully'}, 
                status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, serializer_class=FlagSerializer)
    def flag(self, request,pk):
        fs = FlagSerializer(data=request.data)
        flagged = get_object_or_404(Survivor, id=fs.initial_data['flagged_id'])
        flagging = get_object_or_404(Survivor, id=pk)
        if fs.is_valid():
            if not flagged == flagging:
                flag = Flag()
                flag.flagged = flagged
                flag.flagging = flagging
                flag.save()
                return Response({'status':'Survivor flagged as infected successfully!'}, 
                    status=status.HTTP_200_OK)
            else:
                return Response({'status':'Survivors cannot flag themselves as infected'}, 
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['post'], detail=True, serializer_class=TradeSerializer)
    def trade(self, request, pk):
        ts = TradeSerializer(data=request.data)
        dealer = get_object_or_404(Survivor,id=pk)
        buyer = get_object_or_404(Survivor,id=ts.initial_data['buyer_id'])
        if ts.is_valid():
            if not dealer.infected or not buyer.infected:
                points_dealer = (int(ts.data['pick_water']) * 4 + int(ts.data['pick_food']) * 3 +
                                 int(ts.data['pick_med']) * 2 + int(ts.data['pick_ammo']) * 1)
                points_buyer = (int(ts.data['offer_water']) * 4 + int(ts.data['offer_food']) * 3 +
                                    int(ts.data['offer_med']) * 2 + int(ts.data['offer_ammo']) * 1)     
                if dealer.inventory.get_points() >= points_dealer or buyer.inventory.get_points() >= points_buyer:
                    if points_dealer == points_buyer:
                        dealer.inventory.water -= ts.data['pick_water']
                        dealer.inventory.food -= ts.data['pick_food']
                        dealer.inventory.med -= ts.data['pick_med']
                        dealer.inventory.ammo -= ts.data['pick_ammo']

                        buyer.inventory.water -= ts.data['offer_water']
                        buyer.inventory.food -= ts.data['offer_food']
                        buyer.inventory.med -= ts.data['offer_med']
                        buyer.inventory.ammo -= ts.data['offer_ammo']

                        buyer.inventory.water += ts.data['pick_water']
                        buyer.inventory.food += ts.data['pick_food']
                        buyer.inventory.med += ts.data['pick_med']
                        buyer.inventory.ammo += ts.data['pick_ammo']

                        dealer.inventory.water += ts.data['offer_water']
                        dealer.inventory.food += ts.data['offer_food']
                        dealer.inventory.med += ts.data['offer_med']
                        dealer.inventory.ammo += ts.data['offer_ammo']

                        dealer.inventory.save()
                        buyer.inventory.save()
                        return Response({'status':'Items traded successfully!'}, 
                            status=status.HTTP_200_OK)
                    else:
                        return Response({'status':'Sorry couldnt make it, one of the traders doesnt have enough points to trade!'}, 
                            status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response({'status':'One of the traders doesnt have enough points to trade!'}, 
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'status':'Trade failed due to one of the traders is infected!'}, 
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
  

class InventoryViewSet(viewsets.ModelViewSet):
   
   queryset = Inventory.objects.all()
   serializer_class = InventorySerializer
   permission_classes = [SurvivorReadOnly]


class ReportViewSet(viewsets.ViewSet):

    @action(methods=['get'], detail=False)
    def infected(self, request):
        return Response(Report.infected())

    @action(methods=['get'], detail=False)
    def non_infected(self, request):
        return Response(Report.non_infected())
    
    @action(methods=['get'], detail=False)
    def resource(self, request):
        return Response(Report.resource())

    @action(methods=['get'], detail=False)
    def lost_points(self, request):
        return Response(Report.lost_points())
                    